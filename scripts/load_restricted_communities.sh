#
# Import script for restricted communities (synchronized 27.8.2025)
#
# Usage:
# ./scripts/load_restricted_communities.sh
#
#

set -ex

if [ -d .venv ]; then
    source .venv/bin/activate
fi

RESTRICTED_COMMUNITIES=(
    "sf4z;AGRITEC, výzkum, šlechtění a služby"
    "a3vz;Agrotest fyto"
    "orx0;Agrovýzkum Rapotín"
    "vz0p;Akademie múzických umění v Praze"
    "s6w0;Akademie výtvarných umění v Praze"
    "3y70;Arnika"
    "bn9g;CENIA, Česká informační agentura životního prostředí"
    "5d7u;Centrum dopravního výzkumu"
    "gkuu;Centrum pro dopravu a energetiku"
    "sif9;Centrum pro studium vysokého školství"
    "158p;Ústav výzkumu globální změny AV ČR"
    "37x0;Česká asociace ergoterapeutů"
    "1lzg;Česká asociace paraplegiků"
    "td9y;Česká společnost ornitologická"
    "f3da;CESNET"
    "6q0q;Česká rada dětí a mládeže"
    "ij19;CzWa: Asociace pro vodu ČR"
    "0ycl;Ekodomov"
    "ls7n;Fairtrade Česko a Slovensko"
    "c3wj;Galerie výtvarného umění v Ostravě"
    "sco8;Gender Studies"
    "xwx8;Geologický ústav AV ČR"
    "tdgt;GLE"
    "zpp5;HESTIA"
    "xh47;Historický ústav AV ČR"
    "2w0h;Chmelařský institut"
    "ww2n;Institut umění - Divadelní ústav"
    "a5ep;Iuridicum Remedium"
    "esco;Jihomoravské muzeum ve Znojmě"
    "cgnx;Mendelova univerzita v Brně"
    "w4js;Ministerstvo spravedlnosti"
    "x5g4;Moravská galerie v Brně"
    "ee9w;Moravská zemská knihovna v Brně"
    "h9qi;Muzeum Brněnska"
    "mw0v;Muzeum skla a bižuterie v Jablonci nad Nisou"
    "s7qs;Muzeum východních Čech v Hradci Králové"
    "ph4r;Národní archiv"
    "lvkj;Nadace Karel Komárek Family Foundation"
    "n39l;Národní hřebčín Kladruby nad Labem"
    "i3rd;Národní muzeum"
    "5lz0;Národní muzeum v přírodě"
    "j60z;Národní památkový ústav"
    "8w0f;Národní technické muzeum"
    "bptm;Národní zemědělské muzeum"
    "dyc9;Národní filmový archiv"
    "8ox9;Národní ústav lidové kultury"
    "ezi6;Ostravská univerzita"
    "ua9m;Památník národního písemnictví"
    "x1uj;Parlamentní institut"
    "cbsj;Psychologický ústav AV ČR"
    "hmf6;Sdružení pro integraci a migraci"
    "xnqf;Severočeské muzeum v Liberci"
    "w2su;SIRIRI"
    "aml6;Slezská univerzita v Opavě"
    "qbvk;Slezské zemské muzeum"
    "0xxb;Správa úložišť radioaktivních odpadů"
    "pg8m;Státní zemědělská a potravinářská inspekce"
    "pja0;Technické muzeum v Brně"
    "jbcq;Univerzita Hradec Králové"
    "g57k;Univerzita Jana Evangelisty Purkyně v Ústí nad Labem"
    "am51;Uměleckoprůmyslové museum v Praze"
    "kw7r;Univerzita Palackého v Olomouci"
    "eaww;Úřad průmyslového vlastnictví"
    "gp40;Ústav archeologické památkové péče severozápadních Čech"
    "51w5;Ústav dějin umění AV ČR"
    "yqi3;Ústav pro studium totalitních režimů"
    "6fa7;Ústav teoretické a aplikované mechaniky AV ČR"
    "nkpd;Vysoká škola chemicko-technologická v Praze"
    "mq7e;Výzkumný ústav vodohospodářský T. G. Masaryka"
    "euy3;Výzkumný a vývojový ústav dřevařský, Praha"
    "t6uk;Vysoká škola ekonomická v Praze"
    "2nsj;Vysoká škola evropských a regionálních studií"
    "oisl;Vysoká škola finanční a správní"
    "qnk8;Výzkumný institut práce a sociálních věcí"
    "2n6p;Výzkumný ústav lesního hospodářství a myslivosti"
    "v1n8;Národní centrum zemědělského a potravinářského výzkumu"
    "7w8p;Výzkumný ústav pro krajinu"
    "rgmz;WOODEXPERT"
    "q81z;Západočeské muzeum v Plzni"
)

for community in "${RESTRICTED_COMMUNITIES[@]}"; do
    slug="${community%%;*}"
    title="${community#*;}"
    
    echo "Creating community: $slug - $title"
    invenio oarepo communities create --private "$slug" "$title"
done