# -*- coding: utf-8 -*-
"""Vsa besedila in podatki za beezee.si (SL / EN / HR).
Uredi tukaj, nato zaženi build.py."""

SITE = "https://beezee.si"

LANGS = ["sl", "en", "hr"]

# Pot do domače strani in pravnih strani po jezikih (relativno na koren)
PATHS = {
    "sl": {"home": "/",    "privacy": "/zasebnost/",   "cookies": "/piskotki/",   "imprint": "/impresum/", "thanks": "/hvala/", "welcome": "/panj/dobrodosli/"},
    "en": {"home": "/en/", "privacy": "/en/privacy/",  "cookies": "/en/cookies/", "imprint": "/en/imprint/", "thanks": "/en/thanks/", "welcome": "/en/hive/welcome/"},
    "hr": {"home": "/hr/", "privacy": "/hr/privatnost/", "cookies": "/hr/kolacici/", "imprint": "/hr/impresum/", "thanks": "/hr/hvala/", "welcome": "/hr/kosnica/dobrodosli/"},
}

T = {
    "sl": {
        "htmlLang": "sl", "ogLocale": "sl_SI",
        "metaTitle": "BEEZEE – spletne strani, trgovine, vtičniki in aplikacije | Katja Kolšek",
        "metaDesc": "Za vse, ki ste vedno beezee. Izdelujem in prenavljam spletne strani in WooCommerce trgovine, pišem WordPress vtičnike ter razvijam iOS in Android aplikacije.",
        "navWork": "Delo", "navServices": "Storitve", "navAbout": "O meni", "navHive": "Panj", "navContact": "Kontakt",
        "ctaWrite": "Pišimo si", "ctaWork": "Poglej moje delo",
        "stickerHi": "živjo, jaz sem Katja", "stickerCta": "← začni tukaj", "stickerMe": "moj brskalnik, vsak dan", "stickerHive": "pssst, tukaj je med",
        "heroTitle": "Za vse, ki ste vedno beezee.",
        "heroSub": "Spletne strani, trgovine, vtičniki in aplikacije – zgrajeni s skrbnostjo čebele, da ti ostane več časa za tisto, kar imaš rad/-a.",
        "servicesH": "Kaj delam", "servicesSub": "Štiri stvari, ki jih delam dobro in rada.",
        "s1": "Spletne strani in prenove", "s1d": "Nova stran ali prenova obstoječe. Hitra, pregledna, tvoja.",
        "s2": "Spletne trgovine (WooCommerce)", "s2d": "Trgovina, ki prodaja tudi takrat, ko ti spiš.",
        "s3": "WordPress vtičniki", "s3d": "Funkcija, ki je ne najdeš v nobenem vtičniku? Jo napišem.",
        "s4": "iOS in Android aplikacije", "s4d": "Od ideje do App Stora in Google Playa.",
        "workH": "Izbrano delo", "workSub": "Nekaj projektov iz panja.",
        "fAll": "Vse", "fSites": "Strani", "fShops": "Trgovine", "fPlugins": "Vtičniki", "fApps": "Aplikacije",
        "catSite": "Spletna stran", "catShop": "Spletna trgovina", "catPlugin": "WordPress vtičnik", "catApp": "Aplikacija",
        "empty": "Tukaj kmalu brenči nov projekt.",
        "aboutH": "O meni",
        "about1": "Živjo, jaz sem Katja. Moj brskalnik ima vedno odprtih vsaj 50 zavihkov. Moja glava tudi. Ideja za aplikacijo pride med kuhanjem kosila, rešitev za vtičnik ob polnoči, nov dizajn trgovine nekje vmes. Uradno nediagnosticiran ADHD, neuradno moja supermoč. Pač čebelica.",
        "about2": "BEEZEE je za vse nas, ki smo vedno beezee. Ti imaš svoj posel, družino in sto idej. Jaz tudi – le da je moj posel ravno to: spletne strani, trgovine, vtičniki in aplikacije. Skupaj zgradiva nekaj, kar dela namesto tebe.",
        "signature": "Katja", "tabsLabel": "50+ zavihkov",
        "processH": "Kako delam", "processSub": "Štirje koraki, brez presenečenj.",
        "p1": "Pogovor", "p1d": "Povem ti, kaj je smiselno, in poslušam, kaj potrebuješ.",
        "p2": "Načrt", "p2d": "Jasen obseg, cena in rok. Na papirju, preden se začne.",
        "p3": "Gradnja", "p3d": "Sproti vidiš napredek in lahko poveš svoje.",
        "p4": "Lansiranje in podpora", "p4d": "Objava, predaja in nekdo, ki ti dvigne telefon tudi pozneje.",
        "hiveH": "Dobrodošli v panju.",
        "hiveText": "Panj je moja skupnost: stranke, uporabniki aplikacij in vsi, ki jih zanima, kaj nastaja v delavnici. Ob prijavi dobiš brezplačen kontrolni seznam pred prenovo spletne strani in obvestilo, ko izide nova aplikacija.",
        "hiveDoc": "Kontrolni seznam pred prenovo spletne strani", "hiveDocSub": "PDF · brezplačno ob prijavi",
        "hiveGift1": "Kontrolni seznam pred prenovo", "hiveGift2": "Obvestila o novih aplikacijah",
        "emailPh": "tvoj@naslov.si", "join": "Pridruži se panju",
        "hiveNote": "Brez spama. Pišem samo, ko imam kaj sladkega.",
        "hiveThanks": "Hvala! Preveri pošto in potrdi prijavo.",
        "hiveError": "Ups, nekaj je šlo narobe. Poskusi še enkrat ali mi piši na katja@beezee.si.",
        "contactH": "Brenčimo?", "contactSub": "Povej, kaj te muči, in odpišem v dveh delovnih dneh.",
        "lName": "Ime", "lEmail": "E-pošta", "lNeed": "Kaj potrebuješ?", "lMsg": "Sporočilo", "msgPh": "Nekaj stavkov je dovolj.", "send": "Pošlji sporočilo",
        "sending": "Pošiljam …",
        "sent": "Hvala, sporočilo je v panju. Odpišem kmalu.",
        "sentError": "Sporočila ni bilo mogoče poslati. Piši mi na katja@beezee.si.",
        "consent": "Strinjam se z obdelavo podatkov za namen odgovora.",
        "orWrite": "Ali piši na", "phoneLabel": "Telefon", "phone": "041 449 054", "linkedin": "LinkedIn", "printLabel": "Natisni nalepko",
        "footLegal": "BEEZEE.SI Katja Kolšek s.p.", "privacy": "Zasebnost", "cookies": "Piškotki", "imprint": "Impresum",
        "langLabel": "Jezik", "menu": "Meni", "close": "Zapri", "mainNav": "Glavni meni", "footNav": "Noga", "filterLabel": "Filter",
        "sticker1": "ta je moja", "sticker2": "sladko delo", "sticker3": "tukaj začneva",
        "backHome": "← Nazaj na domačo stran",
        "thanksTitle": "Hvala!", "thanksText": "Tvoje sporočilo je v panju. Odpišem v dveh delovnih dneh.",
        "thanksHiveTitle": "Še en korak.", "thanksHiveText": "Če si se prijavil/-a v panj: preveri pošto in klikni potrditveno povezavo.",
        "welcomeTitle": "Dobrodošel/-a v panju! 🐝", "welcomeText": "Prijava je potrjena. Pisala bom samo, ko bom imela kaj sladkega: nova aplikacija, nov projekt, kontrolni seznam. Odjava je mogoča kadar koli s sporočilom na katja@beezee.si.",
    },
    "en": {
        "htmlLang": "en", "ogLocale": "en_GB",
        "metaTitle": "BEEZEE – websites, online shops, plugins and apps | Katja Kolšek",
        "metaDesc": "For everyone who's always beezee. I build and redesign websites and WooCommerce shops, write WordPress plugins and develop iOS and Android apps.",
        "navWork": "Work", "navServices": "Services", "navAbout": "About", "navHive": "The hive", "navContact": "Contact",
        "ctaWrite": "Let's talk", "ctaWork": "See my work",
        "stickerHi": "hi, I'm Katja", "stickerCta": "← start here", "stickerMe": "my browser, every day", "stickerHive": "psst, the honey is here",
        "heroTitle": "For everyone who's always beezee.",
        "heroSub": "Websites, shops, plugins and apps – built with the care of a bee, so you have more time for what you love.",
        "servicesH": "What I do", "servicesSub": "Four things I do well and gladly.",
        "s1": "Websites and redesigns", "s1d": "A new site or a refresh of the old one. Fast, clear, yours.",
        "s2": "Online shops (WooCommerce)", "s2d": "A shop that keeps selling while you sleep.",
        "s3": "WordPress plugins", "s3d": "Can't find the feature in any plugin? I'll write it.",
        "s4": "iOS and Android apps", "s4d": "From idea to the App Store and Google Play.",
        "workH": "Selected work", "workSub": "A few projects from the hive.",
        "fAll": "All", "fSites": "Sites", "fShops": "Shops", "fPlugins": "Plugins", "fApps": "Apps",
        "catSite": "Website", "catShop": "Online shop", "catPlugin": "WordPress plugin", "catApp": "App",
        "empty": "A new project will buzz here soon.",
        "aboutH": "About me",
        "about1": "Hi, I'm Katja. My browser always has at least 50 tabs open. So does my head. The idea for an app comes while cooking lunch, the fix for a plugin at midnight, a new shop design somewhere in between. Officially undiagnosed ADHD, unofficially my superpower. A bee, basically.",
        "about2": "BEEZEE is for all of us who are always beezee. You have your own business, a family and a hundred ideas. So do I – it's just that my business is exactly this: websites, shops, plugins and apps. Together we build something that works for you.",
        "signature": "Katja", "tabsLabel": "50+ tabs",
        "processH": "How I work", "processSub": "Four steps, no surprises.",
        "p1": "Conversation", "p1d": "I tell you what makes sense and listen to what you need.",
        "p2": "Plan", "p2d": "Clear scope, price and deadline. On paper, before we start.",
        "p3": "Build", "p3d": "You see progress as it happens and can have your say.",
        "p4": "Launch and support", "p4d": "Go-live, handover and someone who picks up the phone later too.",
        "hiveH": "Welcome to the hive.",
        "hiveText": "The hive is my community: clients, app users and everyone curious about what's being made in the workshop. When you join you get a free website redesign checklist and a note whenever a new app comes out.",
        "hiveDoc": "Website redesign checklist", "hiveDocSub": "PDF · free when you join",
        "hiveGift1": "Redesign checklist", "hiveGift2": "New app announcements",
        "emailPh": "you@address.com", "join": "Join the hive",
        "hiveNote": "No spam. I only write when I have something sweet.",
        "hiveThanks": "Thanks! Check your inbox and confirm.",
        "hiveError": "Oops, something went wrong. Try again or write to katja@beezee.si.",
        "contactH": "Shall we buzz?", "contactSub": "Tell me what's bugging you and I'll reply within two working days.",
        "lName": "Name", "lEmail": "Email", "lNeed": "What do you need?", "lMsg": "Message", "msgPh": "A few sentences is enough.", "send": "Send message",
        "sending": "Sending …",
        "sent": "Thanks, your message is in the hive. I'll reply soon.",
        "sentError": "The message could not be sent. Please write to katja@beezee.si.",
        "consent": "I agree to my data being processed to answer this request.",
        "orWrite": "Or write to", "phoneLabel": "Phone", "phone": "+386 41 449 054", "linkedin": "LinkedIn", "printLabel": "Print label",
        "footLegal": "BEEZEE.SI Katja Kolšek s.p.", "privacy": "Privacy", "cookies": "Cookies", "imprint": "Imprint",
        "langLabel": "Language", "menu": "Menu", "close": "Close", "mainNav": "Main menu", "footNav": "Footer", "filterLabel": "Filter",
        "sticker1": "this one is mine", "sticker2": "sweet work", "sticker3": "we start here",
        "backHome": "← Back to the home page",
        "thanksTitle": "Thank you!", "thanksText": "Your message is in the hive. I'll reply within two working days.",
        "thanksHiveTitle": "One more step.", "thanksHiveText": "If you joined the hive: check your inbox and click the confirmation link.",
        "welcomeTitle": "Welcome to the hive! 🐝", "welcomeText": "Your subscription is confirmed. I only write when I have something sweet: a new app, a new project, the checklist. You can unsubscribe any time by writing to katja@beezee.si.",
    },
    "hr": {
        "htmlLang": "hr", "ogLocale": "hr_HR",
        "metaTitle": "BEEZEE – web stranice, trgovine, dodaci i aplikacije | Katja Kolšek",
        "metaDesc": "Za sve koji su uvijek beezee. Izrađujem i redizajniram web stranice i WooCommerce trgovine, pišem WordPress dodatke te razvijam iOS i Android aplikacije.",
        "navWork": "Radovi", "navServices": "Usluge", "navAbout": "O meni", "navHive": "Košnica", "navContact": "Kontakt",
        "ctaWrite": "Javi mi se", "ctaWork": "Pogledaj moje radove",
        "stickerHi": "bok, ja sam Katja", "stickerCta": "← počni ovdje", "stickerMe": "moj preglednik, svaki dan", "stickerHive": "pssst, ovdje je med",
        "heroTitle": "Za sve koji su uvijek beezee.",
        "heroSub": "Web stranice, trgovine, dodaci i aplikacije – izrađeni s pažnjom pčele, da ti ostane više vremena za ono što voliš.",
        "servicesH": "Što radim", "servicesSub": "Četiri stvari koje radim dobro i rado.",
        "s1": "Web stranice i redizajn", "s1d": "Nova stranica ili redizajn postojeće. Brza, pregledna, tvoja.",
        "s2": "Web trgovine (WooCommerce)", "s2d": "Trgovina koja prodaje i dok spavaš.",
        "s3": "WordPress dodaci", "s3d": "Funkcija koje nema ni u jednom dodatku? Napišem je.",
        "s4": "iOS i Android aplikacije", "s4d": "Od ideje do App Storea i Google Playa.",
        "workH": "Odabrani radovi", "workSub": "Nekoliko projekata iz košnice.",
        "fAll": "Sve", "fSites": "Stranice", "fShops": "Trgovine", "fPlugins": "Dodaci", "fApps": "Aplikacije",
        "catSite": "Web stranica", "catShop": "Web trgovina", "catPlugin": "WordPress dodatak", "catApp": "Aplikacija",
        "empty": "Ovdje će uskoro zujati novi projekt.",
        "aboutH": "O meni",
        "about1": "Bok, ja sam Katja. Moj preglednik uvijek ima otvorenih barem 50 kartica. Moja glava također. Ideja za aplikaciju dođe dok kuham ručak, rješenje za dodatak u ponoć, novi dizajn trgovine negdje između. Službeno nedijagnosticiran ADHD, neslužbeno moja supermoć. Pčelica, eto.",
        "about2": "BEEZEE je za sve nas koji smo uvijek beezee. Ti imaš svoj posao, obitelj i sto ideja. Ja također – samo što je moj posao upravo ovo: web stranice, trgovine, dodaci i aplikacije. Zajedno gradimo nešto što radi umjesto tebe.",
        "signature": "Katja", "tabsLabel": "50+ kartica",
        "processH": "Kako radim", "processSub": "Četiri koraka, bez iznenađenja.",
        "p1": "Razgovor", "p1d": "Kažem ti što ima smisla i slušam što trebaš.",
        "p2": "Plan", "p2d": "Jasan opseg, cijena i rok. Na papiru, prije početka.",
        "p3": "Izrada", "p3d": "Napredak vidiš u hodu i možeš reći svoje.",
        "p4": "Lansiranje i podrška", "p4d": "Objava, primopredaja i netko tko se javi na telefon i kasnije.",
        "hiveH": "Dobrodošli u košnicu.",
        "hiveText": "Košnica je moja zajednica: klijenti, korisnici aplikacija i svi koje zanima što nastaje u radionici. Prijavom dobivaš besplatan kontrolni popis prije redizajna web stranice i obavijest kad izađe nova aplikacija.",
        "hiveDoc": "Kontrolni popis prije redizajna web stranice", "hiveDocSub": "PDF · besplatno uz prijavu",
        "hiveGift1": "Kontrolni popis prije redizajna", "hiveGift2": "Obavijesti o novim aplikacijama",
        "emailPh": "tvoj@adresa.hr", "join": "Pridruži se košnici",
        "hiveNote": "Bez spama. Pišem samo kad imam nešto slatko.",
        "hiveThanks": "Hvala! Provjeri poštu i potvrdi prijavu.",
        "hiveError": "Ups, nešto je pošlo po zlu. Pokušaj ponovno ili mi piši na katja@beezee.si.",
        "contactH": "Zujimo?", "contactSub": "Reci što te muči i odgovorim u dva radna dana.",
        "lName": "Ime", "lEmail": "E-pošta", "lNeed": "Što trebaš?", "lMsg": "Poruka", "msgPh": "Nekoliko rečenica je dovoljno.", "send": "Pošalji poruku",
        "sending": "Šaljem …",
        "sent": "Hvala, poruka je u košnici. Odgovorim uskoro.",
        "sentError": "Poruku nije bilo moguće poslati. Piši mi na katja@beezee.si.",
        "consent": "Slažem se s obradom podataka u svrhu odgovora.",
        "orWrite": "Ili piši na", "phoneLabel": "Telefon", "phone": "+386 41 449 054", "linkedin": "LinkedIn", "printLabel": "Ispiši naljepnicu",
        "footLegal": "BEEZEE.SI Katja Kolšek s.p.", "privacy": "Privatnost", "cookies": "Kolačići", "imprint": "Impresum",
        "langLabel": "Jezik", "menu": "Izbornik", "close": "Zatvori", "mainNav": "Glavni izbornik", "footNav": "Podnožje", "filterLabel": "Filter",
        "sticker1": "ova je moja", "sticker2": "slatki posao", "sticker3": "ovdje počinjemo",
        "backHome": "← Natrag na početnu",
        "thanksTitle": "Hvala!", "thanksText": "Tvoja poruka je u košnici. Odgovorim u dva radna dana.",
        "thanksHiveTitle": "Još jedan korak.", "thanksHiveText": "Ako si se prijavio/-la u košnicu: provjeri poštu i klikni poveznicu za potvrdu.",
        "welcomeTitle": "Dobrodošao/-la u košnicu! 🐝", "welcomeText": "Prijava je potvrđena. Pišem samo kad imam nešto slatko: nova aplikacija, novi projekt, kontrolni popis. Odjava je moguća bilo kada porukom na katja@beezee.si.",
    },
}

