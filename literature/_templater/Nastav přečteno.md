<%*
// Nastaví `precteno` v poznámce zdroje výběrem ze seznamu.
// Cíl: aktuální poznámka ze sources/, jinak naposledy otevřená poznámka ze sources/.
// Když Templater skript spustí jako „novou poznámku ze šablony“, prázdný soubor po sobě smaže.
const values = ["ne", "abstrakt", "uvod-zaver", "prolet", "cele"];
const labels = [
  "ne – nečteno",
  "abstrakt – jen abstrakt",
  "uvod-zaver – úvod a závěr",
  "prolet – proletěno celé (nadpisy, obrázky, výsledky)",
  "cele – přečteno celé",
];
const self = tp.config.target_file;
const createdNew = tp.config.run_mode === 0;          // 0 = CreateNewFromTemplate
const isSource = (f) => f && f.path.startsWith("sources/") && f.extension === "md" && f.path !== self.path;

let target = isSource(tp.config.target_file) ? tp.config.target_file : null;
if (!target) {
  const active = app.workspace.getActiveFile();
  if (isSource(active)) target = active;
}
if (!target) {
  const recent = app.workspace.getLastOpenFiles().find((p) => p.startsWith("sources/") && p !== self.path);
  if (recent) target = app.vault.getAbstractFileByPath(recent);
}

if (!target) {
  new Notice("Nastav přečteno: otevři nejdřív poznámku ze sources/.");
} else {
  const current = app.metadataCache.getFileCache(target)?.frontmatter?.precteno;
  const choice = await tp.system.suggester(labels, values, false,
    `${target.basename} – přečteno (teď: ${current ?? "–"})`);
  if (choice) {
    await app.fileManager.processFrontMatter(target, (fm) => { fm.precteno = choice; });
    new Notice(`${target.basename}: precteno = ${choice}`);
  }
}

if (createdNew) {
  // the empty note Templater just created: remove it once Templater has finished opening it
  setTimeout(async () => {
    const f = app.vault.getAbstractFileByPath(self.path);
    if (f && (await app.vault.read(f)).trim() === "") await app.vault.trash(f, true);
    if (target) await app.workspace.getLeaf(false).openFile(target);
  }, 500);
}
-%>
