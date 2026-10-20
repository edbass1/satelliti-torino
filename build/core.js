/* Core comune a tutte le 7 opzioni: dati, filtri, ricerca, viste. */
(function(){
'use strict';
const D = window.SATDATA;
const SKIN = window.SKIN || {};
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fold = s => String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const SAT = {}; D.sats.forEach(s => SAT[s.pos] = s);
const TORINO = {lat:45.07, lon:7.69};
function point(lonSat){ // azimut/elevazione da Torino
  const r = Math.PI/180, la = TORINO.lat*r, dl = (lonSat - TORINO.lon)*r, R = 6378.137/42164.2;
  const cosg = Math.cos(la)*Math.cos(dl);
  const el = Math.atan((cosg - R)/Math.sqrt(1 - cosg*cosg))/r;
  let az = 180 - Math.atan(Math.tan(dl)/Math.sin(la))/r;
  return {az: Math.round(az*10)/10, el: Math.round(el*10)/10};
}
D.sats.forEach(s => Object.assign(s, point(s.lon)));
// canali: espansione formato compatto
const CH = D.ch.map((a,i) => ({i, n:a[0], p:a[1], c:a[2], g:a[3]||'', l:a[4]||[], r:a[5], s:a[6], hard:!!a[7], o:a[8]||'', pub:a[9]||null, k:a[10], b:a[11]||''}));
CH.forEach(c => c.f = fold(c.n + ' ' + c.c + ' ' + c.g + ' ' + c.l.join(' ') + ' ' + c.b + ' ' + (c.pub ? c.pub[0]+' '+c.pub[1] : '')));
// aggregazione per canale (stesso canale su più satelliti)
const AGG = new Map();
CH.forEach(c => { let a = AGG.get(c.k); if(!a){ a = {k:c.k, n:c.n, items:[]}; AGG.set(c.k, a);} a.items.push(c); if(c.n.length < a.n.length) a.n = c.n; });
AGG.forEach(a => { a.items.sort((x,y)=>SAT[y.p].lon - SAT[x.p].lon); const f=a.items[0]; a.c=f.c; a.g=f.g; a.pub=a.items.find(x=>x.pub)?.pub||null;
  a.l=[...new Set(a.items.flatMap(x=>x.l))]; a.r = a.items.some(x=>x.r==='UHD')?'UHD':a.items.some(x=>x.r==='HD')?'HD':'SD';
  a.s = a.items.some(x=>x.s===1)?1:2; a.hard = a.items.every(x=>x.hard); a.f = a.items.map(x=>x.f).join(' '); });
const GENRES = [...new Set(CH.map(c=>c.g).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'it'));
const LANGS = (()=>{const m={}; CH.forEach(c=>c.l.forEach(l=>m[l]=(m[l]||0)+1)); return Object.keys(m).sort((a,b)=>m[b]-m[a]);})();
const TYPES = {arrivo:['Nuovo arrivo','in'], tornato:['Tornato','in'], ora_chiaro:['Ora in chiaro','in'], uscita:['Uscito dal satellite','out'], chiuso:['Chiuso (non più in Europa)','out'], ora_criptato:['Ora criptato','out']};
const PUBC = [...new Set(CH.filter(c=>c.pub).map(c=>c.pub[0]))].sort((a,b)=>a.localeCompare(b,'it'));
const ADJ = {franc:'Francia',tedesc:'Germania',german:'Germania',ital:'Italia',spagn:'Spagna',ingles:'Regno Unito',britann:'Regno Unito',ingl:'Regno Unito',uk:'Regno Unito',austr:'Austria',svizz:'Svizzera',portog:'Portogallo',polac:'Polonia',ceco:'Repubblica Ceca',cechi:'Repubblica Ceca',ceca:'Repubblica Ceca',slovacc:'Slovacchia',ungher:'Ungheria',sloven:'Slovenia',croat:'Croazia',serb:'Serbia',bosn:'Bosnia ed Erzegovina',monten:'Montenegro',kosov:'Kosovo',alban:'Albania',grec:'Grecia',cipr:'Cipro',bulgar:'Bulgaria',romen:'Romania',rumen:'Romania',moldav:'Moldavia',ucrain:'Ucraina',turc:'Turchia',lituan:'Lituania',lussemb:'Lussemburgo',moneg:'Monaco',belg:'Paesi Bassi / Belgio',oland:'Paesi Bassi / Belgio',fiamming:'Paesi Bassi / Belgio',sammarin:'San Marino',vatican:'Vaticano',europe:'Unione Europea',ue:'Unione Europea',internaz:'Internazionale'};
const st = {view:'sat', sat:(D.sats.find(s=>s.pos==='13E')||D.sats[0]).pos, q:'', genre:'', lang:'', res:'', stato:'', hideHard:false, group:'genere', limit:240,
  pubSel:new Set(['Italia','Francia','Germania']), pubPart:true, nSat:'', nType:'', nDays:''};
const api = {st, D, SAT, CH, AGG, esc, setSat, setView, render, badgeSat, resBadge, statoBadge};
window.SATAPP = api;

function resBadge(r){ return r==='UHD' ? '<span class="bdg b-4k" title="Ultra HD 4K">4K</span>' : r==='HD' ? '<span class="bdg b-hd" title="Alta definizione">HD</span>' : '<span class="bdg b-sd" title="Definizione standard">SD</span>'; }
function statoBadge(s){ return s===2 ? '<span class="bdg b-part" title="Parzialmente in chiaro: in alcuni periodi/eventi può essere criptato (o è temporaneamente in chiaro)">PARZIALE</span>' : '<span class="bdg b-fta" title="In chiaro">IN CHIARO</span>'; }
function badgeSat(c, withRes){ const s=SAT[c.p]; return `<button class="sbdg${c.s===2?' part':''}${c.hard?' hard':''}" data-gosat="${c.p}" title="${esc(s.nome)}${c.s===2?' · parzialmente in chiaro':''}${c.hard?' · fascio non diretto sull\u2019Italia (ricezione difficile da Torino)':''}">${esc(s.nome.replace(/ \d.*$/,''))} <b>${esc(s.pos.replace('E','°E').replace('W','°W'))}</b>${withRes&&c.r!=='SD'?' <i>'+(c.r==='UHD'?'4K':'HD')+'</i>':''}${c.s===2?' <i>parz.</i>':''}</button>`; }
function initials(n){ const w = n.replace(/[^\p{L}\p{N} ]/gu,' ').split(/\s+/).filter(Boolean); return (w.length>1 ? w[0][0]+(/\d/.test(w[1][0])?w[1]:w[1][0]) : (w[0]||'?').slice(0,2)).toUpperCase().slice(0,3); }
function hue(s){ let h=0; for(const ch of s) h=(h*31+ch.charCodeAt(0))%360; return h; }
api.initials = initials; api.hue = hue;

function defaultCard(c, agg){
  const sats = agg ? `<div class="sats">${agg.items.map(x=>badgeSat(x,true)).join('')}</div>` : '';
  const x = agg || c;
  return `<article class="card${x.s===2?' is-part':''}${x.hard?' is-hard':''}" style="--h:${hue(x.n)}">
    <div class="logo">${esc(initials(x.n))}</div>
    <div class="info"><h3>${esc(x.n)}</h3>
      <div class="meta">${[x.c, x.g, x.l.slice(0,3).join(', ')].filter(Boolean).map(esc).join(' · ')||'—'}${(c&&c.o)?' · <em>'+esc(c.o)+'</em>':''}</div>
      ${x.pub?`<div class="pubtag">🏛 Servizio pubblico · ${esc(x.pub[1])}</div>`:''}
      ${sats}</div>
    <div class="tags">${resBadge(x.r)}${statoBadge(x.s)}${(!agg&&c.hard)?'<span class="bdg b-hard" title="Fascio non diretto sull\u2019Italia: da Torino serve una parabola grande o non è ricevibile">⚠ DIFFICILE</span>':''}</div>
  </article>`;
}
const card = SKIN.card || defaultCard;

function opt(v, label, cur){ return `<option value="${esc(v)}"${v===cur?' selected':''}>${esc(label)}</option>`; }
function filtersHTML(){
  return `<div class="filters">
   <label class="fl"><span>Genere</span><select id="f-genre">${opt('','Tutti i generi',st.genre)}${GENRES.map(g=>opt(g,g,st.genre)).join('')}</select></label>
   <label class="fl"><span>Lingua</span><select id="f-lang">${opt('','Tutte le lingue',st.lang)}${LANGS.map(g=>opt(g,g,st.lang)).join('')}</select></label>
   <label class="fl"><span>Qualità</span><select id="f-res">${opt('','Tutte',st.res)}${opt('HD','HD e 4K',st.res)}${opt('UHD','Solo 4K',st.res)}${opt('SD','Solo SD',st.res)}</select></label>
   <label class="fl"><span>Stato</span><select id="f-stato">${opt('','Chiaro + parziali',st.stato)}${opt('1','Solo in chiaro',st.stato)}${opt('2','Solo parzialmente in chiaro',st.stato)}</select></label>
   <label class="fl"><span>Raggruppa</span><select id="f-group">${opt('genere','Per genere',st.group)}${opt('lingua','Per lingua',st.group)}${opt('paese','Per paese',st.group)}${opt('','Nessun gruppo (A-Z)',st.group)}</select></label>
   <label class="chk"><input type="checkbox" id="f-hard"${st.hideHard?' checked':''}> Nascondi ricezione difficile da Torino</label>
   ${(st.genre||st.lang||st.res||st.stato||st.hideHard)?'<button class="reset" id="f-reset">Azzera filtri</button>':''}
  </div>`;
}
function pass(x){
  if(st.genre && x.g!==st.genre) return false;
  if(st.lang && !x.l.includes(st.lang)) return false;
  if(st.res==='HD' && x.r==='SD') return false;
  if(st.res && st.res!=='HD' && x.r!==st.res) return false;
  if(st.stato && String(x.s)!==st.stato) return false;
  if(st.hideHard && x.hard) return false;
  if(st.q){ const t = fold(st.q).split(/\s+/).filter(Boolean); if(!t.every(w=>x.f.includes(w))) return false; }
  return true;
}
function groupKey(x){ return st.group==='genere' ? (x.g||'Non definito') : st.group==='lingua' ? (x.l[0]||'Lingua non definita') : st.group==='paese' ? (x.c||'Paese non definito') : ''; }
function listHTML(items, isAgg){
  items.sort((a,b)=>a.n.localeCompare(b.n,'it',{sensitivity:'base'}));
  let html=''; let shown=0;
  if(st.group){
    const g = new Map(); items.forEach(x=>{const k=groupKey(x); if(!g.has(k)) g.set(k,[]); g.get(k).push(x);});
    const keys=[...g.keys()].sort((a,b)=>g.get(b).length-g.get(a).length);
    html += `<nav class="gjump">${keys.map(k=>`<a href="#g-${encodeURIComponent(k)}" data-jump="${esc(k)}">${esc(k)} <small>${g.get(k).length}</small></a>`).join('')}</nav>`;
    for(const k of keys){ if(shown>=st.limit) break; const arr=g.get(k).slice(0, st.limit-shown); shown+=arr.length;
      html += `<section class="grp" id="g-${encodeURIComponent(k)}"><h2 class="gh">${esc(k)} <small>${g.get(k).length}</small></h2><div class="list">${arr.map(x=>isAgg?card(null,x):card(x,null)).join('')}</div></section>`; }
  } else { const arr=items.slice(0,st.limit); shown=arr.length; html += `<div class="list">${arr.map(x=>isAgg?card(null,x):card(x,null)).join('')}</div>`; }
  if(items.length>shown) html += `<button class="more" id="more">Mostra altri (${items.length-shown})</button>`;
  if(!items.length) html += `<p class="empty">Nessun canale trovato con questi filtri.</p>`;
  return html;
}
function satInfoHTML(s){
  const ch = CH.filter(c=>c.p===s.pos);
  return `<div class="satinfo"><div><h1>${esc(s.nome)}</h1><p>${esc(s.satelliti)}</p></div>
   <ul class="kpi"><li><b>${ch.length}</b><span>canali in chiaro</span></li><li><b>${ch.filter(c=>c.r==='HD').length}</b><span>HD</span></li><li><b>${ch.filter(c=>c.r==='UHD').length}</b><span>4K</span></li><li><b>${ch.filter(c=>c.s===2).length}</b><span>parziali</span></li>
   <li title="Puntamento indicativo da Torino"><b>${s.az}° / ${s.el}°</b><span>azimut / elevazione da Torino</span></li></ul></div>`;
}
function viewSat(){
  const s = SAT[st.sat]; const items = CH.filter(c=>c.p===st.sat && pass(c));
  return { controls: filtersHTML(), head: satInfoHTML(s), body: `<p class="count">${items.length} canali${st.q?` per “${esc(st.q)}”`:''}</p>` + listHTML(items,false) };
}
function viewAll(){
  const items = [...AGG.values()].filter(pass);
  return { controls: filtersHTML(), head: `<div class="satinfo"><div><h1>${st.q?'Risultati ricerca':'Tutti i canali'}</h1><p>${st.q?`Ricerca “${esc(st.q)}” su tutti i ${D.sats.length} satelliti`:`Ogni canale con i satelliti dove è in chiaro`}</p></div><ul class="kpi"><li><b>${AGG.size}</b><span>canali unici</span></li><li><b>${CH.length}</b><span>presenze sui satelliti</span></li></ul></div>`,
    body: `<p class="count">${items.length} canali</p>` + listHTML(items,true) };
}
function resolveCountries(text){
  const out=new Set(); fold(text).split(/[,;\/+]|\s+e\s+|\s+/).map(t=>t.trim()).filter(t=>t.length>1).forEach(t=>{
    PUBC.forEach(p=>{ if(fold(p).includes(t)) out.add(p); });
    Object.entries(ADJ).forEach(([k,v])=>{ if(t.startsWith(k) && PUBC.includes(v)) out.add(v); });
  }); return out;
}
function viewPub(){
  const groups = new Map();
  AGG.forEach(a=>{ if(!a.pub || !st.pubSel.has(a.pub[0])) return; if(st.q && !fold(a.f).includes(fold(st.q))) return;
    const its = a.items.filter(x=>x.pub && (st.pubPart || x.s===1) && (!st.hideHard || !x.hard)); if(!its.length) return;
    const k=a.pub[0]; if(!groups.has(k)) groups.set(k,[]); groups.get(k).push({a,its}); });
  const controls = `<div class="pubctl">
    <label class="fl wide"><span>Scrivi i paesi (es. “canali francesi, tedeschi”)</span><input id="pub-text" placeholder="es. francesi, spagnoli, greci…" autocomplete="off"></label>
    <div class="chips">${PUBC.map(p=>`<button class="chip${st.pubSel.has(p)?' on':''}" data-pubc="${esc(p)}">${esc(p)}</button>`).join('')}</div>
    <div class="row"><button class="reset" data-pubset="all">Seleziona tutti</button><button class="reset" data-pubset="none">Nessuno</button>
    <label class="chk"><input type="checkbox" id="pub-part"${st.pubPart?' checked':''}> Conta anche i satelliti dove è solo parzialmente in chiaro</label>
    <label class="chk"><input type="checkbox" id="f-hard"${st.hideHard?' checked':''}> Nascondi ricezione difficile da Torino</label></div></div>`;
  const keys=[...groups.keys()].sort((a,b)=>a.localeCompare(b,'it'));
  let body = keys.length ? '' : '<p class="empty">Seleziona uno o più paesi qui sopra.</p>';
  for(const k of keys){ const arr=groups.get(k).sort((x,y)=>x.a.n.localeCompare(y.a.n,'it'));
    body += `<section class="grp"><h2 class="gh">${esc(k)} <small>${arr.length} canali</small></h2><div class="publist">${arr.map(({a,its})=>
      (SKIN.pubRow? SKIN.pubRow(a,its) : `<div class="pubrow" style="--h:${hue(a.n)}"><div class="pn"><span class="logo sm">${esc(initials(a.n))}</span><div><b>${esc(a.n)}</b><small>${esc(a.pub[1])}${a.g?' · '+esc(a.g):''}</small></div></div><div class="ps">${its.map(x=>badgeSat(x,true)).join('')}</div></div>`)).join('')}</div></section>`; }
  return { controls, head:`<div class="satinfo"><div><h1>Canali pubblici europei</h1><p>Per ogni canale: i satelliti dove è <b>in chiaro</b> (badge tratteggiato = parzialmente in chiaro)</p></div></div>`, body };
}
function viewNews(){
  const evs = D.ev.filter(e=> (!st.nSat || e.p===st.nSat) && (!st.nType || TYPES[e.t][1]===st.nType || e.t===st.nType) && (!st.q || fold(e.n+' '+e.c).includes(fold(st.q))) &&
    (!st.nDays || (Date.parse(D.meta.aggiornato.slice(0,10)) - Date.parse(e.d))/864e5 <= +st.nDays));
  const satsWithEv = D.sats.filter(s=>D.ev.some(e=>e.p===s.pos));
  const controls = `<div class="filters">
    <div class="chips">${['',...D.sats.map(s=>s.pos)].map(p=>`<button class="chip${st.nSat===p?' on':''}" data-nsat="${p}">${p?esc(SAT[p].nome):'Tutti i satelliti'} <small>${p?D.ev.filter(e=>e.p===p).length:D.ev.length}</small></button>`).join('')}</div>
    <label class="fl"><span>Tipo</span><select id="n-type">${opt('','Tutte le novità',st.nType)}${opt('in','Arrivi / tornati / ora in chiaro',st.nType)}${opt('out','Uscite / chiusure / criptati',st.nType)}${Object.entries(TYPES).map(([k,v])=>opt(k,v[0],st.nType)).join('')}</select></label>
    <label class="fl"><span>Periodo</span><select id="n-days">${opt('','Tutto (≈ ultimo mese)',st.nDays)}${opt('7','Ultimi 7 giorni',st.nDays)}${opt('14','Ultimi 14 giorni',st.nDays)}</select></label></div>`;
  let body='', last='';
  if(!evs.length) body='<p class="empty">Nessuna novità per questa selezione nel periodo coperto dai dati.</p>';
  body += '<div class="timeline">';
  evs.forEach(e=>{ const T=TYPES[e.t]; if(e.d!==last){ last=e.d; body+=`<h3 class="tday">${new Date(e.d+'T12:00').toLocaleDateString('it-IT',{weekday:'long',day:'numeric',month:'long',year:'numeric'})}</h3>`; }
    body += SKIN.newsRow ? SKIN.newsRow(e,T) : `<div class="ev ev-${T[1]}"><span class="evt">${T[1]==='in'?'▲':'▼'} ${esc(T[0])}</span><b class="evn">${esc(e.n)}</b>${e.r?resBadge(e.r):''}<span class="evm">${esc(SAT[e.p].nome)}${e.c?' · '+esc(e.c):''}${e.b?' · '+esc(e.b):''}</span>${e.il?'<span class="bdg b-fta">ora in lista</span>':''}</div>`; });
  body += '</div>';
  return { controls, head:`<div class="satinfo"><div><h1>Novità</h1><p>Canali in chiaro arrivati, tornati, usciti o diventati criptati · dati KingOfSat fino al ${esc(D.meta.aggiornato)}</p></div><ul class="kpi"><li><b>${D.ev.filter(e=>TYPES[e.t][1]==='in').length}</b><span>arrivi</span></li><li><b>${D.ev.filter(e=>TYPES[e.t][1]==='out').length}</b><span>uscite</span></li></ul></div>`, body };
}
function render(){
  const v = st.view==='sat' && st.q ? viewAll() : ({sat:viewSat, all:viewAll, pub:viewPub, news:viewNews}[st.view])();
  const ctl=$('#controls'), head=$('#head'), res=$('#results');
  if(ctl) ctl.innerHTML = v.controls; if(head) head.innerHTML = v.head; if(res) res.innerHTML = v.body;
  document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('on', b.dataset.view===st.view));
  document.body.dataset.view = st.view;
  if(SKIN.renderSatSelector) SKIN.renderSatSelector($('#satsel'), D.sats, st.sat, api); else defaultSatSel();
  if(SKIN.after) SKIN.after(api);
}
function defaultSatSel(){ const el=$('#satsel'); if(!el) return;
  el.innerHTML = D.sats.map(s=>`<button class="satbtn${s.pos===st.sat&&st.view==='sat'?' on':''}" data-sat="${s.pos}"><b>${esc(s.nome)}</b><small>${s.canali} canali</small></button>`).join(''); }
function setSat(p){ st.sat=p; st.view='sat'; st.limit=240; st.q=''; const q=$('#q'); if(q) q.value=''; render(); window.scrollTo({top:0,behavior:'smooth'}); }
function setView(v){ st.view=v; st.limit=240; render(); }
document.addEventListener('click', e=>{
  const t = e.target.closest('[data-sat],[data-gosat],[data-view],[data-pubc],[data-pubset],[data-nsat],#more,#f-reset,[data-jump]'); if(!t) return;
  if(t.dataset.jump!==undefined){ e.preventDefault(); const el=document.getElementById('g-'+encodeURIComponent(t.dataset.jump)); if(el) el.scrollIntoView({behavior:'smooth'}); return; }
  if(t.dataset.sat){ setSat(t.dataset.sat); return; }
  if(t.dataset.gosat){ setSat(t.dataset.gosat); return; }
  if(t.dataset.view){ setView(t.dataset.view); return; }
  if(t.dataset.pubc){ const p=t.dataset.pubc; st.pubSel.has(p)?st.pubSel.delete(p):st.pubSel.add(p); render(); return; }
  if(t.dataset.pubset){ st.pubSel = t.dataset.pubset==='all'? new Set(PUBC) : new Set(); render(); return; }
  if(t.dataset.nsat!==undefined){ st.nSat=t.dataset.nsat; render(); return; }
  if(t.id==='more'){ st.limit+=400; render(); return; }
  if(t.id==='f-reset'){ Object.assign(st,{genre:'',lang:'',res:'',stato:'',hideHard:false}); render(); }
});
document.addEventListener('change', e=>{ const t=e.target; const map={'f-genre':'genre','f-lang':'lang','f-res':'res','f-stato':'stato','f-group':'group','n-type':'nType','n-days':'nDays'};
  if(map[t.id]){ st[map[t.id]]=t.value; st.limit=240; render(); }
  else if(t.id==='f-hard'){ st.hideHard=t.checked; render(); }
  else if(t.id==='pub-part'){ st.pubPart=t.checked; render(); }
  else if(t.id==='satsel-select'){ setSat(t.value); } });
let qt; document.addEventListener('input', e=>{ const t=e.target;
  if(t.id==='q'){ clearTimeout(qt); qt=setTimeout(()=>{ st.q=t.value.trim(); st.limit=240; if(st.q && st.view==='sat') {} render(); }, 160); }
  if(t.id==='pub-text'){ const s=resolveCountries(t.value); if(s.size){ st.pubSel=s; const v=t.value; render(); const n=$('#pub-text'); n.value=v; n.focus(); } } });
document.addEventListener('keydown', e=>{ if(e.key==='/' && document.activeElement.tagName!=='INPUT'){ e.preventDefault(); $('#q')?.focus(); } });
document.addEventListener('DOMContentLoaded', ()=>{ const m=$('#meta'); if(m) m.innerHTML=`Dati: ${esc(D.meta.fonte)} · aggiornati il ${esc(D.meta.aggiornato)} · ${CH.length} presenze, ${AGG.size} canali unici`; if(SKIN.init) SKIN.init(api); render(); });
})();
