#!/usr/bin/env python3
"""Scraper KingOfSat -> channels.json / novita.json
channels.json: canali TV in chiaro / parzialmente in chiaro.
novita.json:   SOLO entrate e uscite di canali in chiaro (FTA puro): niente cambi di codifica, rinomini,
               cambi di frequenza, rientri dopo interruzioni o canali parzialmente in chiaro.
Se KingOfSat non risponde o i dati sembrano incompleti, esce con codice 2 SENZA toccare i file in data/.
Uso:  python3 scrape.py            (scarica di nuovo le pagine e rigenera i dati)
      python3 scrape.py --offline  (usa le pagine già scaricate in ../raw)
"""
import re, json, html, os, sys, time, datetime, collections, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from public_rules import classify
BASE = 'https://it.kingofsat.net/'
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, '..', 'raw'); DATA = os.path.join(HERE, '..', 'data')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'

# Satelliti ricevibili da Torino (45.07N 7.69E) con copertura in chiaro significativa
SATS = [
 ('42E',  'Türksat 42°E',   'Türksat 3A/4A/5B/6A', 42.0),
 ('39E',  'Hellas Sat 39°E','Hellas Sat 3/4', 39.0),
 ('28.2E','Astra 28.2°E',   'Astra 2E/2F/2G', 28.2),
 ('23.5E','Astra 23.5°E',   'Astra 3B/3C', 23.5),
 ('19.2E','Astra 19.2°E',   'Astra 1M/1N/1P', 19.2),
 ('16E',  'Eutelsat 16°E',  'Eutelsat 16A/16D', 16.0),
 ('13E',  'Hotbird 13°E',   'Hot Bird 13F/13G', 13.0),
 ('9E',   'Eutelsat 9°E',   'Eutelsat 9B', 9.0),
 ('7E',   'Eutelsat 7°E',   'Eutelsat 7C', 7.0),
 ('4.8E', 'Astra 4.8°E',    'Astra 4A / SES 5', 4.8),
 ('0.8W', 'Thor 0.8°W',     'Thor 5/6/7 · Intelsat 10-02', -0.8),
 ('5W',   'Eutelsat 5°W',   'Eutelsat 5 West B', -5.0),
 ('7W',   'Nilesat 7°W',    'Nilesat / Eutelsat 7 West A', -7.0),
 ('30W',  'Hispasat 30°W',  'Hispasat 30W-5/30W-6', -30.0),
]
# fasci (beam) non puntati sull'Italia: ricezione da Torino difficile/impossibile con parabole normali
HARD_BEAMS = {'28.2E':{'U.K.'}, '0.8W':{'K1 Nordic','Spot 1','Spot 2','Spot 3'}, '4.8E':{'Nordic','BSS Nordic'},
              '7E':{'Eastern'}, '42E':{'East','Turkey'}, '39E':{'Middle-East'}, '7W':{'Middle-East'}}

GENRE = {'General':'Generalista','News':'Notizie','Sport':'Sport','Movies':'Film','Music':'Musica','Kids':'Bambini',
 'Documentary':'Documentari','Religious':'Religione','Shopping':'Televendite','Entertainment':'Intrattenimento',
 'Lifestyle':'Lifestyle','Culture':'Cultura','Various':'Varie','Adult':'Adulti','Regional':'Regionale',
 'Education':'Educazione','Series':'Serie TV','Fashion':'Moda','Travel':'Viaggi','Cooking':'Cucina','Business':'Economia',
 'Parliament':'Istituzionale','Weather':'Meteo','Science':'Scienza','Comedy':'Commedia','Nature':'Natura','History':'Storia',
 'Health':'Salute','Gaming':'Gaming','Erotic':'Adulti','Local':'Locale','Information':'Informazione','Animation':'Animazione',
 'Hunting':'Caccia e pesca','Fishing':'Caccia e pesca','Cars':'Motori','Automotive':'Motori','Classical Music':'Musica','Women':'Donna','Men':'Uomo',
 'Arts':'Arte','Teleshopping':'Televendite','Children':'Bambini','Youth':'Giovani','Movies & Series':'Film','Dating':'Incontri','Documentaries':'Documentari','Cultural':'Cultura','Presentations':'Presentazioni','Politics':'Politica e istituzioni','Racing':'Ippica e corse','Game':'Giochi','Talk shows':'Talk show','Chat':'Chat','Real TV':'Reality','Theater':'Teatro'}
