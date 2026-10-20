NAV = '''<button data-view="sat">Satelliti</button><button data-view="all">Tutti i canali</button><button data-view="pub">Pubblici europei</button><button data-view="news">Novità</button>'''
SEARCH = '<input id="q" type="search" placeholder="Cerca un canale… (es. Rai, France 24, sport)" autocomplete="off">'
T = {}

# 1 MINIMAL ------------------------------------------------------------
T[1] = dict(title='Minimal', desc='Stile essenziale “Apple-like”: tipografia grande, controllo segmentato, satelliti in una barra a scorrimento.',
css='''
body{font-family:-apple-system,"SF Pro Display","Inter",system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(0,0,0,.78);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid #1d1d1f}
.bar{max-width:1180px;margin:auto;display:flex;gap:18px;align-items:center;padding:12px 22px;flex-wrap:wrap}
.brand{font-weight:600;font-size:19px;letter-spacing:-.02em}.brand span{color:#86868b;font-weight:400}
.seg{display:flex;background:#1d1d1f;border-radius:10px;padding:3px;margin-left:auto}
.seg button{border:0;background:none;padding:6px 14px;border-radius:8px;font-size:13.5px;color:#a1a1a6}.seg button.on{background:#3a3a3c;color:#fff}
#q{flex:1 1 260px;max-width:340px;background:#1d1d1f;border:0;border-radius:10px;padding:9px 14px;color:#fff}
main{max-width:1180px;margin:auto;padding:0 22px 60px}
#satsel{display:flex;gap:10px;overflow-x:auto;padding:18px 0 6px;scrollbar-width:none}
.satbtn{flex:none;background:#111;border:1px solid #222;border-radius:14px;padding:10px 16px;text-align:left}
.satbtn b{display:block;font-size:14px;font-weight:600}.satbtn small{color:#86868b}.satbtn.on{background:#f5f5f7;color:#000}.satbtn.on small{color:#555}
body:not([data-view=sat]) #satsel{display:none}
#head{padding:34px 0 18px}#head h1{font-size:48px;letter-spacing:-.035em;font-weight:700}
#controls{padding:14px 0;border-top:1px solid #1d1d1f;border-bottom:1px solid #1d1d1f;margin-bottom:10px}
.gh{font-size:26px;letter-spacing:-.02em;margin:34px 0 8px}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:0 28px}
.card{display:flex;gap:14px;align-items:center;padding:12px 0;border-bottom:1px solid #1d1d1f}
.card .info{flex:1;min-width:0}.card h3{margin:0;font-size:15.5px;font-weight:600}.card .meta{color:#86868b;font-size:12.5px;margin-top:2px}
.card .tags{display:flex;flex-direction:column;gap:4px;align-items:flex-end}.card .b-fta{display:none}
.logo{border-radius:12px;background:#1d1d1f;color:#f5f5f7}
footer{color:#6e6e73;font-size:12px;text-align:center;padding:30px}
#fontslot #fontctl{background:#1d1d1f;border:0;border-radius:10px}#fontctl button{color:#f5f5f7}#fontctl button:hover:not(:disabled){background:#3a3a3c}
#totop{background:rgba(29,29,31,.85);backdrop-filter:blur(20px);border:0}
''',
body=f'''<header><div class="bar"><div class="brand">Satelliti <span>da Torino</span></div>{SEARCH}<nav class="seg">{NAV}</nav><div id="fontslot"></div></div></header>
<main><div id="satsel"></div><div id="head"></div><div id="controls"></div><div id="results"></div></main><footer id="meta"></footer>''', js='')

