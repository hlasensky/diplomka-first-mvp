---
type: concept
aliases: [LLM for time series, LLMs and time series, LLM time series analysis, time series foundation models, LLM anomaly detection]
---

Použití velkých jazykových (a multimodálních) modelů na analýzu časových řad – predikci, klasifikaci nebo detekci anomálií – ať už přímo nad čísly v textu, nad grafem, nebo jako orchestrátor nad jinými metodami.

## Sources
- [[zhouCanLLMsUnderstand2025]] — C3–C6: řízené experimenty: LLM vidí anomálie lépe z obrázku než z textu, CoT nepomáhá, delší vstup výkon zhoršuje, modely se výrazně liší.
- [[liuElephantRoomReliable2024]] — C5: foundation modely silné na bodové anomálie, slabé na sekvenční; integrace LLM do detekce anomálií zatím neuspokojivá.
- [[alnegheimishLargeLanguageModels2024]] — C2–C4, C6–C7: SigLLM převádí řadu na text a zkouší zero-shot detekci anomálií dvěma cestami; detekce z předpovědi LLM (DETECTOR, F1 0,525) je výrazně lepší než přímý dotaz (PROMPTER), ale za hlubokým učením (AER) zaostává zhruba o 30 %.
- [[wangChartInsighterApproachMitigating2025]] — C2, C3: LLM při shrnutí grafů časových řad nejčastěji chybují ve směru trendu a vynechávají detaily; C4: řadu proto předem segmentuje a statistiky počítá externí modul, ne LLM.

## Napětí
- [[liuElephantRoomReliable2024]] C5 vs. [[zhouCanLLMsUnderstand2025]] C7: Liu hodnotí integraci LLM (OFA, fine-tuning GPT) do detekce anomálií jako neuspokojivou, Zhou uvádí, že M-LLM s obrazovým vstupem v zero-shot překonávají Isolation Forest a prahování na syntetických bodových, rozsahových a trendových datech. Liší se metody (fine-tuned GPT vs. multimodální zero-shot), data (benchmark vs. syntetika) i metrika (VUS-PR vs. affinity F1).
- [[zhouCanLLMsUnderstand2025]] C7 vs. [[alnegheimishLargeLanguageModels2024]] C7: Zhou uvádí, že zero-shot M-LLM s obrazovým vstupem překonávají Isolation Forest a prahování; u Alnegheimish textové LLM (GPT-3.5, Mistral-7B) zaostávají za ARIMA i za modely hlubokého učení (AER o 30 %) a předčí jen klouzavý průměr a Anomaly Transformer. Liší se vstup (obrázek vs. text), data (syntetika vs. NASA/Yahoo/NAB), baseline i metrika (affinity F1 vs. F1 se započtením částečné detekce).
- [[zhouCanLLMsUnderstand2025]] C4 vs. [[wangChartInsighterApproachMitigating2025]] C8: Zhou uvádí, že M-LLM najdou anomálie mnohem lépe z obrázku řady než z čísel v textu; Wang volí jako vstup surová data a Vega-Lite specifikaci s odkazem na výzkum, podle něhož podkladová data dávají efektivnější shrnutí než jiné formy vstupu (obrázek jen jako budoucí práce). Liší se úloha (detekce anomálií vs. shrnutí grafu) i to, že Wang tvrzení přebírá z citované literatury a sám ho netestuje.

## Související
- [[anomaly-detection]]