SKIPLANG = {'audio originale','Audio Description','AC3 (Dolby Digital 5.1)','Dolby Digital Plus','non definito','mis','und','Multilingue'}

class FetchError(Exception): pass
DELAY = 3  # secondi tra una richiesta e l'altra (cortesia verso KingOfSat)
def fetch(name, url):
    p = os.path.join(RAW, name)
    if '--offline' not in sys.argv:
        last = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'it-IT,it;q=0.9'})
                data = urllib.request.urlopen(req, timeout=60).read()
                if len(data) < 2000: raise FetchError('risposta troppo corta (%d byte)' % len(data))
                open(p, 'wb').write(data); time.sleep(DELAY)
                break
            except Exception as e:
                last = e; time.sleep(DELAY * (attempt + 2))
        else:
            raise FetchError('%s: %s' % (url, last))
    return open(p, encoding='utf-8', errors='replace').read()

def txt(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\xa0',' ').strip()
import unicodedata
def norm(n):
    n = ''.join(ch for ch in unicodedata.normalize('NFKD', n.lower()) if not unicodedata.combining(ch))
    n = re.sub(r'\b(uhd|4k|hd|fhd|sd|hevc|h\.?265|8k)\b', ' ', n)
    n = re.sub(r'[^a-z0-9àèéìòùäöüçñşğıé]+', ' ', n)
    return ' '.join(n.split())

MS_RANK = {'': 0, 'def': 1, 'mis': 2, 't2mi': 3}   # 0 = più facile da ricevere
def stream_info(part):
    """Analizza un transponder KingOfSat: tipo di flusso, stream (ISI), PLS, blocchi T2-MI.
    Restituisce (info_transponder, lista di (chunk_html, isi, t2mi))."""
    toks = re.split(r'(<table class="frq kos-stream-summary">.*?</table>)', part, flags=re.S)
    head = None; streams = {}; chunks = []; isi = None; t2 = False
    for tk in toks:
        if tk.startswith('<table class="frq kos-stream-summary">'):
            t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' | ', tk)))
            idt = re.search(r'NID (\d+) - TSID (\d+)', t)
            m = re.search(r'\|\s*Stream (\d+)\s*\|', t)
            if m:
                isi = int(m.group(1)); t2 = False; streams[isi] = idt.groups() if idt else None
            elif 'T2-MI' in t: t2 = True
            elif head is None and 'Stream' in t:
                head = dict(tipo=t, mis=' - MIS - ' in t, id=idt.groups() if idt else None)
        else:
            chunks.append((tk, isi, t2))
    pls = re.search(r'PLS: ([^<]+)<', part)
    pls = pls.group(1).strip() if pls else ''
    head = head or dict(tipo='', mis=False, id=None)
    mis = head['mis'] or len(streams) >= 2
    default = None
    if mis and streams and head['id']:
        low = min(streams)
        if streams[low] == head['id']: default = low   # stream che KingOfSat riceve come flusso principale = ISI più basso
    return dict(mis=mis, pls=pls, pls_default=pls in ('', 'Root+1', 'Gold+0'), default=default, n=len(streams)), chunks

def ms_class(ti, isi, t2):
    """'' = normale, 'def' = multistream ma flusso principale, 'mis' = serve tuner multistream/PLS, 't2mi' = T2-MI"""
    if t2: return 't2mi'
    if not ti['pls_default']: return 'mis'
    if not ti['mis']: return ''
    if isi is not None and ti['default'] is not None and isi == ti['default']: return 'def'
    return 'mis'