# 2 NEON ---------------------------------------------------------------
T[2] = dict(title='Neon Cyberpunk', desc='Luci al neon magenta/ciano, font monospazio, satellite scelto da una tendina “finestrella”.',
css='''

body{font-family:"JetBrains Mono","Fira Code",ui-monospace,Menlo,Consolas,monospace;background:#000 radial-gradient(ellipse at top,#1a0024 0,#000 60%) fixed}
header{padding:22px 24px 10px;max-width:1240px;margin:auto}
.logo-t{font-size:30px;font-weight:800;letter-spacing:.08em;color:#fff;text-shadow:0 0 6px #ff00e6,0 0 18px #ff00e6,0 0 40px #8000ff}
.logo-t em{color:#00f0ff;font-style:normal;text-shadow:0 0 8px #00f0ff,0 0 24px #00a2ff}
.tag{color:#7cf;font-size:12px;letter-spacing:.3em;text-transform:uppercase}
.top{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:16px}
nav{display:flex;gap:8px;flex-wrap:wrap}nav button{background:none;border:1px solid #ff00e6;color:#ff8bf2;padding:7px 14px;text-transform:uppercase;font-size:12px;letter-spacing:.12em;clip-path:polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%)}
nav button.on{background:#ff00e6;color:#000;box-shadow:0 0 18px #ff00e6}
#q{flex:1 1 260px;background:#05000a;border:1px solid #00f0ff;color:#00f0ff;padding:10px 14px;box-shadow:0 0 12px #00f0ff55 inset;outline:none}
#q::placeholder{color:#00f0ff88}
main{max-width:1240px;margin:auto;padding:10px 24px 60px}
.win{border:1px solid #00f0ff;box-shadow:0 0 22px #00f0ff44;padding:14px 16px;margin:14px 0;background:#000a}
.win label{color:#00f0ff;font-size:11px;letter-spacing:.25em}
#satsel select{width:100%;background:#000;color:#fff;border:1px solid #ff00e6;padding:12px;font-size:16px;margin-top:6px;box-shadow:0 0 14px #ff00e655}
body:not([data-view=sat]) .win{display:none}
#head h1{font-size:34px;color:#00f0ff;text-shadow:0 0 12px #00f0ff;text-transform:uppercase}
.kpi b{color:#ff8bf2;text-shadow:0 0 10px #ff00e6}
.fl{color:#7cf}.fl select,.fl input{background:#000;border-color:#ff00e688;color:#fff;border-radius:0}
#controls{margin:16px 0}.chip{border-radius:0;border-color:#00f0ff66}.chip.on{background:#00f0ff;color:#000;box-shadow:0 0 12px #00f0ff}
.gh{color:#ff8bf2;text-shadow:0 0 10px #ff00e6;text-transform:uppercase;letter-spacing:.1em;font-size:18px;margin-top:30px;border-bottom:1px dashed #ff00e655;padding-bottom:6px}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.card{display:flex;gap:12px;align-items:center;padding:12px;border:1px solid #222;background:linear-gradient(135deg,#0a0012,#000);position:relative}
.card:hover{border-color:#00f0ff;box-shadow:0 0 16px #00f0ff55}
.card h3{margin:0;font-size:14px;color:#fff}.card .meta{font-size:11.5px;color:#8a8aa8;margin-top:3px}.card .info{flex:1;min-width:0}
.card .tags{display:flex;flex-direction:column;gap:4px}
.logo{border-radius:0;background:#000;border:1px solid hsl(var(--h) 100% 60%);color:hsl(var(--h) 100% 70%);text-shadow:0 0 8px hsl(var(--h) 100% 60%)}
.b-hd{background:none;border:1px solid #00f0ff;color:#00f0ff;box-shadow:0 0 8px #00f0ff88}.b-4k{background:none;border:1px solid #ffe600;color:#ffe600;box-shadow:0 0 8px #ffe600aa}
.b-fta{background:none;border:1px solid #39ff14;color:#39ff14}.b-part{background:none}
.sbdg{border-radius:0;background:#000;border-color:#ff00e666}.sbdg b{color:#00f0ff}
footer{color:#7cf8;font-size:11px;text-align:center;padding:30px}
.tday{color:#00f0ff}.ev{border-color:#1a0024}
#fontctl{background:#05000a;border:1px solid #00f0ff;border-radius:0;box-shadow:0 0 16px #00f0ff66}#fontctl button{color:#00f0ff;border-radius:0;font-family:inherit}#fontctl button:hover:not(:disabled){background:#00f0ff22}
#fontctl #fs-reset{color:#ff8bf2}
#totop{border-radius:0;background:#000;border:1px solid #ff00e6;color:#ff8bf2;box-shadow:0 0 18px #ff00e6;clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);width:54px}
''',
body=f'''<header><div class="tag">// ricevibili da torino //</div><div class="logo-t">SAT<em>NEON</em>.TV</div><div class="top">{SEARCH}<nav>{NAV}</nav></div></header>
<main><div class="win"><label>&gt; FINESTRELLA SATELLITE</label><div id="satsel"></div></div><div id="head"></div><div id="controls"></div><div id="results"></div></main><footer id="meta"></footer>''',
js='''window.SKIN={renderSatSelector(el,sats,cur,api){ if(!el) return; el.innerHTML='<select id="satsel-select">'+sats.map(s=>`<option value="${s.pos}"${s.pos===cur?' selected':''}>${s.nome} — ${s.canali} canali in chiaro</option>`).join('')+'</select>'; }};''')