# Projekti v portfoliu (vrstni red = vrstni red na strani)
PROJECTS = [
    {"id": "lonc", "name": "Lonc", "url": "lonc.app", "href": "https://lonc.app/", "img": "lonc", "cat": "app", "catKey": "catApp", "type": "app",
     "d": {"sl": "Aplikacija z recepti. »Vrzi v lonc.« Za iOS in Android.",
           "en": "Recipe app. »Vrzi v lonc.« For iOS and Android.",
           "hr": "Aplikacija s receptima. »Vrzi v lonc.« Za iOS i Android."}},
    {"id": "pausie", "name": "Pausie", "url": "pausie.app", "href": "https://pausie.app/", "img": "pausie", "cat": "app", "catKey": "catApp", "type": "app",
     "d": {"sl": "Dnevnik za perimenopavzo in menopavzo. Za iOS in Android.",
           "en": "A journal for perimenopause and menopause. For iOS and Android.",
           "hr": "Dnevnik za perimenopauzu i menopauzu. Za iOS i Android."}},
    {"id": "astor", "name": "astor.si", "url": "astor.si", "href": "https://astor.si/", "img": "astor", "cat": "shop", "catKey": "catShop", "type": "web",
     "d": {"sl": "Prenova spletne trgovine za hišne ljubljenčke.",
           "en": "Redesign of an online shop for pet supplies.",
           "hr": "Redizajn web trgovine za kućne ljubimce."}},
    {"id": "dingo", "name": "dingogear.si", "url": "dingogear.si", "href": "https://dingogear.si/", "img": "dingogear", "cat": "shop", "catKey": "catShop", "type": "web",
     "d": {"sl": "Spletna trgovina za šport in trening psov.",
           "en": "Online shop for dog sport and training.",
           "hr": "Web trgovina za sport i trening pasa."}},
    {"id": "tropidog", "name": "tropidog.si", "url": "tropidog.si", "href": "https://tropidog.si/", "img": "tropidog", "cat": "shop", "catKey": "catShop", "type": "web",
     "d": {"sl": "Spletna trgovina s hrano, priboljški in prehranskimi dodatki za pse.",
           "en": "Online shop for dog food, treats and supplements.",
           "hr": "Web trgovina s hranom, poslasticama i dodacima prehrani za pse."}},
    {"id": "loncsi", "name": "lonc.si", "url": "lonc.si", "href": "https://lonc.si/", "img": "lonc", "cat": "site", "catKey": "catSite", "type": "web",
     "d": {"sl": "Predstavitvena stran aplikacije Lonc. Čist HTML, brez WordPressa, SL/EN/HR.",
           "en": "Landing site for the Lonc app. Plain HTML, no WordPress, SL/EN/HR.",
           "hr": "Predstavitvena stranica aplikacije Lonc. Čisti HTML, bez WordPressa, SL/EN/HR."}},
    {"id": "pausiesi", "name": "pausie.si", "url": "pausie.si", "href": "https://pausie.si/", "img": "pausie", "cat": "site", "catKey": "catSite", "type": "web",
     "d": {"sl": "Predstavitvena stran aplikacije Pausie: hitra, lahka, brez WordPressa.",
           "en": "Landing site for the Pausie app: fast, light, no WordPress.",
           "hr": "Predstavitvena stranica aplikacije Pausie: brza, lagana, bez WordPressa."}},
    {"id": "shipping", "name": {"sl": "Woo pošiljanje", "en": "Woo shipping", "hr": "Woo dostava"}, "url": {"sl": "WooCommerce › Naročilo #4821", "en": "WooCommerce › Order #4821", "hr": "WooCommerce › Narudžba #4821"},
     "href": None, "img": None, "cat": "plugin", "catKey": "catPlugin", "type": "plugin", "ph": "DPD · GLS",
     "d": {"sl": "Vtičnika za DPD in GLS: paketi in nalepke neposredno iz naročila.",
           "en": "DPD and GLS plugins: parcels and labels straight from the order.",
           "hr": "Dodaci za DPD i GLS: paketi i naljepnice izravno iz narudžbe."}},
]