def parse_pos(pos, s, tempfta_ids):
    out = {}
    hard = HARD_BEAMS.get(pos, set())
    # blocchi: header frequenza (beam) seguito da tabella canali
    parts = re.split(r'(<table class="frequencies-table frq kos-frequency-header)', s)
    beam = ''
    for part in parts:
        m = re.search(r'href="beams\.php\?[^"]*">([^<]+)</a>', part)
        if m and 'frequency-row' in part[:400]: beam = html.unescape(m.group(1))
        ti, chunks = stream_info(part)
        rows = [(cid, r, isi, t2) for ch_, isi, t2 in chunks for cid, r in re.findall(r'<tr data-channel-id="(\d*)">(.*?)</tr>', ch_, re.S)]
        for cid, r, isi, t2 in rows:
            vrd = re.search(r'<td class="vrd[^"]*">(.*?)</td>', r, re.S)
            if not vrd or not re.search(r'zap\.gif|tv\.gif', vrd.group(1)): continue  # solo TV
            name = txt(re.search(r'<td class="ch">(.*?)</td>', r, re.S).group(1))
            if not name: continue
            parts_n = re.split(r'\s{3,}', name); name = parts_n[0].strip(); nota = ' '.join(dict.fromkeys(parts_n[1:])).strip()
            for a_, b_ in (('Version pour la Suisse','versione per la Svizzera'),('Part-time','a orari'),('Daytime','solo di giorno'),('Nights','solo di notte'),('Sundays','domenica'),('Saturdays','sabato'),('CET','(ora italiana)')): nota = nota.replace(a_, b_)
            g = lambda c: txt((re.search(r'<td class="[^"]*\b%s">(.*?)</td>' % c, r, re.S) or [None,''])[1] if re.search(r'<td class="[^"]*\b%s">(.*?)</td>' % c, r, re.S) else '')
            enc_m = re.search(r'<span class="encryption-label">(.*?)</span>', r, re.S)
            enc = [x.strip() for x in html.unescape(re.sub(r'<br\s*/?>', '|', enc_m.group(1))).split('|')] if enc_m else []
            enc = [e for e in enc if e]
            fta = 'In chiaro - FTA' in enc
            cas = [e for e in enc if e != 'In chiaro - FTA']
            if not fta: continue
            status = 'parziale' if (cas or cid in tempfta_ids) else 'chiaro'
            res = 'UHD' if 'ultrahd.gif' in r else ('HD' if '/hd.gif' in r else 'SD')
            audio = re.search(r'<td class="audio[^"]*">(.*?)</td>', r, re.S)
            langs = []
            if audio:
                for t in re.findall(r'<a title="([^"]+)">\s*<font', audio.group(1)):
                    t = html.unescape(t)
                    if t not in SKIPLANG and t not in langs: langs.append(t)
            pays = g('pays'); genre = g('genre')
            pk = re.findall(r'class="bq"[^>]*>([^<]+)</a>', r)
            site = re.search(r'HREF="(https?://[^"]+)"', r)
            upd = re.search(r'(\d{4}-\d\d-\d\d)', r)
            rec = 'difficile' if beam in hard else 'buona'
            c = dict(id=cid, nome=name, key=norm(name), paese=pays if pays and pays!='non definito' else '',
                     genere=GENRE.get(genre, genre) if genre else '', lingue=langs, ris=res, stato=status,
                     cas=cas, bouquet=[html.unescape(x) for x in pk], sito=site.group(1) if site else '',
                     agg=upd.group(1) if upd else '', ricezione=rec, nota=nota)
            c['ms'] = ms_class(ti, isi, t2); c['isi'] = isi if (ti['mis'] or t2) else None
            c['pls'] = '' if ti['pls_default'] else ti['pls']
            c['pubblico'] = classify(name, c['paese'])
            k = (c['nome'].lower())
            if k in out:  # stesso canale su più frequenze: tieni il "migliore"
                o = out[k]
                if o['stato']=='parziale' and c['stato']=='chiaro': o['stato']='chiaro'; o['cas']=[]
                if o['ricezione']=='difficile' and rec=='buona': o['ricezione']='buona'
                if MS_RANK[c['ms']] < MS_RANK[o['ms']]: o['ms'], o['isi'], o['pls'] = c['ms'], c['isi'], c['pls']
                for l in langs:
                    if l not in o['lingue']: o['lingue'].append(l)
            else: out[k] = c
    return list(out.values())