# 3 DASHBOARD ----------------------------------------------------------
T[3] = dict(title='Dashboard', desc='Pannello di controllo con barra laterale: satelliti e sezioni a sinistra, filtri in alto, elenco a tabella compatta.',
css='''
body{font-family:Inter,system-ui,sans-serif;font-size:14px}
.app{display:grid;grid-template-columns:270px 1fr;min-height:100vh}
aside{background:#0b0b0d;border-right:1px solid #1e1e22;padding:18px 14px;position:sticky;top:0;height:100vh;overflow:auto}
.brand{font-weight:800;font-size:17px;display:flex;gap:8px;align-items:center;margin-bottom:18px}.brand i{width:10px;height:10px;border-radius:50%;background:#22c55e;box-shadow:0 0 10px #22c55e}
.side-h{font-size:10.5px;color:#666;text-transform:uppercase;letter-spacing:.12em;margin:18px 6px 6px}
aside nav{display:flex;flex-direction:column;gap:2px}
aside nav button,.satbtn{display:flex;justify-content:space-between;align-items:center;width:100%;border:0;background:none;text-align:left;padding:8px 10px;border-radius:8px;color:#bbb}
aside nav button:hover,.satbtn:hover{background:#16161a}aside nav button.on,.satbtn.on{background:#14532d;color:#dcfce7}
.satbtn b{font-weight:500}.satbtn small{color:#777;font-size:11.5px}.satbtn.on small{color:#bbf7d0}
#satsel{display:flex;flex-direction:column;gap:2px}
.content{padding:0 26px 50px;min-width:0}
.topbar{position:sticky;top:0;z-index:4;background:#000e;backdrop-filter:blur(8px);display:flex;gap:12px;padding:14px 0;border-bottom:1px solid #1e1e22}
#q{flex:1;background:#0f0f12;border:1px solid #26262b;border-radius:8px;padding:9px 12px;color:#fff}
#head{padding:20px 0 6px}#head h1{font-size:24px}
.kpi li{background:#0b0b0d;border:1px solid #1e1e22;border-radius:10px;padding:8px 14px}.kpi b{color:#4ade80;font-size:18px}
#controls{background:#0b0b0d;border:1px solid #1e1e22;border-radius:12px;padding:12px;margin:12px 0}
.gh{font-size:15px;margin:22px 0 6px;color:#4ade80}
.list{display:flex;flex-direction:column;border:1px solid #1e1e22;border-radius:10px;overflow:hidden}
.card{display:grid;grid-template-columns:34px minmax(180px,1.4fr) 2fr auto;gap:12px;align-items:center;padding:7px 12px;border-bottom:1px solid #16161a}
.card:nth-child(odd){background:#08080a}.card:hover{background:#101418}
.card .logo{width:30px;height:30px;font-size:11px;border-radius:6px}
.card .info{display:contents}.card h3{margin:0;font-size:13.5px;font-weight:600}.card .meta{color:#888;font-size:12.5px}
.card .sats{grid-column:2/4}.card .pubtag{display:none}
.card .tags{display:flex;gap:4px;justify-content:flex-end}
@media(max-width:820px){.app{grid-template-columns:1fr}aside{position:static;height:auto}#satsel{flex-direction:row;flex-wrap:wrap}.satbtn{width:auto}.card{grid-template-columns:30px 1fr auto}.card .meta{grid-column:2/4}}
footer{color:#666;font-size:12px;padding:20px 0}
#fontslot #fontctl{background:#0f0f12;border-color:#26262b;border-radius:8px}#fontctl button:hover:not(:disabled){background:#14532d}
#totop{background:#14532d;border-color:#22c55e;color:#dcfce7;border-radius:10px}
''',
body=f'''<div class="app"><aside><div class="brand"><i></i>SatDash Torino</div><div class="side-h">Sezioni</div><nav>{NAV}</nav><div class="side-h">Satelliti</div><div id="satsel"></div></aside>
<div class="content"><div class="topbar">{SEARCH}<div id="fontslot"></div></div><div id="head"></div><div id="controls"></div><div id="results"></div><footer id="meta"></footer></div></div>''', js='')

