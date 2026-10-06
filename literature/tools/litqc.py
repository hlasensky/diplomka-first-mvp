#!/usr/bin/env python3
"""Deterministic quality control for the literature vault (stdlib only, no LLM).

Subcommands:
  ocr      KEY...|--all [--force]   OCR every PDF page -> fulltext/<key>.ocr.txt (independent 2nd extraction)
  fulltext KEY...|--all [--repair]  compare fulltext/<key>.txt with OCR page by page; --repair swaps BAD pages for OCR
  stamp    KEY                      record hashes of the note's current claims into qc/<key>.claims.json
  claims   KEY...|--all             check qc/<key>.claims.json evidence against fulltext + OCR + claim pages/numbers
  lint                              vault-wide consistency (bib, notes, concepts, wikilinks, fulltexts)
  check    KEY...|--all             ocr (if missing) + fulltext + claims + lint, writes qc/<key>.md and qc/_vault.md
  plan     [--sync]                 pair literature/seznam.md with Zotero + notes, status per item -> qc/_plan.md;
                                    --sync writes uroven into note frontmatter
  meta     [KEY...]                 compare bib entries with Crossref + Semantic Scholar (OpenAlex fallback) -> qc/_metadata.md (never edits the bib)

Exit code 1 when any ERROR is found.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "literature"
BIB = ROOT / "thesis" / "projekt-20-literatura-bibliography.bib"
SOURCES = VAULT / "sources"
CONCEPTS = VAULT / "concepts"
FULLTEXT = VAULT / "fulltext"
QC = VAULT / "qc"
DICT = Path("/usr/share/dict/cracklib-small")

PAGE_RE = re.compile(r"^=== PAGE (\d+) ===(?: \(OCR\))?$", re.M)
CLAIM_RE = re.compile(r"^- (C\d+):\s*(.*)$", re.M)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")

# Page-agreement thresholds (pdftotext vs OCR), calibrated on the first 4 papers.
MIN_OCR_TOKENS = 40      # fewer OCR tokens = figure/blank page, metrics not meaningful
BAD_RECALL = 0.70        # share of OCR words also present in fulltext
WARN_RECALL = 0.85
WARN_BIGRAM = 0.60       # share of OCR word pairs present in fulltext (reading order)
QUOTE_OCR_MIN = 0.80     # share of quote words/bigrams that must be found on the OCR page

LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st",
             "\u00ad": "", "\u00a0": " ", "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
             "−": "-", "×": "x"}


# ---------------------------------------------------------------- reporting

@dataclass
class Issue:
    level: str   # ERROR | WARN | INFO
    code: str
    msg: str

    def md(self) -> str:
        return f"| {self.level} | {self.code} | {self.msg.replace('|', '/')} |"


@dataclass
class Result:
    issues: list[Issue] = field(default_factory=list)
    tables: list[str] = field(default_factory=list)

    def add(self, level: str, code: str, msg: str) -> None:
        self.issues.append(Issue(level, code, msg))

    @property
    def errors(self) -> int:
        return sum(i.level == "ERROR" for i in self.issues)

    @property
    def warns(self) -> int:
        return sum(i.level == "WARN" for i in self.issues)


# ---------------------------------------------------------------- text utils

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    for a, b in LIGATURES.items():
        text = text.replace(a, b)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)        # line-break hyphenation
    return re.sub(r"\s+", " ", text).strip()


def loose(text: str) -> str:
    """Lowercase, letters and digits only. Robust to spacing, punctuation, hyphenation."""
    return re.sub(r"[^0-9a-z]", "", normalize(text).lower())


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]{3,}", normalize(text).lower())


def bigrams(ws: list[str]) -> Counter:
    return Counter(zip(ws, ws[1:]))


def overlap(part: Counter, whole: Counter) -> float:
    total = sum(part.values())
    return sum((part & whole).values()) / total if total else 1.0


def split_pages(text: str) -> dict[int, str]:
    pages: dict[int, str] = {}
    marks = list(PAGE_RE.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        pages[int(m.group(1))] = text[m.end():end]
    return pages


_DICT: set[str] | None = None


def dict_ratio(ws: list[str]) -> float | None:
    global _DICT
    if _DICT is None:
        _DICT = set(DICT.read_text(errors="ignore").split()) if DICT.exists() else set()
    if not _DICT or not ws:
        return None
    return sum(w in _DICT or w.rstrip("s") in _DICT for w in ws) / len(ws)


# ---------------------------------------------------------------- bib / notes

def read_bib() -> dict[str, dict[str, str]]:
    text = BIB.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        i, depth = m.end(), 1
        while depth and i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        body = text[m.end():i - 1]
        fields = {"_type": m.group(1).lower()}
        for f in re.finditer(r"(\w+)\s*=\s*", body):
            j = f.end()
            if j < len(body) and body[j] == "{":
                d, k = 0, j
                while k < len(body):
                    d += {"{": 1, "}": -1}.get(body[k], 0)
                    k += 1
                    if d == 0:
                        break
                val = body[j + 1:k - 1]
            else:
                val = re.match(r"[^,\n]*", body[j:]).group(0)
            fields.setdefault(f.group(1).lower(), val.strip())
        entries[m.group(2)] = fields
    return entries


def pdf_path(entry: dict[str, str]) -> Path | None:
    for part in entry.get("file", "").split(";"):
        part = part.strip()
        if part.lower().endswith(".pdf") and Path(part).exists():
            return Path(part)
    return None


def frontmatter(text: str) -> dict[str, object]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data: dict[str, object] = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"\s+-\s+", line) and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line.split("-", 1)[1].strip().strip("\"'"))
            continue
        km = re.match(r"(\w+):\s*(.*)$", line)
        if not km:
            continue
        key, val = km.group(1), km.group(2)
        if not val.startswith(('"', "'")):
            val = val.split(" #")[0]
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            data[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
        elif val == "":
            data[key] = []
        else:
            data[key] = val.strip("\"'")
    return data


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


@dataclass
class Claim:
    cid: str
    text: str            # claim without the trailing page reference
    ref: str             # raw "(s. …)" reference
    pages: list[set[int]]  # one set per "s. X" / "s. X–Y" item (PDF pages, before "|")

    @property
    def all_pages(self) -> set[int]:
        return set().union(*self.pages) if self.pages else set()

    @property
    def sha(self) -> str:
        return hashlib.sha1(normalize(self.text + " " + self.ref).encode()).hexdigest()[:12]


def parse_claims(note: str) -> list[Claim]:
    claims = []
    for cid, body in CLAIM_RE.findall(section(note, "Klíčová tvrzení")):
        refs = list(re.finditer(r"\(([^()]*\bs\.\s*\d[^()]*)\)", body))
        ref = refs[-1] if refs else None
        text = body[:ref.start()].strip() if ref else body.strip()
        pages = []
        if ref:
            pdf_part = ref.group(1).split("|")[0]
            for a, b in re.findall(r"\bs\.\s*(\d+)(?:\s*[–-]\s*(\d+))?", pdf_part):
                pages.append(set(range(int(a), int(b or a) + 1)))
        claims.append(Claim(cid, text, ref.group(0) if ref else "", pages))
    return claims


def strip_links(text: str) -> str:
    return WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1), text)


# ---------------------------------------------------------------- OCR

def pdf_pages(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def ocr_page(pdf: Path, page: int) -> str:
    # tesseract runs in firejail without access to Zotero storage -> feed the image via stdin.
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    render = subprocess.Popen(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "300", "-gray", "-png", str(pdf)],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    ocr = subprocess.run(["tesseract", "stdin", "stdout", "-l", "eng"], stdin=render.stdout,
                         capture_output=True, text=True, env=env)
    render.stdout.close()
    render.wait()
    return ocr.stdout


def ocr_path(key: str) -> Path:
    return FULLTEXT / f"{key}.ocr.txt"


def cmd_ocr(key: str, bib: dict, force: bool = False) -> Path | None:
    out = ocr_path(key)
    if out.exists() and not force:
        return out
    pdf = pdf_path(bib.get(key, {}))
    if not pdf:
        return None
    n = pdf_pages(pdf)
    print(f"[ocr] {key}: {n} pages", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) // 2)) as ex:
        texts = list(ex.map(lambda p: ocr_page(pdf, p), range(1, n + 1)))
    out.write_text("".join(f"=== PAGE {i} ===\n{t.rstrip()}\n" for i, t in enumerate(texts, 1)), encoding="utf-8")
    return out


# ---------------------------------------------------------------- fulltext QC

def page_stats(ft: str, oc: str) -> dict:
    fw, ow = words(ft), words(oc)
    s = {
        "ft_words": len(fw), "ocr_words": len(ow),
        "recall": overlap(Counter(ow), Counter(fw)) if ow else None,
        "precision": overlap(Counter(fw), Counter(ow)) if fw and ow else None,
        "bigram": overlap(bigrams(ow), bigrams(fw)) if len(ow) > 1 else None,
        "dict_ft": dict_ratio(fw), "dict_ocr": dict_ratio(ow),
        "cid": len(re.findall(r"\(cid:\d+\)", ft)),
        "bad_chars": ft.count("\ufffd"),
        "pua": sum("\ue000" <= c <= "\uf8ff" for c in ft),               # private-use glyphs (math fonts)
        "spaced": len(re.findall(r"\b(?:[A-Za-z] ){3,}[A-Za-z]\b", ft)),  # "t h a t" letter-spacing
    }
    if len(ow) < MIN_OCR_TOKENS:
        s["status"] = "BAD" if len(fw) < 0.5 * len(ow) and len(ow) >= 15 else "SKIP"
    elif s["cid"] or s["bad_chars"] > 5 or s["spaced"] > 5 or s["recall"] < BAD_RECALL:
        s["status"] = "BAD"
    elif (s["recall"] < WARN_RECALL or (s["bigram"] or 1) < WARN_BIGRAM or s["spaced"]
          or s["pua"] > 0.005 * max(len(ft), 1)):
        s["status"] = "WARN"
    else:
        s["status"] = "OK"
    return s


def fmt(x) -> str:
    return "–" if x is None else (f"{x:.2f}" if isinstance(x, float) else str(x))


def cmd_fulltext(key: str, bib: dict, res: Result, repair: bool = False) -> None:
    ftp = FULLTEXT / f"{key}.txt"
    if not ftp.exists():
        res.add("ERROR", "NO_FULLTEXT", f"chybí fulltext/{key}.txt")
        return
    pdf = pdf_path(bib.get(key, {}))
    ocp = cmd_ocr(key, bib)
    if not pdf or not ocp:
        res.add("WARN", "NO_PDF", "PDF není dostupné přes bib `file` → fulltext nelze porovnat s OCR")
        return
    n = pdf_pages(pdf)
    ft_text = ftp.read_text(encoding="utf-8")
    ft, oc = split_pages(ft_text), split_pages(ocp.read_text(encoding="utf-8"))
    if max(ft, default=0) > n:
        res.add("ERROR", "PAGE_COUNT", f"fulltext má značku strany {max(ft)}, PDF má jen {n} stran")
    rows, bad = [], []
    for p in range(1, n + 1):
        s = page_stats(ft.get(p, ""), oc.get(p, ""))
        if s["status"] in ("BAD", "WARN"):
            rows.append(f"| {p} | {s['status']} | {s['ft_words']} | {s['ocr_words']} | {fmt(s['recall'])} | "
                        f"{fmt(s['precision'])} | {fmt(s['bigram'])} | {fmt(s['dict_ft'])} | {fmt(s['dict_ocr'])} | "
                        f"{s['cid'] + s['bad_chars']}/{s['pua']}/{s['spaced']} |")
        if s["status"] == "BAD":
            bad.append((p, s))
        elif s["status"] == "WARN":
            res.add("WARN", "PAGE_WARN", f"s. {p}: shoda s OCR recall {fmt(s['recall'])}, pořadí {fmt(s['bigram'])}, "
                    f"PUA {s['pua']}, rozpalovaná slova {s['spaced']} (tabulka/vzorec/sloupce?) – ověř v PDF, "
                    "než z ní cituješ")
    ocr_marked = [int(m.group(1)) for m in re.finditer(r"^=== PAGE (\d+) === \(OCR\)$", ft_text, re.M)]
    repaired = []
    for p, s in bad:
        if p in ocr_marked:
            continue
        better = ((s["dict_ocr"] or 0) > (s["dict_ft"] or 0) + 0.05 or s["cid"] or s["bad_chars"] > 5
                  or s["spaced"] > 5 or (s["recall"] or 1) < BAD_RECALL)
        if repair and better and os.access(ftp, os.W_OK):
            repaired.append(p)
        else:
            res.add("ERROR", "PAGE_BAD", f"s. {p}: fulltext nesedí s PDF (recall {fmt(s['recall'])}, "
                    f"{s['ft_words']} vs {s['ocr_words']} slov OCR)" + ("" if os.access(ftp, os.W_OK) else
                    " – soubor je jen pro čtení, oprav ručně"))
    if repaired:
        for p in repaired:
            ft[p] = "\n" + oc[p].strip() + "\n"
        out = "".join(f"=== PAGE {p} ==={' (OCR)' if p in repaired or p in ocr_marked else ''}\n{ft[p].strip()}\n"
                      for p in sorted(ft))
        ftp.write_text(out, encoding="utf-8")
        res.add("WARN", "PAGE_REPAIRED", f"strany {', '.join(map(str, repaired))} nahrazeny OCR textem "
                "(pdftotext byl horší) – zmínit v „Pozor“")
    if ocr_marked:
        res.add("INFO", "PAGE_OCR", f"strany z OCR: {', '.join(map(str, ocr_marked))}")
    ok = n - len(rows)
    res.tables.append(f"### Fulltext vs. OCR\n\n{n} stran PDF, {ok} bez nálezu. "
                      "recall = podíl slov z OCR, která jsou ve fulltextu; pořadí = shoda dvojic slov.\n")
    if rows:
        res.tables.append("| strana | stav | slov ft | slov OCR | recall | precision | pořadí | slovník ft | slovník OCR | cid+�/PUA/r o z p a l |\n"
                          "|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


# ---------------------------------------------------------------- claims QC

def claims_json(key: str) -> Path:
    return QC / f"{key}.claims.json"


def cmd_stamp(key: str) -> None:
    note = (SOURCES / f"{key}.md").read_text(encoding="utf-8")
    path = claims_json(key)
    data = json.loads(path.read_text(encoding="utf-8"))
    current = {c.cid: c for c in parse_claims(note)}
    for cid, entry in data.get("claims", {}).items():
        if cid in current:
            entry["claim_sha"] = current[cid].sha
    data["stamped"] = date.today().isoformat()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"stamped {len(current)} claims in {path.relative_to(ROOT)}")


NUM_RE = re.compile(r"(?<![\w.])\d{1,3}(?:[ \u00a0]\d{3})+(?:,\d+)?|(?<![\w.^])\d+(?:[.,]\d+)?")


def claim_numbers(text: str) -> list[str]:
    text = re.sub(r"§\s*[\d.–-]+|\b(?:Def|Eq|Obr|Tab|Example|C)\.?\s*\d+|\[[^\]]*\]", " ", strip_links(text))
    out = []
    for raw in NUM_RE.findall(text):
        n = re.sub(r"[ \u00a0]", "", raw).replace(",", ".")
        if re.fullmatch(r"\d+", n) and int(n) <= 10:
            continue                                  # small integers are usually spelled out in English
        out.append(n)
    return out


def number_in(n: str, text: str) -> bool:
    plain = normalize(text)
    # Thousands separators are joined so "2 404" matches 2404, but that also glues adjacent
    # table cells ("25 940" -> 25940), so the unjoined text is searched as well.
    texts = (re.sub(r"(?<=\d)[, ](?=\d{3}\b)", "", plain), plain)
    variants = {n}
    if n.startswith("0."):
        variants.add(n[1:])                           # .90
    if "." in n:
        variants.add(n.rstrip("0").rstrip("."))
    return any(re.search(rf"(?<![\d.]){re.escape(v)}(?!\d)", t) for t in texts for v in variants)


def quote_on_ocr(quote: str, page_text: str) -> float:
    qw, pw = words(quote), words(page_text)
    if len(qw) < 3:
        return 1.0
    return min(overlap(Counter(qw), Counter(pw)), overlap(bigrams(qw), bigrams(pw)))


def cmd_claims(key: str, res: Result) -> None:
    notep = SOURCES / f"{key}.md"
    if not notep.exists():
        res.add("ERROR", "NO_NOTE", f"chybí sources/{key}.md")
        return
    claims = parse_claims(notep.read_text(encoding="utf-8"))
    if not claims:
        res.add("ERROR", "NO_CLAIMS", "poznámka nemá žádné claims")
        return
    for c in claims:
        if not c.pages:
            res.add("ERROR", "CLAIM_NO_PAGE", f"{c.cid}: chybí stránka `(s. N, §…)`")
    ids = [int(c.cid[1:]) for c in claims]
    if ids != list(range(1, len(ids) + 1)):
        res.add("WARN", "CLAIM_NUMBERING", f"číslování claims není souvislé: {ids}")

    ftp = FULLTEXT / f"{key}.txt"
    ft = split_pages(ftp.read_text(encoding="utf-8")) if ftp.exists() else {}
    oc = split_pages(ocr_path(key).read_text(encoding="utf-8")) if ocr_path(key).exists() else {}
    jp = claims_json(key)
    if not jp.exists():
        res.add("ERROR", "NOT_VERIFIED", f"chybí qc/{key}.claims.json – claims neprošly ověřovacím agentem")
        return
    data = json.loads(jp.read_text(encoding="utf-8")).get("claims", {})
    rows = []
    for c in claims:
        e = data.get(c.cid)
        if not e:
            res.add("ERROR", "CLAIM_UNCHECKED", f"{c.cid}: chybí v claims.json")
            rows.append(f"| {c.cid} | – | – | – | – | – |")
            continue
        verdict = e.get("verdict", "?")
        stale = e.get("claim_sha") != c.sha
        if stale:
            res.add("ERROR", "CLAIM_STALE", f"{c.cid}: claim se změnil po ověření (nebo chybí `stamp`) – ověřit znovu")
        if verdict != "supported":
            res.add("ERROR", "CLAIM_" + verdict.upper(), f"{c.cid}: verdikt `{verdict}` – {e.get('note', '')}")
        ev_pages, q_ok, o_scores = set(), 0, []
        for ev in e.get("evidence", []):
            p, q = int(ev.get("page", 0)), ev.get("quote", "")
            ev_pages.add(p)
            if len(words(q)) < 4:
                res.add("ERROR", "QUOTE_SHORT", f"{c.cid}: citace „{q[:40]}“ je moc krátká na jednoznačné ověření")
            if loose(q) and loose(q) in loose(ft.get(p, "")):
                q_ok += 1
            else:
                where = [pp for pp, t in ft.items() if loose(q) and loose(q) in loose(t)]
                res.add("ERROR", "QUOTE_NOT_FOUND", f"{c.cid}: citace „{q[:60]}…“ není ve fulltextu na s. {p}"
                        + (f" (je na s. {where})" if where else ""))
            if oc:
                score = quote_on_ocr(q, oc.get(p, ""))
                o_scores.append(score)
                if score < QUOTE_OCR_MIN:
                    res.add("ERROR", "QUOTE_NOT_IN_PDF", f"{c.cid}: citace z s. {p} se v OCR téže strany PDF "
                            f"nenašla (shoda {score:.2f}) – fulltext může být chybný")
            if c.pages and p not in c.all_pages:
                res.add("ERROR", "PAGE_MISMATCH", f"{c.cid}: důkaz je na s. {p}, claim cituje {c.ref}")
        if not e.get("evidence"):
            res.add("ERROR", "NO_EVIDENCE", f"{c.cid}: bez důkazu")
        for i, group in enumerate(c.pages):
            if not group & ev_pages:
                res.add("WARN", "REF_UNSUPPORTED", f"{c.cid}: citovaná s. {min(group)}"
                        f"{'–' + str(max(group)) if len(group) > 1 else ''} nemá žádný důkaz")
        cited_text = " ".join(ft.get(p, "") + " " + oc.get(p, "") for p in c.all_pages | ev_pages)
        missing = [n for n in claim_numbers(c.text) if not number_in(n, cited_text)]
        if missing:
            res.add("ERROR", "NUMBER_NOT_FOUND", f"{c.cid}: čísla {', '.join(missing)} nejsou na citovaných stranách "
                    "(převod? graf? – ověř)")
        rows.append(f"| {c.cid} | {verdict}{' (STALE)' if stale else ''} | {', '.join(map(str, sorted(ev_pages)))} | "
                    f"{q_ok}/{len(e.get('evidence', []))} | {fmt(min(o_scores)) if o_scores else '–'} | "
                    f"{(e.get('note') or '').replace('|', '/')[:120]} |")
    for extra in set(data) - {c.cid for c in claims}:
        res.add("WARN", "CLAIM_ORPHAN", f"{extra}: je v claims.json, ale ne v poznámce")
    res.tables.append("### Claims\n\n| claim | verdikt | strany důkazů | citace ve fulltextu | min. shoda s OCR | poznámka ověřovatele |\n"
                      "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


# ---------------------------------------------------------------- vault lint

# How far the user has read a paper (frontmatter `precteno`, set only by the user), shallow -> deep.
READ_STATES = ("ne", "abstrakt", "uvod-zaver", "prolet", "cele")


def cmd_lint(bib: dict, res: Result) -> None:
    notes = {p.stem: p.read_text(encoding="utf-8") for p in sorted(SOURCES.glob("*.md"))}
    concepts = {p.stem: p.read_text(encoding="utf-8") for p in sorted(CONCEPTS.glob("*.md"))}
    names = {p.stem for p in VAULT.rglob("*.md")} | {p.name for p in VAULT.rglob("*") if p.is_file()}

    for key in sorted(set(bib) - set(notes)):
        res.add("INFO", "TO_INGEST", f"{key}: v bibu, ale bez poznámky (`/ingest {key}`)")
    for key, text in notes.items():
        fm = frontmatter(text)
        if key not in bib:
            res.add("ERROR", "NOT_IN_BIB", f"sources/{key}.md: citekey není v bibu (změnil se v Zoteru?)")
        if fm.get("citekey") != key:
            res.add("ERROR", "CITEKEY_MISMATCH", f"{key}: frontmatter citekey `{fm.get('citekey')}` ≠ název souboru")
        if fm.get("status") not in ("candidate", "confirmed", "rejected"):
            res.add("ERROR", "BAD_STATUS", f"{key}: status `{fm.get('status')}`")
        if fm.get("verified") not in ("true", "false"):
            res.add("ERROR", "BAD_VERIFIED", f"{key}: verified `{fm.get('verified')}`")
        if fm.get("status") == "confirmed" and fm.get("verified") != "true":
            res.add("WARN", "CONFIRMED_UNVERIFIED", f"{key}: confirmed, ale verified: false")
        read = fm.get("precteno")
        if read is None:
            res.add("WARN", "NO_PRECTENO", f"{key}: chybí `precteno` ({' | '.join(READ_STATES)})")
        elif read not in READ_STATES:
            res.add("ERROR", "BAD_PRECTENO", f"{key}: precteno `{read}` (povoleno: {' | '.join(READ_STATES)})")
        elif fm.get("status") == "confirmed" and read in ("ne", "abstrakt"):
            res.add("WARN", "CONFIRMED_UNREAD", f"{key}: confirmed, ale precteno: {read}")
        if fm.get("status") == "confirmed" and not section(text, "Citovat pro"):
            res.add("INFO", "NO_CITE_FOR", f"{key}: confirmed, ale „Citovat pro“ je prázdné")
        if key in bib:
            e = bib[key]
            if not e.get("year"):
                res.add("WARN", "BIB_NO_YEAR", f"{key}: bib záznam nemá rok (citekey se může změnit)")
            if e.get("year") and str(fm.get("year")) != e["year"]:
                res.add("WARN", "YEAR_MISMATCH", f"{key}: rok v poznámce {fm.get('year')} ≠ bib {e['year']}")
            zm = re.search(r"storage/([A-Z0-9]{8})/", e.get("file", ""))
            zl = re.search(r"items/([A-Z0-9]*)\)", text)
            if zm and zl and zl.group(1) != zm.group(1):
                res.add("ERROR", "ZOTERO_LINK", f"{key}: odkaz do Zotera {zl.group(1)} ≠ příloha {zm.group(1)}")
            if not pdf_path(e):
                res.add("WARN", "PDF_MISSING", f"{key}: PDF z bib `file` neexistuje")
        if not (FULLTEXT / f"{key}.txt").exists():
            res.add("ERROR", "NO_FULLTEXT", f"{key}: chybí fulltext")
        claim_ids = {c.cid for c in parse_claims(text)}
        fm_concepts = fm.get("concepts") or []
        for c in fm_concepts:
            if c not in concepts:
                res.add("ERROR", "CONCEPT_MISSING", f"{key}: koncept `{c}` neexistuje")
            elif f"[[{key}]]" not in section(concepts[c], "Sources"):
                res.add("ERROR", "CONCEPT_BACKLINK", f"{key} → [[{c}]], ale koncept zdroj neuvádí v Sources")
        for c, ctext in concepts.items():
            for line in section(ctext, "Sources").splitlines():
                m = re.search(rf"\[\[{re.escape(key)}\]\]", line)
                if not m:
                    continue
                if c not in fm_concepts:
                    res.add("ERROR", "CONCEPT_FORWARD", f"[[{c}]] uvádí {key}, ale poznámka nemá `{c}` v concepts")
                for cid in re.findall(r"\bC\d+\b", line):
                    if cid not in claim_ids:
                        res.add("ERROR", "CONCEPT_CLAIM", f"[[{c}]] odkazuje na {key} {cid}, který neexistuje")
    for path in sorted(VAULT.rglob("*.md")):
        if any(part in ("_templates", "qc", ".obsidian") for part in path.relative_to(VAULT).parts):
            continue
        body = re.sub(r"```.*?```|`[^`\n]*`", "", path.read_text(encoding="utf-8"), flags=re.S)  # skip code
        for m in WIKILINK_RE.finditer(body):
            target = m.group(1).strip()
            if target not in names and Path(target).name not in names:
                res.add("ERROR", "BROKEN_LINK", f"{path.relative_to(VAULT)}: [[{target}]] neexistuje")
    for ft in sorted(FULLTEXT.glob("*.txt")):
        stem = ft.name.split(".")[0]
        if stem not in notes:
            res.add("WARN", "ORPHAN_FULLTEXT", f"fulltext/{ft.name} nemá poznámku")
    for jp in sorted(QC.glob("*.claims.json")):
        if jp.name.split(".")[0] not in notes:
            res.add("WARN", "ORPHAN_QC", f"qc/{jp.name} nemá poznámku")


# ---------------------------------------------------------------- reading list (plan)

SEZNAM = VAULT / "seznam.md"
LEVEL_NAMES = {"1": "1 povinné", "2": "2 důležité", "3": "3 doplňkové", "nastroje": "nástroje a data"}


@dataclass
class PlanItem:
    no: int
    level: str
    text: str
    dois: list[str] = field(default_factory=list)
    arxiv: list[str] = field(default_factory=list)
    key: str | None = None


def read_plan() -> list[PlanItem]:
    """Parse literature/seznam.md. Item numbers are only valid inside one revision of the list."""
    text = SEZNAM.read_text(encoding="utf-8")
    items: dict[int, PlanItem] = {}
    level = None
    for line in text.splitlines():
        s = line.strip()
        if m := re.match(r"ÚROVEŇ (\d)\b", s):
            level = m.group(1)
        elif s.startswith("NÁSTROJE A DATA"):
            level = "nastroje"
        elif re.match(r"(VYŘAZENO|NEVYŘEŠENO|OPRAVY|SHRNUTÍ|KONTROLNÍ SEZNAM)", s):
            level = None
        elif level and (m := re.match(r"(\d+)\.\s+(.+)", s)):
            item = PlanItem(int(m.group(1)), level, m.group(2))
            item.dois = [d.rstrip(".,;)").lower() for d in re.findall(r"\b10\.\d{4,9}/\S+", s)]
            item.arxiv = re.findall(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", s)
            items[item.no] = item
    return [items[n] for n in sorted(items)]


def bib_title(entry: dict[str, str]) -> str:
    return re.sub(r"[{}\\]", "", entry.get("title", ""))


def title_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", normalize(text).lower()))


def match_plan(plan: list[PlanItem], bib: dict) -> dict[str, PlanItem]:
    """Pair list items with bib entries by DOI, arXiv id, then title words. Never by item number."""
    matched: dict[str, PlanItem] = {}
    for key, e in bib.items():
        doi, eprint = e.get("doi", "").lower(), e.get("eprint", "")
        tw = title_words(bib_title(e))
        best, score = None, 0.0
        for it in plan:
            if doi and doi in it.dois or eprint and eprint in it.arxiv:
                best, score = it, 2.0
                break
            if len(tw) >= 3:
                s = len(tw & title_words(it.text)) / len(tw)
                if s > score:
                    best, score = it, s
        if best and score >= 0.8:
            matched[key] = best
            best.key = key
    return matched


def qc_verdict(key: str) -> str:
    p = QC / f"{key}.md"
    m = re.search(r"\*\*QC: ([^*]+)\*\*", p.read_text(encoding="utf-8")) if p.exists() else None
    return m.group(1).strip() if m else "–"


def set_frontmatter(path: Path, key: str, value: str) -> bool:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return False
    lines = m.group(1).split("\n")
    new = f"{key}: {value}"
    for i, line in enumerate(lines):
        if re.match(rf"{key}:", line):
            if line == new:
                return False
            lines[i] = new
            break
    else:
        lines.append(new)
    path.write_text("---\n" + "\n".join(lines) + "\n---\n" + text[m.end():], encoding="utf-8")
    return True


def cmd_plan(bib: dict, res: Result, sync: bool = False) -> None:
    if not SEZNAM.exists():
        res.add("ERROR", "NO_PLAN", "chybí literature/seznam.md")
        return
    plan = read_plan()
    matched = match_plan(plan, bib)
    notes = {p.stem: p for p in SOURCES.glob("*.md")}
    synced = []
    for key, it in matched.items():
        if key not in notes:
            continue
        fm = frontmatter(notes[key].read_text(encoding="utf-8"))
        want = {"uroven": it.level}
        have = {"uroven": str(fm.get("uroven", ""))}
        for k in want:
            if want[k] != have[k]:
                if sync and set_frontmatter(notes[key], k, want[k]):
                    synced.append(f"{key}.{k}")
                elif not sync:
                    res.add("WARN", "PLAN_DRIFT", f"{key}: {k} v poznámce {have[k] or '–'}, v seznamu {want[k]} "
                            "(`litqc.py plan --sync`)")
    if synced:
        res.add("INFO", "PLAN_SYNCED", "aktualizováno: " + ", ".join(synced))
    for key in sorted(set(bib) - set(matched)):
        res.add("WARN", "NOT_IN_PLAN", f"{key}: je v Zoteru, ale ne v seznamu (vyřazeno? jinak doplň do seznamu DOI)")

    def state(it: PlanItem) -> str:
        if not it.key:
            return "chybí v Zoteru"
        if it.key not in notes:
            return "k ingestu"
        fm = frontmatter(notes[it.key].read_text(encoding="utf-8"))
        done = fm.get("status") == "confirmed" and fm.get("verified") == "true"
        return (f"{'✅ ověřeno' if done else fm.get('status', '?')} · čteno: {fm.get('precteno', '–')} "
                f"· QC {qc_verdict(it.key)}")

    def read_state(it: PlanItem) -> str:
        return frontmatter(notes[it.key].read_text(encoding="utf-8")).get("precteno", "ne") \
            if it.key in notes else "ne"

    states = {it.no: state(it) for it in plan}
    reads = {it.no: read_state(it) for it in plan}
    rows = []
    for lvl, name in LEVEL_NAMES.items():
        its = [it for it in plan if it.level == lvl]
        rows.append(f"| {name} | {len(its)} | {sum(bool(it.key) for it in its)} | "
                    f"{sum(it.key in notes for it in its if it.key)} | "
                    f"{sum(reads[it.no] not in ('ne', 'abstrakt') for it in its)} | "
                    f"{sum(reads[it.no] == 'cele' for it in its)} | "
                    f"{sum(states[it.no].startswith('✅') for it in its)} |")
    res.tables.append("### Stav podle úrovní\n\n"
                      "| úroveň | položek | v Zoteru | poznámka | čteno víc než abstrakt | čteno celé | ověřeno |\n"
                      "|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    for lvl, name in LEVEL_NAMES.items():
        its = [it for it in plan if it.level == lvl]
        if not its:
            continue
        lines = [f"| {it.no} | {it.text[:90].replace('|', '/')}… | "
                 f"{'[[' + it.key + ']]' if it.key in notes else (it.key or '–')} | {states[it.no]} |" for it in its]
        res.tables.append(f"### Úroveň {name} ({len(its)})\n\n| č. | položka | citekey | stav |\n"
                          "|---|---|---|---|\n" + "\n".join(lines) + "\n")


# ---------------------------------------------------------------- metadata (Crossref + Semantic Scholar / OpenAlex)

CACHE = QC / ".cache"
_last_request = [0.0]


def http_json(url: str) -> dict | None:
    import time
    import urllib.error
    import urllib.request
    CACHE.mkdir(parents=True, exist_ok=True)
    cp = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".json")
    if cp.exists():
        return json.loads(cp.read_text(encoding="utf-8"))
    time.sleep(max(0.0, 1.0 - (time.time() - _last_request[0])))        # be polite: max 1 request/s
    _last_request[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "litqc/1.0 (thesis literature check)"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:                   # rate limit / outage: wait, never cache
                time.sleep(3 * (attempt + 1))
                continue
            data = {"_http_error": e.code}
            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            print(f"[meta] {url}: {e}", file=sys.stderr)
            return None
    else:
        return None
    cp.write_text(json.dumps(data), encoding="utf-8")
    return data


def norm_pages(p: str | None) -> str:
    return re.sub(r"\s*[-–—]+\s*", "-", p or "").strip()


def similarity(a: str, b: str) -> float:
    wa, wb = title_words(a), title_words(b)
    return len(wa & wb) / max(len(wa | wb), 1)


def crossref_record(doi: str) -> dict | None:
    from urllib.parse import quote
    d = http_json(f"https://api.crossref.org/works/{quote(doi)}")
    return d.get("message") if d and "message" in d else d


def s2_hits(title: str) -> list[dict]:
    """Semantic Scholar best title match: carries venue, DBLP key, arXiv id and pages."""
    from urllib.parse import quote
    d = http_json("https://api.semanticscholar.org/graph/v1/paper/search/match?fields=title,year,venue,externalIds,"
                  f"publicationVenue,journal&query={quote(title)}")
    out = []
    for w in (d or {}).get("data", []):
        if similarity(w.get("title") or "", title) < 0.85:
            continue
        pv = w.get("publicationVenue") or {}
        venue = pv.get("name") or w.get("venue") or ""
        ext = w.get("externalIds") or {}
        out.append({"title": w.get("title"), "year": str(w.get("year") or ""),
                    "pages": norm_pages((w.get("journal") or {}).get("pages")), "doi": ext.get("DOI", ""),
                    "venue": venue, "dblp": ext.get("DBLP", ""),
                    "preprint": not venue or bool(re.search(r"arxiv|corr", venue, re.I))})
    return out


def openalex_hits(title: str) -> list[dict]:
    """OpenAlex title search (DBLP's API sits behind an anti-bot wall). Returns normalized records."""
    from urllib.parse import quote
    q = re.sub(r"[^\w\s-]", " ", re.sub(r"\([^)]*\)", " ", title))   # drop "(long-version)" etc.
    d = http_json("https://api.openalex.org/works?per-page=8&select=title,publication_year,doi,biblio,primary_location,type"
                  f"&filter=title.search:{quote(q)}")
    out = []
    for w in (d or {}).get("results", []):
        wt = w.get("title") or ""
        if similarity(wt, title) < 0.85 or re.match(r"(review|reviews?)\b", wt, re.I):
            continue
        src = ((w.get("primary_location") or {}).get("source") or {})
        venue = src.get("display_name") or ""
        b = w.get("biblio") or {}
        pages = f"{b['first_page']}-{b['last_page']}" if b.get("first_page") and b.get("last_page") else ""
        out.append({"title": w.get("title"), "year": str(w.get("publication_year") or ""), "pages": pages,
                    "doi": (w.get("doi") or "").replace("https://doi.org/", ""), "venue": venue,
                    "preprint": w.get("type") == "preprint" or src.get("type") == "repository"
                    or bool(re.search(r"arxiv|ssrn|research square", venue, re.I))})
    return out


def cmd_meta(bib: dict, res: Result, keys: list[str]) -> None:
    rows = []
    for key in keys or sorted(bib):
        e = bib[key]
        title, year, pages = bib_title(e), e.get("year", ""), norm_pages(e.get("pages"))
        doi = e.get("doi", "").strip()
        venue = e.get("journal") or e.get("booktitle") or ""
        preprint = bool(re.search(r"arxiv|corr", venue, re.I)) or (not venue and bool(e.get("eprint")))
        found = []
        if doi:
            cr = crossref_record(doi)
            if cr is None:
                res.add("WARN", "META_OFFLINE", f"{key}: Crossref nedostupný")
            elif "_http_error" in cr:
                res.add("ERROR", "DOI_INVALID", f"{key}: DOI {doi} v Crossref neexistuje (HTTP {cr['_http_error']})")
            else:
                found.append("Crossref")
                ct = " ".join((cr.get("title") or [""])[:1] + (cr.get("subtitle") or [])[:1])
                if similarity(ct, title) < 0.6:
                    res.add("ERROR", "DOI_MISMATCH", f"{key}: DOI vede na jiný článek: „{ct[:80]}“")
                cy = str(((cr.get("published") or cr.get("issued") or {}).get("date-parts") or [[None]])[0][0] or "")
                if cy and year and cy != year:
                    res.add("WARN", "META_YEAR", f"{key}: rok v Zoteru {year}, Crossref {cy}")
                cp = norm_pages(cr.get("page"))
                if cp and pages and cp != pages:
                    res.add("WARN", "META_PAGES", f"{key}: stránky v Zoteru {pages}, Crossref {cp}")
                for u in cr.get("updated-by", []) + cr.get("update-to", []):
                    if "retract" in str(u.get("type", "")).lower():
                        res.add("ERROR", "RETRACTED", f"{key}: článek byl stažen (retraction)")
        hits, src = (s2_hits(title), "Semantic Scholar") if title else ([], "")
        if title and not hits:
            hits, src = openalex_hits(title), "OpenAlex"
        if hits:
            found.append(src)
            published = sorted((h for h in hits if not h["preprint"]),
                               key=lambda h: -(bool(h["doi"]) + bool(h["pages"]) + bool(h["venue"])))
            best = (published or hits)[0]
            if not doi and best.get("doi") and not (best["doi"].lower().startswith("10.48550") and not preprint):
                # arXiv DOIs (10.48550) are only suggested for entries that are themselves preprints
                res.add("WARN", "META_NO_DOI", f"{key}: chybí DOI, {src} uvádí {best['doi']} ({best.get('venue')} "
                        f"{best.get('year')})")
            if preprint and any(h["venue"] for h in published):
                p0 = next(h for h in published if h["venue"])
                res.add("WARN", "PREPRINT_PUBLISHED", f"{key}: je preprint, existuje publikovaná verze "
                        f"{p0.get('venue')}" + (f", DOI {p0['doi']}" if p0.get("doi") else "")
                        + (f", DBLP {p0['dblp']}" if p0.get("dblp") else "")
                        + " – v Zoteru „Update to a published one“")
            if published and not doi:
                dp, dy = norm_pages(best.get("pages")), str(best.get("year", ""))
                if dp and pages and dp != pages:
                    res.add("WARN", "META_PAGES", f"{key}: stránky v Zoteru {pages}, {src} {dp}")
                if dy and year and dy != year:
                    res.add("WARN", "META_YEAR", f"{key}: rok v Zoteru {year}, {src} {dy}")
        if not venue and e.get("_type") not in ("book", "misc", "online", "dataset", "software"):
            res.add("WARN", "META_NO_VENUE", f"{key}: chybí journal/booktitle")
        if not found:
            res.add("WARN", "META_NOT_FOUND", f"{key}: nenalezeno v Crossref, Semantic Scholar ani OpenAlex – ověř ručně")
        rows.append(f"| {key} | {year or '–'} | {venue[:40] or '–'} | {pages or '–'} | {doi or '–'} | "
                    f"{', '.join(found) or '–'} |")
    res.tables.append("### Záznamy\n\n| citekey | rok | venue | stránky | DOI | ověřeno v |\n|---|---|---|---|---|---|\n"
                      + "\n".join(rows) + "\n")


# ---------------------------------------------------------------- report

def write_report(path: Path, title: str, res: Result, link: str | None = None) -> None:
    verdict = "FAIL" if res.errors else ("PASS s varováními" if res.warns else "PASS")
    lines = ["---", "type: qc", "generated: " + date.today().isoformat(), "---", "",
             "> Generováno `literature/tools/litqc.py`, needitovat ručně.", "",
             f"# {title}", ""]
    if link:
        lines += [f"Zdroj: [[{link}]]", ""]
    lines += [f"**QC: {verdict}** – {res.errors} chyb, {res.warns} varování", ""]
    if res.issues:
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        lines += ["| úroveň | kód | nález |", "|---|---|---|"]
        lines += [i.md() for i in sorted(res.issues, key=lambda i: order[i.level])] + [""]
    lines += res.tables
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_result(name: str, res: Result) -> None:
    print(f"== {name}: {res.errors} ERROR, {res.warns} WARN")
    for i in res.issues:
        if i.level != "INFO":
            print(f"  {i.level:5} {i.code:18} {i.msg}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["ocr", "fulltext", "stamp", "claims", "lint", "check", "plan", "meta"])
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--all", action="store_true", help="all keys that have a source note")
    ap.add_argument("--repair", action="store_true", help="replace BAD fulltext pages with OCR text")
    ap.add_argument("--force", action="store_true", help="re-run OCR even if cached")
    ap.add_argument("--sync", action="store_true", help="plan: write uroven from seznam.md into notes")
    a = ap.parse_args()

    QC.mkdir(exist_ok=True)
    bib = read_bib()
    keys = sorted(p.stem for p in SOURCES.glob("*.md")) if a.all else a.keys
    if a.cmd not in ("lint", "plan", "meta") and not keys:
        ap.error("give citekeys or --all")
    errors = 0

    if a.cmd == "ocr":
        for k in keys:
            print(cmd_ocr(k, bib, force=a.force) or f"{k}: no PDF")
    elif a.cmd == "stamp":
        for k in keys:
            cmd_stamp(k)
    elif a.cmd in ("fulltext", "claims", "check"):
        for k in keys:
            res = Result()
            if a.cmd in ("fulltext", "check"):
                cmd_fulltext(k, bib, res, repair=a.repair)
            if a.cmd in ("claims", "check"):
                cmd_claims(k, res)
            if a.cmd == "check":
                write_report(QC / f"{k}.md", f"QC {k}", res, link=k)
            print_result(k, res)
            errors += res.errors
    if a.cmd == "plan":
        res = Result()
        cmd_plan(bib, res, sync=a.sync)
        write_report(QC / "_plan.md", "Seznam literatury × Zotero × vault", res)
        print_result("plan", res)
        errors += res.errors
    if a.cmd == "meta":
        res = Result()
        cmd_meta(bib, res, keys)
        write_report(QC / "_metadata.md", "Metadata: Zotero × Crossref × Semantic Scholar/OpenAlex", res)
        print_result("meta", res)
        errors += res.errors
    if a.cmd in ("lint", "check"):
        res = Result()
        cmd_lint(bib, res)
        write_report(QC / "_vault.md", "QC celého vaultu", res)
        print_result("vault", res)
        errors += res.errors
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
