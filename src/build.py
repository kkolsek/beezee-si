#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zgradi statično stran beezee.si v mapo dist/.
Uporaba:  python3 build.py
Vsa besedila so v content.py, slog v style.css, skript v main.js."""
import os, shutil, html, datetime
from content import SITE, LANGS, PATHS, T, PROJECTS, FILTERS, LEGAL

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(HERE), "dist")
LOGO_Y = "/assets/img/logo-yellow.png"
LOGO_B = "/assets/img/logo-black.png"
TODAY = datetime.date.today().isoformat()

def esc(s): return html.escape(s, quote=True)
def L(p, lang):
    """Lokalizirano polje (string ali slovar po jezikih)."""
    return p[lang] if isinstance(p, dict) else p

# ---------------------------------------------------------------- deli strani
def head(lang, t, title, desc, path, alt_paths, noindex=False):
    hreflang = "".join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (l, SITE, alt_paths[l]) for l in LANGS)
    hreflang += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, alt_paths["sl"])
    robots = '<meta name="robots" content="noindex,follow">\n' if noindex else ""
    jsonld = ""
    if path == PATHS[lang]["home"]:
        jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
 {"@type":"Person","@id":"%(s)s/#katja","name":"Katja Kolšek","url":"%(s)s/","email":"mailto:katja@beezee.si","telephone":"+38641449054","jobTitle":"Web & app developer","sameAs":["https://www.linkedin.com/in/katja-kolsek/"]},
 {"@type":"ProfessionalService","@id":"%(s)s/#beezee","name":"BEEZEE","legalName":"BEEZEE.SI Katja Kolšek s.p.","url":"%(s)s/","logo":"%(s)s/assets/img/logo-yellow.png","image":"%(s)s/assets/img/og.png","email":"katja@beezee.si","telephone":"+38641449054","founder":{"@id":"%(s)s/#katja"},"areaServed":["SI","HR","EU"],"knowsLanguage":["sl","en","hr"],"address":{"@type":"PostalAddress","addressCountry":"SI"}},
 {"@type":"WebSite","@id":"%(s)s/#site","url":"%(s)s/","name":"BEEZEE","inLanguage":"%(l)s","publisher":{"@id":"%(s)s/#beezee"}}
]}
</script>
""" % {"s": SITE, "l": lang}
    return """<!DOCTYPE html>
<html lang="%(hl)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(robots)s<link rel="canonical" href="%(site)s%(path)s">
%(hreflang)s<meta property="og:type" content="website">
<meta property="og:site_name" content="BEEZEE">
<meta property="og:locale" content="%(ogl)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(site)s%(path)s">
<meta property="og:image" content="%(site)s/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFDD55">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/baloo-2-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/dm-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
%(jsonld)s</head>
<body>
""" % {"hl": t["htmlLang"], "title": esc(title), "desc": esc(desc), "robots": robots, "site": SITE, "path": path,
       "hreflang": hreflang, "ogl": t["ogLocale"], "jsonld": jsonld}

def bee():
    return """<div class="bee" id="bee" aria-hidden="true"><div class="bee-flip"><div class="bee-body"><span class="wing wing-l"></span><span class="wing wing-r"></span><img src="%s" alt="" width="56" height="56"></div></div></div>
""" % LOGO_Y