# 4 CARD GRID ----------------------------------------------------------
T[4] = dict(title='Griglia a schede', desc='Griglia di grandi schede colorate con le iniziali del canale come logo, satelliti come schede in alto.',
css='''
body{font-family:"Poppins","Segoe UI",system-ui,sans-serif}
header{max-width:1360px;margin:auto;padding:22px 22px 0;display:flex;flex-wrap:wrap;gap:16px;align-items:center}
.brand{font-size:24px;font-weight:800}.brand b{background:linear-gradient(90deg,#f43f5e,#f59e0b);-webkit-background-clip:text;color:transparent}
nav{display:flex;gap:6px;margin-left:auto}nav button{border:0;background:#141414;padding:9px 16px;border-radius:12px;font-weight:600}nav button.on{background:#fff;color:#000}
#q{flex:1 1 100%;background:#111;border:2px solid #222;border-radius:16px;padding:14px 18px;font-size:16px;color:#fff}
#q:focus{border-color:#f59e0b;outline:none}
main{max-width:1360px;margin:auto;padding:0 22px 60px}
#satsel{display:flex;gap:6px;flex-wrap:wrap;margin:18px 0;border-bottom:2px solid #1c1c1c;padding-bottom:0}
.satbtn{border:0;background:none;padding:10px 14px;border-bottom:3px solid transparent;margin-bottom:-2px;text-align:left}
.satbtn b{display:block;font-size:14px}.satbtn small{color:#777;font-size:11px}.satbtn.on{border-color:#f59e0b}.satbtn.on b{color:#f59e0b}
body:not([data-view=sat]) #satsel{display:none}
#head{margin:22px 0 10px}#head h1{font-size:34px}
#controls{margin:10px 0 6px}
.gh{font-size:22px;margin:30px 0 12px}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}
.tile{background:#0e0e0e;border:1px solid #1d1d1d;border-radius:18px;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s}
.tile:hover{transform:translateY(-3px);border-color:hsl(var(--h) 70% 40%)}
.tile .big{aspect-ratio:16/9;display:grid;place-items:center;font-size:40px;font-weight:900;letter-spacing:-.03em;background:linear-gradient(135deg,hsl(var(--h) 70% 30%),hsl(calc(var(--h) + 40) 70% 14%));color:hsl(var(--h) 100% 88%);position:relative}
.tile .big .tags{position:absolute;top:8px;right:8px;display:flex;gap:4px}
.tile .tx{padding:10px 12px 12px}.tile h3{margin:0;font-size:14.5px;line-height:1.25}.tile .meta{font-size:11.5px;color:#888;margin-top:4px}
.tile .sats{margin-top:6px}.tile .sbdg{font-size:10.5px;padding:2px 6px}
.publist{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:10px}
@media(max-width:640px){#satsel{flex-wrap:nowrap;overflow-x:auto}.satbtn{flex:none}.list{grid-template-columns:repeat(2,1fr)}.publist{grid-template-columns:1fr}}.pubrow{background:#0e0e0e;border-radius:14px;padding:12px;border:1px solid #1d1d1d}
footer{color:#666;font-size:12px;text-align:center;padding:30px}
#fontctl{background:#141414;border:2px solid #222;border-radius:16px}#fontctl button{border-radius:12px}#fontctl button:hover:not(:disabled){background:#fff;color:#000}
#totop{background:linear-gradient(135deg,#f43f5e,#f59e0b);border:0;color:#000;font-weight:900;border-radius:16px}
.tile .big{font-size:calc(40px * var(--fs))}
''',
body=f'''<header><div class="brand">Sat<b>Grid</b> · Torino</div><nav>{NAV}</nav>{SEARCH}</header>
<main><div id="satsel"></div><div id="head"></div><div id="controls"></div><div id="results"></div></main><footer id="meta"></footer>''',
js='''window.SKIN={card(c,agg){const A=window.SATAPP,x=agg||c,e=A.esc;return `<article class="tile" style="--h:${A.hue(x.n)}"><div class="big">${e(A.initials(x.n))}<div class="tags">${A.resBadge(x.r)}${x.s===2?'<span class="bdg b-part" title="Parzialmente in chiaro">PARZ.</span>':''}${(!agg&&c.hard)?'<span class="bdg b-hard" title="Ricezione difficile da Torino">⚠</span>':''}</div></div><div class="tx"><h3><span class="cn">${e(x.n)}</span></h3><div class="meta">${[x.c,x.g,x.l.slice(0,2).join(', ')].filter(Boolean).map(e).join(' · ')}</div>${agg?'<div class="sats">'+agg.items.map(i=>A.badgeSat(i,false)).join('')+'</div>':''}</div></article>`;}};''')

