# Satelliti da Torino – 7 opzioni di design

Apri `index.html` (doppio clic) e scegli tra `opzione-1.html` … `opzione-7.html`.
Ogni opzione è un unico file HTML con i dati incorporati: funziona offline.

- `data/channels.json` – canali TV in chiaro / parzialmente in chiaro per satellite (fonte KingOfSat)
- `data/novita.json` – arrivi, uscite, chiusure, passaggi in chiaro/criptato (circa l'ultimo mese)
- `scraper/scrape.py` – riscarica i dati da it.kingofsat.net (`--offline` usa le pagine in `raw/`)
- `scraper/public_rules.py` – regole per riconoscere le emittenti pubbliche europee
- `build/build.py` – rigenera le 7 pagine e index.html; `build/test_shots.py` – test + screenshot

Aggiornare tutto:  `python3 scraper/scrape.py && python3 build/build.py`

Note: "PARZIALE" = canale in chiaro ma con codifica attiva in alcuni periodi/eventi, oppure
temporaneamente in chiaro. "Ricezione difficile" = trasmesso su fascio non diretto verso l'Italia
(es. fascio UK di Astra 28.2°E, fasci nordici di Thor/Astra 4.8°E, fasci turchi/mediorientali).
