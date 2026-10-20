# Paese (nome italiano usato da KingOfSat) -> (codice ISO bandiera, continente)
# Scelte: Turchia, Russia, Cipro -> Europa (Stati membri del Consiglio d'Europa/UEFA/EBU, emittenti
# storicamente "europee"); Caucaso (Armenia, Azerbaigian, Georgia), Kazakistan, Medio Oriente e Golfo -> Asia;
# Nord Africa (Egitto, Libia, Tunisia, Algeria, Marocco, Mauritania, Sudan) -> Africa.
# Paese vuoto / non riconosciuto -> 'Non specificato' (chip a parte, globo al posto della bandiera).
EU, AS, AF, AM, OC = 'Europa', 'Asia', 'Africa', 'America', 'Oceania'
C = {
 # Europa
 'Italia':('it',EU),'Francia':('fr',EU),'Germania':('de',EU),'Spagna':('es',EU),'Portogallo':('pt',EU),'Regno Unito':('gb',EU),
 'Irlanda':('ie',EU),'Austria':('at',EU),'Svizzera':('ch',EU),'Belgio':('be',EU),'Paesi Bassi':('nl',EU),'Lussemburgo':('lu',EU),
 'Monaco':('mc',EU),'San Marino':('sm',EU),'Vaticano':('va',EU),'Malta':('mt',EU),'Andorra':('ad',EU),'Liechtenstein':('li',EU),
 'Polonia':('pl',EU),'Repubblica Ceca':('cz',EU),'Slovacchia':('sk',EU),'Ungheria':('hu',EU),'Slovenia':('si',EU),'Croazia':('hr',EU),
 'Serbia':('rs',EU),'Bosnia Herzegovina':('ba',EU),'Montenegro':('me',EU),'Kosovo':('xk',EU),'Macedonia':('mk',EU),'Macedonia del Nord':('mk',EU),
 'Albania':('al',EU),'Grecia':('gr',EU),'Cipro':('cy',EU),'Bulgaria':('bg',EU),'Romania':('ro',EU),'Moldavia':('md',EU),'Ucraina':('ua',EU),
 'Bielorussia':('by',EU),'Russia':('ru',EU),'Turchia':('tr',EU),'Lituania':('lt',EU),'Lettonia':('lv',EU),'Estonia':('ee',EU),
 'Norvegia':('no',EU),'Svezia':('se',EU),'Danimarca':('dk',EU),'Finlandia':('fi',EU),'Islanda':('is',EU),
 # Asia (incl. Medio Oriente, Golfo, Caucaso)
 'Armenia':('am',AS),'Azerbaigian':('az',AS),'Georgia':('ge',AS),'Kazakistan':('kz',AS),'Uzbekistan':('uz',AS),'Turkmenistan':('tm',AS),
 'Tagikistan':('tj',AS),'Kirghizistan':('kg',AS),'Afghanistan':('af',AS),'Iran':('ir',AS),'Iraq':('iq',AS),'Siria':('sy',AS),'Libano':('lb',AS),
 'Giordania':('jo',AS),'Israele':('il',AS),'Palestina':('ps',AS),'Arabia Saudita':('sa',AS),'Yemen':('ye',AS),'Oman':('om',AS),'Qatar':('qa',AS),
 'Kuwait':('kw',AS),'Emirati del Bahrain':('bh',AS),'Bahrain':('bh',AS),'Emirati Arabi Uniti':('ae',AS),'Abu Dhabi':('ae',AS),
 'Emirati del Dubai':('ae',AS),'Emirato Sharjah':('ae',AS),'Pakistan':('pk',AS),'India':('in',AS),'Bangladesh':('bd',AS),'Sri Lanka':('lk',AS),
 'Nepal':('np',AS),'Cina':('cn',AS),'Hong Kong':('hk',AS),'Taiwan':('tw',AS),'Giappone':('jp',AS),'Corea del Sud':('kr',AS),'Corea del Nord':('kp',AS),
 'Mongolia':('mn',AS),'Singapore':('sg',AS),'Malesia':('my',AS),'Malaysia':('my',AS),'Indonesia':('id',AS),'Filippine':('ph',AS),
 'Thailandia':('th',AS),'Vietnam':('vn',AS),
 # Africa
 'Egitto':('eg',AF),'Libia':('ly',AF),'Tunisia':('tn',AF),'Algeria':('dz',AF),'Marocco':('ma',AF),'Mauritania':('mr',AF),'Sudan':('sd',AF),
 'Etiopia':('et',AF),'Eritrea':('er',AF),'Somalia':('so',AF),'Kenya':('ke',AF),'Uganda':('ug',AF),'Tanzania':('tz',AF),'Ruanda':('rw',AF),
 'Nigeria':('ng',AF),'Niger':('ne',AF),'Mali':('ml',AF),'Burkina Faso':('bf',AF),'Benin':('bj',AF),'Togo':('tg',AF),'Ghana':('gh',AF),
 'Ivory Coast':('ci',AF),"Costa d'Avorio":('ci',AF),'Senegal':('sn',AF),'Guinea':('gn',AF),'Camerun':('cm',AF),'Gabon':('ga',AF),
 'Chad':('td',AF),'Ciad':('td',AF),'Congo':('cg',AF),'Repubblica Democratica del Congo':('cd',AF),'Equatorial Guinea':('gq',AF),
 'Angola':('ao',AF),'Mozambico':('mz',AF),'Zimbabwe':('zw',AF),'Madagascar':('mg',AF),'Sud Africa':('za',AF),
 # America
 'U.S.A.':('us',AM),'Canada':('ca',AM),'Messico':('mx',AM),'Cuba':('cu',AM),'Venezuela':('ve',AM),'Brasile':('br',AM),
 'Argentina':('ar',AM),'Colombia':('co',AM),'Cile':('cl',AM),'Perù':('pe',AM),
 # Oceania
 'Australia':('au',OC),'Nuova Zelanda':('nz',OC),
}
CONTINENTS = [EU, AS, AF, AM, OC, 'Non specificato']
def info(paese):
    return C.get(paese or '', (None, 'Non specificato'))