# 5 ORBITAL ------------------------------------------------------------
T[5] = dict(title='Orbitale', desc='Tema spaziale con cielo stellato: i satelliti sono disposti sull’arco orbitale come visti da Torino, clicca un satellite per aprirne la sezione.',
css='''
body{font-family:"Space Grotesk","Segoe UI",system-ui,sans-serif;background:#000}
#stars{position:fixed;inset:0;z-index:-1;background:radial-gradient(1px 1px at 20% 30%,#fff8,transparent),radial-gradient(1px 1px at 70% 80%,#fff6,transparent),radial-gradient(1.5px 1.5px at 40% 60%,#fff9,transparent),radial-gradient(1px 1px at 85% 20%,#fff7,transparent),radial-gradient(1px 1px at 10% 85%,#fff5,transparent),radial-gradient(ellipse at 50% 120%,#0b1a3a 0,#000 60%);background-size:230px 230px,310px 310px,410px 410px,170px 170px,270px 270px,100% 100%}
header{max-width:1220px;margin:auto;padding:20px 22px 0;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.brand{font-size:20px;letter-spacing:.2em;text-transform:uppercase}.brand b{color:#7dd3fc}
nav{display:flex;gap:4px;margin-left:auto;background:#ffffff0d;border:1px solid #ffffff1a;border-radius:999px;padding:4px}
nav button{border:0;background:none;padding:7px 14px;border-radius:999px;font-size:13px;color:#cbd5e1}nav button.on{background:#7dd3fc;color:#001}
#q{flex:1 1 100%;background:#ffffff08;border:1px solid #ffffff22;border-radius:999px;padding:11px 18px;color:#fff}
main{max-width:1220px;margin:auto;padding:0 22px 60px}
#satsel{margin:10px 0 0}#satsel svg{width:100%;height:auto;display:block}
.sat-dot{cursor:pointer}.sat-dot circle.c{fill:#0b1220;stroke:#7dd3fc;stroke-width:1.5;transition:.2s}.sat-dot:hover circle.c{fill:#7dd3fc33}
.sat-dot.on circle.c{fill:#7dd3fc;filter:drop-shadow(0 0 8px #7dd3fc)}.sat-dot text{fill:#cbd5e1;font-size:11px;text-anchor:middle}.sat-dot.on text{fill:#fff;font-weight:700}
.sat-dot text.n{fill:#7dd3fc;font-size:10px}
body:not([data-view=sat]) #satsel{opacity:.35}
#head{margin:4px 0 10px}#head h1{font-size:36px;font-weight:500}
#controls{background:#ffffff08;border:1px solid #ffffff14;border-radius:18px;padding:14px;margin:10px 0}
.fl select,.fl input{background:#0b1220;border-color:#ffffff22}
.gh{font-weight:500;font-size:20px;color:#7dd3fc;margin:28px 0 10px}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.card{display:flex;gap:12px;align-items:center;padding:12px;border-radius:16px;background:#0b1220aa;border:1px solid #ffffff12}
.card .logo{border-radius:50%;background:radial-gradient(circle at 30% 30%,hsl(var(--h) 70% 45%),hsl(var(--h) 60% 12%));color:#fff}
.card .info{flex:1;min-width:0}.card h3{margin:0;font-size:14.5px;font-weight:600}.card .meta{color:#94a3b8;font-size:12px}
.card .tags{display:flex;flex-direction:column;gap:4px;align-items:flex-end}
footer{color:#64748b;font-size:12px;text-align:center;padding:30px}
#fontctl{background:#0b1220cc;border:1px solid #7dd3fc55;border-radius:999px;backdrop-filter:blur(8px)}#fontctl button{border-radius:999px;color:#cbd5e1}#fontctl button:hover:not(:disabled){background:#7dd3fc;color:#001}
#totop{background:radial-gradient(circle at 30% 30%,#7dd3fc,#0b3a5a);border:0;color:#001;box-shadow:0 0 20px #7dd3fc88}
''',
body=f'''<div id="stars"></div><header><div class="brand">Orbita <b>Torino</b></div><nav>{NAV}</nav>{SEARCH}</header>
<main><div id="satsel"></div><div id="head"></div><div id="controls"></div><div id="results"></div></main><footer id="meta"></footer>''',
js='''window.SKIN={renderSatSelector(el,sats,cur,api){ if(!el) return; const W=1100,H=250,pad=60;
 const els=sats.map(s=>s.el), mn=Math.min(...els), mx=Math.max(...els);
 const P=sats.map((s,i)=>({s,x:pad+i*(W-2*pad)/(sats.length-1), y:200-(s.el-mn)/(mx-mn)*140}));
 let d='M '+P.map(p=>p.x+' '+p.y).join(' L ');
 let h=`<svg viewBox="0 0 ${W} ${H}"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7dd3fc22"/><stop offset=".5" stop-color="#7dd3fcaa"/><stop offset="1" stop-color="#7dd3fc22"/></linearGradient></defs>`;
 h+=`<path d="${d}" fill="none" stroke="url(#g)" stroke-width="1.5" stroke-dasharray="4 6"/>`;
 h+=`<text x="${pad-20}" y="16" fill="#64748b" font-size="11">◀ EST</text><text x="${W-pad-20}" y="16" fill="#64748b" font-size="11">OVEST ▶</text><text x="${W/2}" y="${H-8}" fill="#64748b" font-size="11" text-anchor="middle">Arco geostazionario visto da Torino (altezza = elevazione) · clicca un satellite</text>`;
 P.forEach(({s,x,y},i)=>{const r=6+Math.sqrt(s.canali)/2.4, up=i%2===0;
  h+=`<g class="sat-dot${s.pos===cur&&api.st.view==='sat'?' on':''}" data-sat="${s.pos}"><title>${s.nome} — ${s.canali} canali in chiaro · azimut ${s.az}° · elevazione ${s.el}°</title><circle cx="${x}" cy="${y}" r="${r+12}" fill="transparent"/><circle class="c" cx="${x}" cy="${y}" r="${r}"/><text x="${x}" y="${up?y-r-18:y+r+16}">${s.nome.replace(/ [\\d.]+°.*/,'')}</text><text class="n" x="${x}" y="${up?y-r-6:y+r+28}">${s.pos.replace('E','°E').replace('W','°W')}</text></g>`;});
 el.innerHTML=h+'</svg>'; }};''')