FILTERS = [("all", "fAll"), ("site", "fSites"), ("shop", "fShops"), ("plugin", "fPlugins"), ("app", "fApps")]

# Pravne strani – besedila (HTML odstavki). Oglate oklepaje [ ] je treba zamenjati s pravimi podatki.
LEGAL = {
    "sl": {
        "imprint": {"title": "Impresum", "html": """
<p><strong>BEEZEE.SI Katja Kolšek s.p.</strong><br>[Naslov], [Pošta]<br>Slovenija</p>
<p>Matična številka: [matična št.]<br>Davčna številka: [davčna št.]<br>Identifikacijska številka za DDV: [SI-ID za DDV, če je]</p>
<p>E-pošta: <a href="mailto:katja@beezee.si">katja@beezee.si</a><br>Telefon: <a href="tel:+38641449054">041 449 054</a></p>
<p>Odgovorna oseba za vsebino: Katja Kolšek.</p>
<p>Logotip in besedila na tej strani so last BEEZEE.SI Katja Kolšek s.p. Posnetki zaslona projektov so last njihovih lastnikov in so prikazani kot referenca.</p>"""},
        "privacy": {"title": "Politika zasebnosti", "html": """
<p>Upravljavec osebnih podatkov je BEEZEE.SI Katja Kolšek s.p., [Naslov], [Pošta], <a href="mailto:katja@beezee.si">katja@beezee.si</a> (v nadaljevanju »jaz«).</p>
<h2>Katere podatke obdelujem in zakaj</h2>
<p><strong>Kontaktni obrazec.</strong> Ko mi pišeš prek obrazca, obdelujem tvoje ime, e-poštni naslov in vsebino sporočila, da ti lahko odgovorim. Pravna podlaga je tvoja privolitev (člen 6(1)(a) GDPR) in izvajanje predpogodbenih ukrepov (člen 6(1)(b) GDPR). Sporočila hranim največ 2 leti po zadnjem stiku, razen če iz njih nastane sodelovanje.</p>
<p><strong>Panj (e-novice).</strong> Ob prijavi obdelujem tvoj e-poštni naslov, da ti pošljem kontrolni seznam in občasna obvestila o novih aplikacijah in projektih. Pravna podlaga je privolitev, ki jo potrdiš s klikom v potrditvenem e-sporočilu (dvojna potrditev). Odjaviš se lahko kadar koli s povezavo na dnu vsakega sporočila ali s sporočilom na katja@beezee.si. Seznam članov hranim na svojem strežniku (Neoserv, Slovenija); ne uporabljam zunanjih orodij za e-novice.</p>
<p><strong>Strežniški dnevniki.</strong> Gostovanje strani zagotavlja Neoserv (Slovenija). Strežnik iz tehničnih in varnostnih razlogov kratek čas beleži IP naslov, čas dostopa in zahtevano stran. Pravna podlaga je moj zakoniti interes (člen 6(1)(f) GDPR).</p>
<h2>Komu posredujem podatke</h2>
<p>Podatkov ne prodajam in jih ne posredujem tretjim osebam, razen ponudniku gostovanja, ki delujejo po mojih navodilih in v skladu z GDPR.</p>
<h2>Tvoje pravice</h2>
<p>Kadar koli lahko zahtevaš dostop do svojih podatkov, popravek, izbris, omejitev obdelave ali prenos podatkov ter prekličeš privolitev. Piši na <a href="mailto:katja@beezee.si">katja@beezee.si</a>. Pritožbo lahko vložiš pri Informacijskem pooblaščencu Republike Slovenije (www.ip-rs.si).</p>
<p>Zadnja posodobitev: [datum].</p>"""},
        "cookies": {"title": "Piškotki", "html": """
<p>Ta stran <strong>ne uporablja piškotkov za sledenje ali oglaševanje</strong> in ne nalaga orodij za analitiko, ki bi zahtevala tvojo privolitev. Zato ne prikazujem obvestila o piškotkih.</p>
<p>Edini podatki, ki se lahko shranijo v tvojem brskalniku, so tehnično nujni za delovanje strani (na primer zaščita obrazca pred zlorabo). Teh ni mogoče izklopiti, ker brez njih stran ne deluje pravilno, in se ne uporabljajo za sledenje.</p>
<p>Če bom v prihodnje dodala analitiko ali druge storitve, ki uporabljajo piškotke, bom to stran posodobila in po potrebi prosila za privolitev.</p>
<p>Zadnja posodobitev: [datum].</p>"""},
    },
    "en": {
        "imprint": {"title": "Imprint", "html": """
<p><strong>BEEZEE.SI Katja Kolšek s.p.</strong> (sole proprietor)<br>[Address], [Postal code and town]<br>Slovenia</p>
<p>Registration number: [reg. no.]<br>Tax number: [tax no.]<br>VAT ID: [SI VAT ID, if applicable]</p>
<p>Email: <a href="mailto:katja@beezee.si">katja@beezee.si</a><br>Phone: <a href="tel:+38641449054">+386 41 449 054</a></p>
<p>Responsible for content: Katja Kolšek.</p>
<p>The logo and texts on this site belong to BEEZEE.SI Katja Kolšek s.p. Project screenshots belong to their respective owners and are shown as references.</p>"""},
        "privacy": {"title": "Privacy policy", "html": """
<p>The data controller is BEEZEE.SI Katja Kolšek s.p., [Address], [Postal code and town], Slovenia, <a href="mailto:katja@beezee.si">katja@beezee.si</a> ("I").</p>
<h2>What I process and why</h2>
<p><strong>Contact form.</strong> When you write to me through the form, I process your name, email address and message so I can reply. The legal basis is your consent (Art. 6(1)(a) GDPR) and pre-contractual steps (Art. 6(1)(b) GDPR). I keep messages for up to 2 years after our last contact unless they lead to a project.</p>
<p><strong>The hive (newsletter).</strong> When you join, I process your email address to send you the checklist and occasional news about new apps and projects. The legal basis is consent, which you confirm by clicking the link in the confirmation email (double opt-in). You can unsubscribe at any time via the link in every email or by writing to katja@beezee.si. The member list is stored on my own server (Neoserv, Slovenia); I do not use third-party newsletter tools.</p>
<p><strong>Server logs.</strong> The site is hosted by Neoserv (Slovenia). For technical and security reasons the server briefly logs the IP address, time of access and requested page. The legal basis is my legitimate interest (Art. 6(1)(f) GDPR).</p>
<h2>Who receives your data</h2>
<p>I do not sell data or share it with third parties other than my hosting provider, who act on my instructions and in line with the GDPR.</p>
<h2>Your rights</h2>
<p>You can request access to your data, rectification, erasure, restriction of processing or data portability, and withdraw consent at any time. Write to <a href="mailto:katja@beezee.si">katja@beezee.si</a>. You can also lodge a complaint with the Slovenian Information Commissioner (www.ip-rs.si).</p>
<p>Last updated: [date].</p>"""},
        "cookies": {"title": "Cookies", "html": """
<p>This site <strong>does not use tracking or advertising cookies</strong> and does not load analytics tools that would require your consent, which is why there is no cookie banner.</p>
<p>The only data that may be stored in your browser is strictly necessary for the site to work (for example, protecting the forms against abuse). It cannot be switched off because the site would not work properly without it, and it is not used for tracking.</p>
<p>If I add analytics or other cookie-based services in the future, I will update this page and ask for consent where required.</p>
<p>Last updated: [date].</p>"""},
    },
    "hr": {
        "imprint": {"title": "Impresum", "html": """
<p><strong>BEEZEE.SI Katja Kolšek s.p.</strong> (obrt)<br>[Adresa], [Poštanski broj i mjesto]<br>Slovenija</p>
<p>Matični broj: [matični broj]<br>Porezni broj: [porezni broj]<br>PDV ID: [SI PDV ID, ako postoji]</p>
<p>E-pošta: <a href="mailto:katja@beezee.si">katja@beezee.si</a><br>Telefon: <a href="tel:+38641449054">+386 41 449 054</a></p>
<p>Odgovorna osoba za sadržaj: Katja Kolšek.</p>
<p>Logotip i tekstovi na ovoj stranici vlasništvo su BEEZEE.SI Katja Kolšek s.p. Snimke zaslona projekata vlasništvo su njihovih vlasnika i prikazane su kao referenca.</p>"""},
        "privacy": {"title": "Politika privatnosti", "html": """
<p>Voditelj obrade osobnih podataka je BEEZEE.SI Katja Kolšek s.p., [Adresa], [Poštanski broj i mjesto], Slovenija, <a href="mailto:katja@beezee.si">katja@beezee.si</a> (dalje »ja«).</p>
<h2>Koje podatke obrađujem i zašto</h2>
<p><strong>Kontaktni obrazac.</strong> Kad mi pišeš putem obrasca, obrađujem tvoje ime, adresu e-pošte i sadržaj poruke kako bih ti mogla odgovoriti. Pravna osnova je tvoja privola (čl. 6(1)(a) GDPR) i radnje prije sklapanja ugovora (čl. 6(1)(b) GDPR). Poruke čuvam najviše 2 godine nakon zadnjeg kontakta, osim ako iz njih nastane suradnja.</p>
<p><strong>Košnica (newsletter).</strong> Prijavom obrađujem tvoju adresu e-pošte kako bih ti poslala kontrolni popis i povremene obavijesti o novim aplikacijama i projektima. Pravna osnova je privola, koju potvrđuješ klikom u e-poruci za potvrdu (dvostruka potvrda). Odjaviti se možeš bilo kada putem poveznice na dnu svake poruke ili porukom na katja@beezee.si. Popis članova čuvam na vlastitom poslužitelju (Neoserv, Slovenija); ne koristim vanjske alate za newsletter.</p>
<p><strong>Zapisi poslužitelja.</strong> Stranicu hostira Neoserv (Slovenija). Poslužitelj iz tehničkih i sigurnosnih razloga kratko bilježi IP adresu, vrijeme pristupa i traženu stranicu. Pravna osnova je moj legitimni interes (čl. 6(1)(f) GDPR).</p>
<h2>Kome prosljeđujem podatke</h2>
<p>Podatke ne prodajem i ne prosljeđujem trećim stranama, osim pružatelju hostinga, koji rade prema mojim uputama i u skladu s GDPR-om.</p>
<h2>Tvoja prava</h2>
<p>U svakom trenutku možeš zatražiti pristup svojim podacima, ispravak, brisanje, ograničenje obrade ili prijenos podataka te povući privolu. Piši na <a href="mailto:katja@beezee.si">katja@beezee.si</a>. Pritužbu možeš podnijeti Informacijskom povjereniku Republike Slovenije (www.ip-rs.si) ili AZOP-u u Hrvatskoj.</p>
<p>Zadnje ažuriranje: [datum].</p>"""},
        "cookies": {"title": "Kolačići", "html": """
<p>Ova stranica <strong>ne koristi kolačiće za praćenje ili oglašavanje</strong> i ne učitava alate za analitiku koji bi zahtijevali tvoju privolu, pa zato nema obavijesti o kolačićima.</p>
<p>Jedini podaci koji se mogu spremiti u tvoj preglednik tehnički su nužni za rad stranice (npr. zaštita obrasca od zlouporabe). Ne mogu se isključiti jer bez njih stranica ne radi ispravno i ne koriste se za praćenje.</p>
<p>Ako u budućnosti dodam analitiku ili druge usluge koje koriste kolačiće, ažurirat ću ovu stranicu i po potrebi zatražiti privolu.</p>
<p>Zadnje ažuriranje: [datum].</p>"""},
    },
}
