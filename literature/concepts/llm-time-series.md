---
type: concept
aliases: [LLM for time series, LLMs and time series, LLM time series analysis, time series foundation models, LLM anomaly detection]
---

Použití velkých jazykových (a multimodálních) modelů na analýzu časových řad – predikci, klasifikaci nebo detekci anomálií – ať už přímo nad čísly v textu, nad grafem, nebo jako orchestrátor nad jinými metodami.

## Sources
- [[zhouCanLLMsUnderstand2025]] — C3–C6: řízené experimenty: LLM vidí anomálie lépe z obrázku než z textu, CoT nepomáhá, delší vstup výkon zhoršuje, modely se výrazně liší.
- [[liuElephantRoomReliable2024]] — C5: foundation modely silné na bodové anomálie, slabé na sekvenční; integrace LLM do detekce anomálií zatím neuspokojivá.

## Napětí
- [[liuElephantRoomReliable2024]] C5 vs. [[zhouCanLLMsUnderstand2025]] C7: Liu hodnotí integraci LLM (OFA, fine-tuning GPT) do detekce anomálií jako neuspokojivou, Zhou uvádí, že M-LLM s obrazovým vstupem v zero-shot překonávají Isolation Forest a prahování na syntetických bodových, rozsahových a trendových datech. Liší se metody (fine-tuned GPT vs. multimodální zero-shot), data (benchmark vs. syntetika) i metrika (VUS-PR vs. affinity F1).

## Související
- [[anomaly-detection]]