# 6 EPG / TELEVIDEO ----------------------------------------------------
T[6] = dict(title='Guida TV / Televideo', desc='Elenco denso stile guida TV (EPG) con colori da Televideo: righe numerate, colonne Canale/Genere/Lingua/Paese/Qualità.',
css='''
body{font-family:"VT323","Courier New",ui-monospace,monospace;font-size:17px;background:#000;color:#fff}
.tt{max-width:1180px;margin:auto;padding:14px 16px 50px}
.ttbar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;background:#0000aa;padding:6px 10px}
.ttbar .p{color:#ffff00}.ttbar .t{color:#00ffff;margin-left:auto}
h1.big{font-size:44px;margin:10px 0;letter-spacing:.06em}h1.big span{background:#ff0000;padding:0 10px}h1.big em{color:#ffff00;font-style:normal}
nav{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:8px 0}
nav button{border:0;padding:6px;font-size:17px;font-family:inherit;color:#000;font-weight:700}
nav button:nth-child(1){background:#ff0000}nav button:nth-child(2){background:#00ff00}nav button:nth-child(3){background:#ffff00}nav button:nth-child(4){background:#00ffff}
nav button.on{outline:3px solid #fff;outline-offset:-3px}
#q{width:100%;background:#000;border:2px solid #ffff00;color:#ffff00;padding:8px 10px;font-family:inherit;font-size:18px;margin:6px 0}
#satsel{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:0 18px;margin:10px 0;border-top:2px solid #00ffff;border-bottom:2px solid #00ffff;padding:6px 0}
.satbtn{border:0;background:none;text-align:left;font-family:inherit;font-size:17px;display:flex;gap:10px;padding:1px 4px;color:#fff}
.satbtn .pg{color:#ffff00}.satbtn small{color:#00ffff;margin-left:auto}.satbtn.on{background:#ffff00;color:#000}.satbtn.on .pg,.satbtn.on small{color:#000}
body:not([data-view=sat]) #satsel{display:none}
#head h1{font-size:30px;color:#00ffff;text-transform:uppercase}#head p{color:#fff}.kpi b{color:#ffff00}.kpi span{color:#0f0;font-size:14px}
#controls{border:2px dashed #00ff00;padding:8px;margin:10px 0}.fl{color:#0f0;font-size:15px}.fl select,.fl input{background:#000;border:1px solid #0f0;color:#fff;border-radius:0;font-family:inherit;font-size:16px}
.chip{border-radius:0;font-family:inherit;font-size:15px}.reset{border-radius:0;font-family:inherit}
.gh{background:#0000aa;color:#ffff00;font-size:22px;padding:2px 8px;margin:20px 0 0;font-weight:400}
.list{display:flex;flex-direction:column}
.row{display:grid;grid-template-columns:52px minmax(170px,2fr) 1.1fr 1.1fr 1fr 120px;gap:10px;padding:2px 8px;align-items:center}
.row:nth-child(even){background:#0a0a2a}.row:hover{background:#222}
.row .num{color:#ffff00}.row .nm{color:#fff}.row .g{color:#00ffff}.row .l{color:#0f0}.row .c{color:#ff66ff}
.row .q{text-align:right}.row .sats{grid-column:2/7}.row .sbdg{font-family:inherit;font-size:14px;border-radius:0}
.hdr{color:#000;background:#00ffff}.hdr:nth-child(even){background:#00ffff}
.bdg{border-radius:0;font-family:inherit;font-size:14px}
@media(max-width:760px){.row{grid-template-columns:46px 1fr 90px}.row .g,.row .l,.row .c{display:none}.row .sats{grid-column:2/4}}
footer{color:#00ffff;padding:20px 0;font-size:15px}
.tday{color:#ffff00;font-size:20px}.ev{font-size:17px}.evt{border-radius:0}

.ttbar{position:sticky;top:0;z-index:10}#fontslot #fontctl{background:#000;border:0;border-radius:0;padding:0;gap:4px}#fontctl button{border-radius:0;font-family:inherit;font-size:17px;height:26px;background:#ffff00;color:#000}
#fontctl #fs-reset{background:#00ffff;color:#000;font-size:15px;opacity:1}#fontctl button:hover:not(:disabled){background:#fff}
#totop{border-radius:0;background:#ff0000;border:2px solid #fff;color:#fff;font-family:inherit}
@media(max-width:640px){.ttbar{gap:6px}.ttbar .t{display:none}}
''',
body=f'''<div class="tt"><div class="ttbar"><span class="p">P100</span><span>SATELLITI DA TORINO</span><span class="t" id="clock"></span><div id="fontslot"></div></div>
<h1 class="big"><span>SAT</span>VIDEO <em>TORINO</em></h1><nav>{NAV}</nav>{SEARCH}<div id="satsel"></div><div id="head"></div><div id="controls"></div><div id="results"></div><footer id="meta"></footer></div>''',
js='''let rowN=0;window.SKIN={
 init(){const c=()=>{const d=new Date();document.getElementById('clock').textContent=d.toLocaleDateString('it-IT',{weekday:'short',day:'2-digit',month:'short'}).toUpperCase()+' '+d.toLocaleTimeString('it-IT');};c();setInterval(c,1000);},
 renderSatSelector(el,sats,cur,api){if(!el)return;el.innerHTML=sats.map((s,i)=>`<button class="satbtn${s.pos===cur?' on':''}" data-sat="${s.pos}"><span class="pg">${201+i}</span>${s.nome}<small>${s.canali}</small></button>`).join('');},
 card(c,agg){const A=window.SATAPP,x=agg||c,e=A.esc;rowN++;return `<div class="row"><span class="num">${String(rowN).padStart(3,'0')}</span><span class="nm cn">${e(x.n)}</span><span class="g">${e(x.g||'-')}</span><span class="l">${e(x.l.slice(0,2).join(', ')||'-')}</span><span class="c">${e(x.c||'-')}</span><span class="q">${A.resBadge(x.r)} ${x.s===2?'<span class="bdg b-part" title="Parzialmente in chiaro">PARZ</span>':''}${(!agg&&c.hard)?'<span class="bdg b-hard" title="Ricezione difficile da Torino">⚠</span>':''}</span>${agg?'<div class="sats">'+agg.items.map(i=>A.badgeSat(i,true)).join('')+'</div>':''}</div>`;},
 after(){rowN=0;}};
const _r=()=>{rowN=0};document.addEventListener('click',_r,true);document.addEventListener('change',_r,true);document.addEventListener('input',_r,true);''')