def header(lang, t, alt_paths, home):
    """home = pot domače strani v tem jeziku (sidra kažejo nanjo, da delujejo tudi s podstrani)."""
    nav = [("#delo", t["navWork"]), ("#storitve", t["navServices"]), ("#o-meni", t["navAbout"]), ("#panj", t["navHive"]), ("#kontakt", t["navContact"])]
    links = "".join('<a href="%s%s">%s</a>' % (home, h, esc(n)) for h, n in nav)
    lang_links = "".join('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (alt_paths[l], l, l, ' aria-current="page"' if l == lang else "", l.upper()) for l in LANGS)
    return """<header class="site-header">
  <div class="wrap">
    <a class="brand" href="%(home)s"><img src="%(logo)s" alt="" width="40" height="40"><span>BEEZEE</span></a>
    <nav class="main-nav" aria-label="%(mainNav)s">%(links)s</nav>
    <div class="head-right">
      <nav class="lang" aria-label="%(langLabel)s">%(lang)s</nav>
      <a class="btn btn-ink btn-sm head-cta" href="%(home)s#kontakt">%(cta)s</a>
      <button class="burger" id="burger" type="button" aria-label="%(menu)s" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <div class="top"><span>BEEZEE</span><button type="button" class="close">%(close)s</button></div>
  <nav aria-label="%(menu)s">%(links)s</nav>
  <a class="btn btn-ink" href="%(home)s#kontakt">%(cta)s</a>
</div>
""" % {"home": home, "logo": LOGO_Y, "mainNav": esc(t["mainNav"]), "links": links, "langLabel": esc(t["langLabel"]), "lang": lang_links,
       "cta": esc(t["ctaWrite"]), "menu": esc(t["menu"]), "close": esc(t["close"])}

def footer(lang, t, home):
    p = PATHS[lang]
    nav = [("#delo", t["navWork"]), ("#storitve", t["navServices"]), ("#o-meni", t["navAbout"]), ("#panj", t["navHive"]), ("#kontakt", t["navContact"])]
    links = "".join('<a href="%s%s">%s</a>' % (home, h, esc(n)) for h, n in nav)
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="foot-brand"><img src="%(logo)s" alt="" width="30" height="30"><div><strong>BEEZEE</strong><br><span>%(legal)s</span></div></div>
    <nav class="foot-nav" aria-label="%(footNav)s">%(links)s</nav>
    <div class="foot-legal"><span>SL · EN · HR</span><a href="%(privacy)s">%(privacyL)s</a><a href="%(cookies)s">%(cookiesL)s</a><a href="%(imprint)s">%(imprintL)s</a></div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
""" % {"logo": LOGO_B, "legal": esc(t["footLegal"]), "footNav": esc(t["footNav"]), "links": links,
       "privacy": p["privacy"], "privacyL": esc(t["privacy"]), "cookies": p["cookies"], "cookiesL": esc(t["cookies"]), "imprint": p["imprint"], "imprintL": esc(t["imprint"])}

def comb(with_labels=True):
    """Satovje iz 7 celic (hero in okno v razdelku O meni)."""
    if with_labels:
        return """<div class="cell cell-honey c1"><img src="%s" alt="" width="86" height="86"></div>
<div class="cell cell-stripes c2"><span class="tag">astor.si</span></div>
<div class="cell cell-stripes c3"><span class="tag">dingogear.si</span></div>
<div class="cell cell-ink c4"><div class="mini">Lonc</div></div>
<div class="cell cell-stripes c5"><span class="tag">tropidog.si</span></div>
<div class="cell cell-amber c6"><div class="mini">Pausie</div></div>
<div class="cell cell-stripes c7"><span class="tag">DPD · GLS</span></div>""" % LOGO_B
    return """<div class="cell cell-honey c1"><img src="%s" alt="" width="86" height="86"></div>
<div class="cell cell-amber c2"></div><div class="cell cell-pale c3"></div><div class="cell cell-pale c4"></div>
<div class="cell cell-amber c5"></div><div class="cell cell-pale c6"></div><div class="cell cell-amber c7"></div>""" % LOGO_B

def card(p, lang, t):
    name = L(p["name"], lang); url = L(p["url"], lang); desc = p["d"][lang]; cat = t[p["catKey"]]
    tag = "a" if p["href"] else "div"
    href = ' href="%s" target="_blank" rel="noopener"' % p["href"] if p["href"] else ""
    if p["type"] == "web":
        visual = """<div class="browser"><div class="bar"><i></i><i></i><i></i><b>%s</b></div><img src="/assets/img/%s-s.webp" alt="" width="440" height="197" loading="lazy"></div>""" % (esc(url), p["img"])
    elif p["type"] == "app":
        visual = """<div class="stage">
  <div class="browser"><div class="bar"><i></i><i></i><i></i><b>%(u)s</b></div><img src="/assets/img/%(i)s-s.webp" alt="" width="440" height="204" loading="lazy"></div>
  <div class="phone"><img src="/assets/img/%(i)s-phone.webp" alt="" width="240" height="480" loading="lazy"></div>
  <div class="badges"><span>App Store</span><span>Google Play</span></div>
</div>""" % {"u": esc(url), "i": p["img"]}
    else:
        visual = """<div class="dash"><div class="bar"><i></i><b>%s</b></div><div class="lines"><span style="width:70%%"></span><span style="width:85%%"></span><span style="width:55%%"></span><div class="act"><span>%s</span><span>%s</span></div></div></div>""" % (esc(url), esc(t["printLabel"]), esc(p.get("ph", "")))
    return """<%(tag)s class="hex hex-%(type)s" data-cat="%(cat)s"%(href)s aria-label="%(name)s – %(catL)s">
  <div class="hex-in">%(visual)s
    <div class="band"><div class="t"><strong>%(name)s</strong><span class="cat">%(catL)s</span></div><p>%(desc)s</p></div>
  </div>
</%(tag)s>""" % {"tag": tag, "type": p["type"], "cat": p["cat"], "href": href, "name": esc(name), "catL": esc(cat), "visual": visual, "desc": esc(desc)}

def rows_html(lang, t):
    cards = [card(p, lang, t) for p in PROJECTS]
    out, i, n = [], 0, 3
    while i < len(cards):
        out.append('<div class="row">\n' + "\n".join(cards[i:i + n]) + '\n</div>')
        i += n; n = 2 if n == 3 else 3
    return "\n".join(out)

def home_page(lang):
    t = T[lang]; p = PATHS[lang]; home = p["home"]
    alt = {l: PATHS[l]["home"] for l in LANGS}
    filters = "".join('<button type="button" class="pill" data-filter="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "all" else "false", esc(t[lk])) for k, lk in FILTERS)
    needs = "".join('<label><input type="checkbox" name="potrebujem[]" value="%s">%s</label>' % (esc(t[k]), esc(t[k])) for k in ["s1", "s2", "s3", "s4"])
    tabs = "".join('<span class="t" style="--w:%dpx"></span>' % w for w in [44, 40, 36, 32, 28, 24, 20, 16, 12] + [10] * 9)
    body = """%(bee)s%(header)s
<main id="top">
<section class="hero" id="hero">
  <div class="hexbg" aria-hidden="true"></div>
  <div class="wrap hero-wrap">
    <div class="hero-text">
      <span class="hand sticker-hi">%(stickerHi)s</span>
      <h1>%(heroTitle)s</h1>
      <p>%(heroSub)s</p>
      <div class="hero-cta">
        <a class="btn btn-honey" href="#delo">%(ctaWork)s</a>
        <a class="btn-outline" href="#kontakt"><span>%(ctaWrite)s</span></a>
        <span class="hand sticker-cta" data-bee-spot="hero" aria-hidden="true">%(stickerCta)s</span>
      </div>
    </div>
    <div class="comb" aria-hidden="true">
      <div class="comb-path"></div>
      %(comb)s
      <span class="hand sticker-mine">%(sticker1)s</span>
    </div>
  </div>
</section>

<section class="services" id="storitve">
  <div class="wrap">
    <div class="head center">
      <h2 class="sec">%(servicesH)s</h2>
      <p class="sub">%(servicesSub)s</p>
      <span class="bee-spot" data-bee-spot="services" style="left:calc(50%% + 150px);top:-30px" aria-hidden="true"></span>
    </div>
    <div class="hexrow">
      <div class="svc"><div class="svc-in"><div class="ico-site" aria-hidden="true"></div><h3>%(s1)s</h3><p>%(s1d)s</p></div></div>
      <div class="svc svc-honey"><div class="svc-in"><div class="ico-shop" aria-hidden="true"></div><h3>%(s2)s</h3><p>%(s2d)s</p></div><span class="hand sticker-sweet" aria-hidden="true">%(sticker2)s</span></div>
      <div class="svc"><div class="svc-in"><div class="ico-plug" aria-hidden="true"><div class="pins"><span></span><span></span></div><div class="box"></div></div><h3>%(s3)s</h3><p>%(s3d)s</p></div></div>
      <div class="svc"><div class="svc-in"><div class="ico-app" aria-hidden="true"><span></span></div><h3>%(s4)s</h3><p>%(s4d)s</p></div></div>
    </div>
  </div>
</section>

<section class="work" id="delo">
  <div class="hexbg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="work-head">
      <div>
        <h2 class="sec">%(workH)s</h2>
        <p class="sub">%(workSub)s</p>
        <span class="bee-spot" data-bee-spot="work" style="right:-70px;top:-20px" aria-hidden="true"></span>
      </div>
      <div class="filters" role="group" aria-label="%(filterLabel)s">%(filters)s</div>
    </div>
    <div class="grid" id="grid">
%(rows)s
    </div>
    <p class="empty" id="empty">%(empty)s</p>
  </div>
</section>

<section class="about" id="o-meni">
  <div class="about-wrap">
    <div class="tabs-mock" aria-hidden="true">
      <div class="tabs-win">
        <div class="tabs-bar"><span class="dot"></span><span class="tab"></span>%(tabs)s<span class="lbl">%(tabsLabel)s</span></div>
        <div class="tabs-body"><div class="lines"><span></span><span></span><span></span></div><div class="tabs-comb">%(comb2)s</div></div>
      </div>
      <span class="hand sticker-me">← %(stickerMe)s</span>
      <span class="bee-spot" data-bee-spot="about" style="left:-30px;top:10px"></span>
    </div>
    <div class="about-text">
      <h2 class="sec">%(aboutH)s</h2>
      <p>%(about1)s</p>
      <p class="second">%(about2)s</p>
      <span class="signature">%(signature)s</span>
    </div>
  </div>
</section>

<section class="process" id="kako">
  <div class="wrap">
    <div class="head center">
      <h2 class="sec">%(processH)s</h2>
      <p class="sub">%(processSub)s</p>
      <span class="bee-spot" data-bee-spot="process" style="left:calc(50%% - 200px);top:-10px" aria-hidden="true"></span>
    </div>
    <div class="steps" id="steps">
      <div class="path" aria-hidden="true"></div><div class="path path2" aria-hidden="true"></div>
      <ol class="steps-grid" style="list-style:none;padding:0;margin:0">
        <li class="step"><div class="stephex"><div class="fill"></div><span>1</span></div><div><h3>%(p1)s</h3><p>%(p1d)s</p></div></li>
        <li class="step"><div class="stephex"><div class="fill"></div><span>2</span></div><div><h3>%(p2)s</h3><p>%(p2d)s</p></div></li>
        <li class="step"><div class="stephex"><div class="fill"></div><span>3</span></div><div><h3>%(p3)s</h3><p>%(p3d)s</p></div></li>
        <li class="step"><div class="stephex"><div class="fill"></div><span>4</span></div><div><h3>%(p4)s</h3><p>%(p4d)s</p></div></li>
      </ol>
    </div>
  </div>
</section>

<section class="hive" id="panj">
  <div class="hexbg h1" aria-hidden="true"></div><div class="hexbg h2" aria-hidden="true"></div><div class="hexbg h3" aria-hidden="true"></div>
  <div class="doc" aria-hidden="true">
    <img src="%(logoB)s" alt="" width="26" height="26"><strong>%(hiveDoc)s</strong><small>%(hiveDocSub)s</small>
    <div class="chk"><span><i class="on"></i><b></b></span><span><i class="on"></i><b></b></span><span><i></i><b></b></span><span><i></i><b></b></span><span><i></i><b></b></span></div>
  </div>
  <div class="hive-wrap">
    <span class="hand sticker-hive" aria-hidden="true">%(stickerHive)s</span>
    <span class="bee-spot" data-bee-spot="hive" style="left:calc(50%% + 180px);top:0" aria-hidden="true"></span>
    <h2>%(hiveH)s</h2>
    <p class="lead">%(hiveText)s</p>
    <div class="gifts"><span>%(hiveGift1)s</span><span>%(hiveGift2)s</span></div>
    <form class="hive-form" id="hive-form" action="/panj.php" method="post" data-sending="%(sending)s" data-thanks="%(hiveThanks)s" data-error="%(hiveError)s">
      <input type="hidden" name="lang" value="%(lang)s">
      <input type="hidden" name="cas" value="">
      <label class="hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
      <label><span class="sr-only">%(lEmail)s</span><input type="email" name="email" required placeholder="%(emailPh)s" autocomplete="email"></label>
      <button type="submit" class="btn btn-honey">%(join)s</button>
    </form>
    <p class="hive-note" id="hive-note">%(hiveNote)s</p>
    <p class="hive-msg" id="hive-msg" hidden></p>
  </div>
</section>

<section class="contact" id="kontakt">
  <div class="contact-wrap">
    <div class="contact-info">
      <h2>%(contactH)s</h2>
      <span class="bee-spot" data-bee-spot="contact" style="left:300px;top:-10px" aria-hidden="true"></span>
      <p class="lead">%(contactSub)s</p>
      <p class="or">%(orWrite)s<br><a href="mailto:katja@beezee.si">katja@beezee.si</a></p>
      <div class="contact-links">
        <a href="tel:+38641449054"><span class="ico ico-phone" aria-hidden="true"></span>%(phone)s</a>
        <a href="https://www.linkedin.com/in/katja-kolsek/" target="_blank" rel="noopener"><span class="ico ico-in" aria-hidden="true">in</span>%(linkedin)s</a>
      </div>
    </div>
    <form class="form" id="contact-form" action="/kontakt.php" method="post" data-sending="%(sending)s" data-error="%(sentError)s">
      <input type="hidden" name="lang" value="%(lang)s">
      <label class="hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
      <div class="two">
        <label class="f">%(lName)s<input type="text" name="ime" required autocomplete="name"></label>
        <label class="f">%(lEmail)s<input type="email" name="email" required autocomplete="email"></label>
      </div>
      <fieldset><legend>%(lNeed)s</legend><div class="needs">%(needs)s</div></fieldset>
      <label class="f">%(lMsg)s<textarea name="sporocilo" rows="5" required placeholder="%(msgPh)s"></textarea></label>
      <label class="consent"><input type="checkbox" name="soglasje" value="1" required>%(consent)s</label>
      <p class="form-msg" id="contact-msg" hidden></p>
      <button type="submit" class="btn btn-honey">%(send)s</button>
    </form>
    <div class="sent-box" id="sent-box" role="status">%(sent)s</div>
  </div>
</section>
</main>
%(footer)s""" % dict(
        {k: esc(v) for k, v in t.items()},
        bee=bee(), header=header(lang, t, alt, home), footer=footer(lang, t, home), comb=comb(True), comb2=comb(False),
        filters=filters, rows=rows_html(lang, t), tabs=tabs, needs=needs, lang=lang, logoB=LOGO_B)
    return head(lang, t, t["metaTitle"], t["metaDesc"], home, alt) + body

def sub_page(lang, key, title, inner, noindex=False, cls=""):
    t = T[lang]; p = PATHS[lang]; home = p["home"]
    alt = {l: PATHS[l][key] for l in LANGS}
    body = """%(header)s
<main class="page %(cls)s">
  <div class="wrap">
    <a class="back" href="%(home)s">%(back)s</a>
    <h1>%(title)s</h1>
    %(inner)s
  </div>
</main>
%(footer)s""" % {"header": header(lang, t, alt, home), "footer": footer(lang, t, home), "home": home, "back": esc(t["backHome"]), "title": esc(title), "inner": inner, "cls": cls}
    return head(lang, t, title + " | BEEZEE", t["metaDesc"], p[key], alt, noindex=noindex) + body

def write(rel, content):
    full = os.path.join(DIST, rel.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

# ---------------------------------------------------------------- build
def main():
    os.makedirs(DIST, exist_ok=True)
    for sub in ("assets/css", "assets/js"): os.makedirs(os.path.join(DIST, sub), exist_ok=True)
    shutil.copy(os.path.join(HERE, "style.css"), os.path.join(DIST, "assets/css/style.css"))
    shutil.copy(os.path.join(HERE, "main.js"), os.path.join(DIST, "assets/js/main.js"))
    for php in ("kontakt.php", "panj.php", "config.example.php", ".htaccess"):
        src = os.path.join(HERE, php)
        if os.path.exists(src): shutil.copy(src, os.path.join(DIST, php))

    urls = []
    for lang in LANGS:
        p = PATHS[lang]; t = T[lang]
        write(p["home"] + "index.html", home_page(lang)); urls.append((p["home"], "1.0"))
        for key in ("privacy", "cookies", "imprint"):
            lg = LEGAL[lang][key]
            write(p[key] + "index.html", sub_page(lang, key, lg["title"], lg["html"])); urls.append((p[key], "0.3"))
        thanks = '<p>%s</p><h2>%s</h2><p>%s</p>' % (esc(t["thanksText"]), esc(t["thanksHiveTitle"]), esc(t["thanksHiveText"]))
        write(p["thanks"] + "index.html", sub_page(lang, "thanks", t["thanksTitle"], thanks, noindex=True, cls="thanks"))
        write(p["welcome"] + "index.html", sub_page(lang, "welcome", t["welcomeTitle"], "<p>%s</p>" % esc(t["welcomeText"]), noindex=True, cls="thanks"))

    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang in LANGS:
        for key in ("home", "privacy", "cookies", "imprint"):
            alts = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l, SITE, PATHS[l][key]) for l in LANGS)
            sm.append('<url><loc>%s%s</loc><lastmod>%s</lastmod>%s</url>' % (SITE, PATHS[lang][key], TODAY, alts))
    sm.append('</urlset>')
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", "User-agent: *\nAllow: /\nDisallow: /hvala/\nDisallow: /en/thanks/\nDisallow: /hr/hvala/\nDisallow: /panj/\nDisallow: /en/hive/\nDisallow: /hr/kosnica/\nSitemap: %s/sitemap.xml\n" % SITE)
    print("OK ->", DIST)

if __name__ == "__main__":
    main()