DAYS = r'(?:Lunedì|Martedì|Mercoledì|Giovedì|Venerdì|Sabato|Domenica)'
MONTHS = {m:i+1 for i,m in enumerate('gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'.split())}
def parse_news(pos, s):
    ev = []
    t = re.sub(r'\s+', ' ', s)
    i = t.find('<h4>&nbsp;<img src="/tv.gif"')
    if i < 0: return ev
    t = t[i:t.find('Archivio News')] if 'Archivio News' in t else t[i:]
    t = re.sub(r'<p>', '\n', t); t = re.sub(r'<h4[^>]*>', '\n@@DATE ', t); t = re.sub(r'<h5[^>]*>', '\n@@SAT ', t)
    t = re.sub(r'</h[45]>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    date = None; sat = ''
    for line in t.split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('@@DATE'):
            m = re.search(DAYS + r' (\d+) (\w+) (\d{4})', line)
            if m: date = '%s-%02d-%02d' % (m.group(3), MONTHS[m.group(2).lower()], int(m.group(1)))
            continue
        if line.startswith('@@SAT'): sat = line[6:].strip(); continue
        if not date: continue
        line = re.sub(r'^\(\d\dh\d\d\)\s*', '', line)
        bq = ''
        mm = re.match(r'^([^:]{2,80}?):\s+(?=\S)', line)
        body = line
        if mm and not re.search(r'Nuova frequenza|Un nuovo canale', mm.group(1)) and 'MHz' not in mm.group(1):
            bq = mm.group(1); body = line[mm.end():]
        tipo = nome = None; paese = ''
        fta_txt = 'In chiaro - FTA' in body
        partial = bool(re.search(r'In chiaro - FTA\s*&|&\s*In chiaro - FTA', body))
        m = re.match(r'Un nuovo canale in DVB-S2? : (.+?) \(([^)]*)\), su', body)
        if m: tipo, nome, paese = 'arrivo', m.group(1), m.group(2)
        if not tipo:
            m = re.match(r'Nuova frequenza per (.+?): \d', body)
            if m: tipo, nome = 'nuova_freq', m.group(1)
        if not tipo:
            m = re.match(r'(.+?) ha lasciato \d', body)
            if m: tipo, nome = ('chiuso' if 'non è più trasmesso' in body else 'uscita'), m.group(1)
        if not tipo:
            m = re.match(r'(.+?)(?: \(([^)]*)\))? è ora trasmesso liberamente', body)
            if m: tipo, nome, paese = 'ora_chiaro', m.group(1), m.group(2) or ''; fta_txt = True
        if not tipo:
            m = re.match(r'(.+?)(?: \(([^)]*)\))? è ora codificato', body)
            if m: tipo, nome, paese = 'ora_criptato', m.group(1), m.group(2) or ''
        if not tipo:
            m = re.match(r'(.+?) è tornato su', body)
            if m: tipo, nome = 'tornato', m.group(1)
        if not tipo:
            m = re.match(r'(.+?) su DVB-S2? \d', body)
            if m: tipo, nome = 'arrivo', m.group(1)
        if not tipo: continue
        res = 'UHD' if ('4K' in nome or 'UHD' in nome) else ('HD' if re.search(r'\bHD\b', nome) else '')
        ev.append(dict(data=date, pos=pos, satellite=sat.split(',')[0], tipo=tipo, nome=nome.strip(), paese=paese,
                       bouquet=bq, fta=fta_txt, partial=partial, ris=res, key=norm(nome)))
    return ev

def novita_pos(pos, ch, fta_news, all_news):
    """Solo ENTRATE e USCITE di canali in chiaro (FTA puro)."""
    def d(x): return datetime.date.fromisoformat(x)
    stato = {c['key']: c['stato'] for c in ch}
    cand, seen = [], set()
    # pagina news "solo in chiaro" + eventuali nuovi canali FTA presenti solo nella pagina news completa
    for e in fta_news + [e for e in all_news if e['tipo'] in ('arrivo', 'nuova_freq') and e['fta']]:
        sig = (e['data'], e['tipo'], e['nome'])
        if sig not in seen: seen.add(sig); cand.append(e)
    out = []
    for e in cand:
        t = e['tipo']
        if t not in ('arrivo', 'nuova_freq', 'uscita', 'chiuso'): continue      # niente codifiche / rientri / altro
        if e['partial'] or stato.get(e['key']) == 'parziale': continue          # niente parzialmente in chiaro
        if t in ('arrivo', 'nuova_freq') and not e['fta'] and e not in fta_news: continue
        near = lambda types: any(o['tipo'] in types and o['key'] == e['key'] and abs((d(o['data']) - d(e['data'])).days) <= 3 for o in cand)
        if t in ('uscita', 'nuova_freq') and near({'nuova_freq', 'tornato'} if t == 'uscita' else {'uscita'}): continue  # cambio frequenza / interruzione
        if t == 'uscita' and near({'arrivo'}) and stato.get(e['key']) == 'chiaro': continue
        tipo = 'entrata' if t in ('arrivo', 'nuova_freq') else 'uscita'
        if tipo == 'entrata' and e['key'] not in stato and d(e['data']) < datetime.date.today() - datetime.timedelta(days=3):
            pass  # entrato e poi sparito: l'uscita (se FTA) compare come evento separato
        out.append(dict(data=e['data'], pos=pos, satellite=e['satellite'], tipo=tipo, chiuso=(t == 'chiuso'), nome=e['nome'],
                        paese=e['paese'] or next((c['paese'] for c in ch if c['key'] == e['key'] and c['paese']), ''),
                        bouquet=e['bouquet'], ris=e['ris'], key=e['key'], in_lista=e['key'] in stato))
    return out

def main():
    os.makedirs(RAW, exist_ok=True); os.makedirs(DATA, exist_ok=True)
    tf = fetch('kos_tempfta.html', BASE + 'tempfta')
    tempfta_ids = set(re.findall(r'<tr data-channel-id="(\d+)"', tf))
    channels = []; sats = []; events = []
    for pos, label, sats_names, lon in SATS:
        s = fetch('kos_pos-%s.html' % pos, BASE + 'pos-' + pos)
        ch = parse_pos(pos, s, tempfta_ids)
        for c in ch: c['pos'] = pos
        channels += ch
        sats.append(dict(pos=pos, nome=label, satelliti=sats_names, lon=lon, canali=len(ch),
                         hd=sum(c['ris']=='HD' for c in ch), uhd=sum(c['ris']=='UHD' for c in ch),
                         parziali=sum(c['stato']=='parziale' for c in ch)))
        fta_news = parse_news(pos, fetch('news_%s.html' % pos, BASE + 'news.php?filtre=Clear&pos=' + pos))
        all_news = parse_news(pos, fetch('newsall_%s.html' % pos, BASE + 'news' + pos))
        events += novita_pos(pos, ch, fta_news, all_news)
    # garanzia: SOLO canali in chiaro o parzialmente in chiaro (nessun canale solo criptato)
    for c in channels:
        assert c['stato'] in ('chiaro', 'parziale'), c
        assert c['stato'] == 'parziale' or not c['cas'], c
        assert c['ms'] in MS_RANK, c
    for e in events:
        assert e['tipo'] in ('entrata', 'uscita'), e
    # controlli di sanità: se KingOfSat ha restituito pagine vuote/incomplete non sovrascrivere i dati
    prev = {}
    try:
        old = json.load(open(os.path.join(DATA, 'channels.json')))
        prev = {x['pos']: x['canali'] for x in old['satelliti']}
    except Exception: old = None
    bad = [x['pos'] for x in sats if x['canali'] == 0 or (prev.get(x['pos'], 0) >= 20 and x['canali'] < prev[x['pos']] * 0.5)]
    if bad or len(channels) < 500:
        print('ERRORE: dati sospetti (posizioni %s, totale %d): file in data/ NON modificati' % (bad, len(channels)), file=sys.stderr)
        sys.exit(2)
    events.sort(key=lambda e: e['data'], reverse=True)
    try:
        from zoneinfo import ZoneInfo
        now = datetime.datetime.now(ZoneInfo('Europe/Rome')).strftime('%Y-%m-%d %H:%M')
    except Exception:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # se i contenuti non sono cambiati (o si lavora --offline) si conserva la data precedente: nessun commit inutile
    if old is not None:
        try:
            old_ev = json.load(open(os.path.join(DATA, 'novita.json')))['eventi']
            if '--offline' in sys.argv or (old['canali'] == channels and old['satelliti'] == sats and old_ev == events):
                now = old['meta'].get('aggiornato', now)
        except Exception: pass
    meta = dict(fonte='KingOfSat (it.kingofsat.net)', aggiornato=now, luogo='Torino (45.07°N, 7.69°E)', fuso='Europe/Rome')
    json.dump(dict(meta=meta, satelliti=sats, canali=channels), open(os.path.join(DATA, 'channels.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(dict(meta=meta, eventi=events), open(os.path.join(DATA, 'novita.json'), 'w'), ensure_ascii=False, indent=1)
    for s_ in sats: print(s_)
    print('canali', len(channels), 'eventi', len(events), collections.Counter(e['tipo'] for e in events))

if __name__ == '__main__':
    try: main()
    except FetchError as e:
        print('ERRORE: KingOfSat non raggiungibile (%s): file in data/ NON modificati' % e, file=sys.stderr); sys.exit(2)
