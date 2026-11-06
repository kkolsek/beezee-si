# beezee.si – nova statična stran

Stran je čist HTML/CSS z malo JavaScripta, zgrajena po vzoru lonc.app. Brez WordPressa, brez Reacta.

## Mape
- `src/` – izvor. **Tukaj se ureja.**
  - `content.py` – vsa besedila SL/EN/HR, projekti v portfoliu, pravne strani
  - `style.css` – ves slog (pisave, barve, odzivnost)
  - `main.js` – mobilni meni, filter portfolia, čebela vodnica, polnjenje korakov z medom, pošiljanje obrazcev brez osvežitve
  - `build.py` – iz zgornjega zgradi `dist/`
  - `kontakt.php`, `panj.php` – obrazca (e-pošta, MailerLite)
  - `config.example.php` – predloga za `config.php` (API ključ MailerLite, naslov za pošto)
  - `.htaccess` – https, brez www, preusmeritve starih WP poti, predpomnjenje
- `dist/` – **zgrajena stran, to gre na strežnik** (vsebina mape v `public_html` oz. v mapo poddomene test.beezee.si).

## Kako spremeniš besedilo
1. uredi `src/content.py`
2. zaženi `python3 src/build.py` (potrebuje samo Python 3; slike in pisave so že v `dist/assets`)
3. `git commit` + `git push` v GitHub (`kkolsek/beezee-si`)
4. v cPanelu → Git Version Control → beezee-si → **Update from Remote**, nato **Deploy HEAD Commit** – `.cpanel.yml` prekopira `dist/` na strežnik

## Git / objava
- repozitorij: https://github.com/kkolsek/beezee-si (privatni), v cPanelu kloniran v `/home/beezeesi/repositories/beezee-si`
- `.cpanel.yml` določa, kam se razporedi: zdaj `test.beezee.si` + doda noindex glavo
- **ob objavi v živo:** v `.cpanel.yml` nastavi `DEPLOYPATH=/home/beezeesi/public_html/`, zbriši vrstico s `printf` (noindex), v `src/.htaccess` dodaj preusmeritve pausie.si/getpausie.com → pausie.app in lonc.si → lonc.app, zgradi, push, deploy

## URL-ji
- `/` slovensko, `/en/` angleško, `/hr/` hrvaško (hreflang je nastavljen)
- `/zasebnost/`, `/piskotki/`, `/impresum/` (+ EN in HR različice)
- `/hvala/` – stran po oddaji obrazca brez JavaScripta (noindex)
- `/sitemap.xml`, `/robots.txt`

## Obrazci – kako delujeta
- **Kontakt** (`kontakt.php`): pošlje e-pošto na katja@beezee.si (PHP `mail()`), honeypot, največ 1 sporočilo / 30 s z istega IP.
- **Panj** (`panj.php`, samostojno, brez MailerLita): obiskovalcu pošlje potrditveno e-pošto s podpisano povezavo; po kliku shrani naslov v `beezee-panj/clani.csv` (ena raven NAD spletno mapo, torej izven javnega dostopa) in Katji pošlje obvestilo. Skrivni ključ za podpis se ustvari sam v `beezee-panj/.secret`.
- `config.php` ni obvezen. Če ga želiš: kopiraj `config.example.php` → `config.php` (pošiljatelj `contact_from` naj bo naslov na beezee.si, npr. noreply@beezee.si, da pošta ne pristane v spamu).
- Preveri, da PHP na gostovanju lahko pošilja pošto (`mail()`); Neoserv to običajno dovoli za naslove na lastni domeni.
- Pošiljanje sporočil članom: ko bo treba, dodamo preprost skript, ki prebere `clani.csv` in pošlje besedilo (ali uvoz CSV v katero koli orodje).

## Kar še manja (po vrsti)
- [ ] Impresum, zasebnost, piškotki: zamenjaj `[oglate oklepaje]` s pravimi podatki (naslov, matična, davčna, datum)
- [ ] preizkus obeh obrazcev na strežniku (pošta pride? potrditvena povezava dela?)
- [ ] kontrolni seznam PDF za Panj (povezava v potrditvenem/pozdravnem sporočilu)
- [ ] povezave na App Store / Google Play, ko bo Lonc objavljen (kartici zdaj vodita na lonc.app in pausie.app)
- [ ] podstrani projektov (študije primerov) – ko bodo posnetki zaslona in številke
- [ ] analitika: če Plausible, ni treba obvestila o piškotkih; če GA4, je treba dodati soglasje in posodobiti stran Piškotki

## Objava v živo (ko bo potrjeno)
1. v `public_html` **obdrži** obstoječe preusmeritve pausie.si / getpausie.com → pausie.app in lonc.si → lonc.app na vrhu `.htaccess`; pod njimi prilepi vsebino `dist/.htaccess` (brez bloka »Prihaja kmalu«)
2. prenesi vsebino `dist/` v `public_html`, dodaj `config.php`
3. odstrani `noindex` in robots Disallow s testne poddomene oz. jo ugasni
4. Search Console: nov sitemap `https://beezee.si/sitemap.xml`