# 7 GLASS --------------------------------------------------------------
T[7] = dict(title='Glassmorphism', desc='Pannelli di vetro sfocato su sfondo nero con bagliori colorati; il satellite si sceglie da una finestrella a comparsa.',
css='''
body{font-family:"Inter","Segoe UI",system-ui,sans-serif;background:#000;min-height:100vh}
.blob{position:fixed;border-radius:50%;filter:blur(90px);opacity:.6;z-index:-1}
.b1{width:520px;height:520px;background:#7c3aed;top:-160px;left:-120px}.b2{width:460px;height:460px;background:#0ea5e9;bottom:-160px;right:-80px}.b3{width:300px;height:300px;background:#db2777;top:40%;left:55%;opacity:.25}
.glass{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(22px) saturate(160%);-webkit-backdrop-filter:blur(22px) saturate(160%);border-radius:22px}
header{max-width:1200px;margin:18px auto 0;padding:12px 16px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;position:sticky;top:12px;z-index:5}
.brand{font-weight:700;font-size:18px}.brand span{opacity:.6;font-weight:400}
nav{display:flex;gap:4px;flex-wrap:wrap}nav button{border:0;background:none;padding:8px 14px;border-radius:14px;font-size:13.5px;color:#ddd}nav button.on{background:rgba(255,255,255,.16);color:#fff}
#q{flex:1 1 240px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:10px 14px;color:#fff}
.open{border:1px solid rgba(255,255,255,.2);background:linear-gradient(135deg,#7c3aed88,#0ea5e988);padding:9px 16px;border-radius:14px;font-weight:600}
main{max-width:1200px;margin:auto;padding:0 16px 60px}
#head{margin:22px 0 0;padding:22px}#head h1{font-size:32px}
#controls{margin:14px 0;padding:14px}.fl select,.fl input{background:rgba(0,0,0,.35);border-color:rgba(255,255,255,.15);border-radius:12px}
.gh{font-size:19px;margin:26px 4px 10px}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}
.card{display:flex;gap:12px;align-items:center;padding:12px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);backdrop-filter:blur(14px)}
.card:hover{background:rgba(255,255,255,.09)}.card .info{flex:1;min-width:0}.card h3{margin:0;font-size:14.5px}.card .meta{font-size:12px;color:#aaa}
.card .logo{border-radius:14px;background:linear-gradient(135deg,hsl(var(--h) 80% 55% / .55),hsl(calc(var(--h) + 60) 80% 40% / .35));color:#fff;border:1px solid rgba(255,255,255,.2)}
.card .tags{display:flex;flex-direction:column;gap:4px;align-items:flex-end}
.chip{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.15)}
#modal{position:fixed;inset:0;z-index:20;display:none;place-items:center;background:rgba(0,0,0,.5)}#modal.show{display:grid}
#modal .glass{width:min(860px,94vw);max-height:86vh;overflow:auto;padding:22px;background:rgba(20,20,30,.6)}
#modal h2{margin:0 0 14px;display:flex;justify-content:space-between}#modal h2 button{border:0;background:none;font-size:22px}
#satsel{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}
.satbtn{text-align:left;padding:14px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12)}
.satbtn b{display:block}.satbtn small{color:#aaa}.satbtn.on{background:linear-gradient(135deg,#7c3aed99,#0ea5e999)}
.curs{font-size:13px;opacity:.75}
footer{color:#888;font-size:12px;text-align:center;padding:30px}
#fontctl{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:16px;backdrop-filter:blur(22px) saturate(160%);-webkit-backdrop-filter:blur(22px)}#fontctl button{border-radius:12px}#fontctl button:hover:not(:disabled){background:rgba(255,255,255,.16)}
#totop{background:linear-gradient(135deg,#7c3aedcc,#0ea5e9cc);border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(14px)}
''',
body=f'''<div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
<header class="glass"><div class="brand">Vetro<span>Sat</span></div><button class="open" id="opensat">🛰 Scegli satellite</button><span class="curs" id="cursat"></span><nav>{NAV}</nav>{SEARCH}</header>
<main><div id="head" class="glass"></div><div id="controls" class="glass"></div><div id="results"></div></main><footer id="meta"></footer>
<div id="modal"><div class="glass"><h2>Scegli il satellite <button id="closesat" aria-label="Chiudi">✕</button></h2><div id="satsel"></div></div></div>''',
js='''window.SKIN={init(api){const m=document.getElementById('modal');document.getElementById('opensat').onclick=()=>m.classList.add('show');document.getElementById('closesat').onclick=()=>m.classList.remove('show');m.addEventListener('click',e=>{if(e.target===m||e.target.closest('[data-sat]'))m.classList.remove('show');});},
 renderSatSelector(el,sats,cur,api){el.innerHTML=sats.map(s=>`<button class="satbtn${s.pos===cur?' on':''}" data-sat="${s.pos}"><b>${s.nome}</b><small>${s.satelliti}<br>${s.canali} canali · ${s.hd} HD · ${s.uhd} 4K</small></button>`).join('');document.getElementById('cursat').textContent=api.st.view==='sat'?'Attuale: '+api.SAT[cur].nome:'';}};''')
