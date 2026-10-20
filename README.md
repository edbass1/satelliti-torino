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

## Aggiornamento automatico (ogni 12 ore)
`.github/workflows/aggiorna.yml` gira alle 00:00 e 12:00 UTC (e a mano da "Actions → Run workflow"):
scarica i dati da KingOfSat (pause di 3 s tra le richieste, User-Agent da browser, 3 tentativi),
rigenera `data/`, `opzione-*.html`, `index.html` (= opzione 1) e fa commit solo se qualcosa è cambiato.
Se KingOfSat non risponde o i dati sembrano incompleti, lo scraper esce senza toccare i file e non c'è commit.

## Regole dei dati
- Solo canali TV **in chiaro** o **parzialmente in chiaro** (lo scraper verifica con `assert` che nessun canale solo criptato finisca nei dati).
- Novità: solo **entrate** e **uscite** di canali in chiaro (FTA puro). Esclusi cambi di codifica, cambi di frequenza,
  rientri dopo interruzioni e canali parzialmente in chiaro.

## Continenti e bandiere (versione Minimal)
Mappa paese → continente in `build/countries.py`: Turchia, Russia e Cipro → Europa; Caucaso, Kazakistan,
Medio Oriente e Golfo → Asia; Nord Africa ed Egitto → Africa; paese mancante → chip "Internaz. / n.d.".
Bandiere da flag-icons (MIT) in `build/flags/` (SVG, o PNG 48×36 per le bandiere con stemmi complessi),
incorporate solo per i paesi presenti nei dati. `build/make_flags.py` le rigenera.
