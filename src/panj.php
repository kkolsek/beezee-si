<?php
/**
 * beezee.si – prijava v Panj z dvojno potrditvijo.
 *
 * A) samostojno (privzeto): pošlje potrditveno e-pošto s podpisano povezavo; po kliku shrani naslov
 *    v CSV izven spletne mape, članu pošlje pozdravno e-pošto s kontrolnim seznamom in obvesti Katjo.
 * B) MailerLite: če sta v config.php 'mailerlite_key' + 'mailerlite_group', doda naročnika (status unconfirmed).
 *
 * E-pošta je HTML (BEEZEE slog) + navadno besedilo (multipart/alternative).
 */
declare(strict_types=1);
header('X-Content-Type-Options: nosniff');

$config = file_exists(__DIR__ . '/config.php') ? require __DIR__ . '/config.php' : [];
$owner  = $config['contact_to']   ?? 'katja@beezee.si';
$from   = $config['contact_from'] ?? 'noreply@beezee.si';
$mlKey  = $config['mailerlite_key']   ?? '';
$mlGrp  = $config['mailerlite_group'] ?? '';
$dataDir = $config['panj_dir'] ?? dirname(__DIR__) . '/beezee-panj';   // izven spletne mape
$siteUrl = rtrim($config['site_url'] ?? ('https://' . ($_SERVER['HTTP_HOST'] ?? 'beezee.si')), '/');

$PATHS = [
    'sl' => ['thanks' => '/hvala/',     'welcome' => '/panj/dobrodosli/',       'home' => '/#panj'],
    'en' => ['thanks' => '/en/thanks/', 'welcome' => '/en/hive/welcome/',       'home' => '/en/#panj'],
    'hr' => ['thanks' => '/hr/hvala/',  'welcome' => '/hr/kosnica/dobrodosli/', 'home' => '/hr/#panj'],
];

/* ---------- besedila e-pošte ---------- */
$MAIL = [
    'sl' => [
        'confirm' => [
            'subject' => 'Potrdi prijavo v panj',
            'sticker' => 'še en korak',
            'title'   => 'Še en klik in si v panju.',
            'text'    => ['Potrdi prijavo in takoj dobiš kontrolni seznam pred prenovo spletne strani.', 'Če se nisi prijavil/-a ti, to sporočilo preprosto prezri.'],
            'button'  => 'Potrdi prijavo',
        ],
        'welcome' => [
            'subject' => 'Bzzz, potrjeno – tukaj je tvoj kontrolni seznam',
            'sticker' => 'dobrodošli v panju',
            'title'   => 'Bzzz, potrjeno!',
            'text'    => ['Hvala, da si se pridružil/-a. Obljubljeni kontrolni seznam pred prenovo spletne strani te čaka spodaj.', 'Brez rednih novic. Oglasim se samo, ko imam nekaj, kar ti bo koristilo. Odjava kadar koli z odgovorom na to sporočilo.'],
            'button'  => 'Prenesi kontrolni seznam',
            'pdf'     => '/assets/pdf/beezee-kontrolni-seznam-sl.pdf',
        ],
        'fallback' => 'Če gumb ne deluje, kopiraj to povezavo v brskalnik:',
        'footer'   => 'BEEZEE.SI Katja Kolšek s.p. · beezee.si',
    ],
    'en' => [
        'confirm' => [
            'subject' => 'Confirm your hive subscription',
            'sticker' => 'one more step',
            'title'   => "One click and you're in the hive.",
            'text'    => ["Confirm your subscription and you'll get the website redesign checklist right away.", "If you didn't sign up, just ignore this email."],
            'button'  => 'Confirm subscription',
        ],
        'welcome' => [
            'subject' => "Bzzz, confirmed – here's your checklist",
            'sticker' => 'welcome to the hive',
            'title'   => 'Bzzz, confirmed!',
            'text'    => ['Thanks for joining. The promised website redesign checklist is waiting for you below.', 'No regular newsletter. I only get in touch when I have something useful for you. Unsubscribe any time by replying to this email.'],
            'button'  => 'Download the checklist',
            'pdf'     => '/assets/pdf/beezee-kontrolni-seznam-en.pdf',
        ],
        'fallback' => "If the button doesn't work, copy this link into your browser:",
        'footer'   => 'BEEZEE.SI Katja Kolšek s.p. · beezee.si',
    ],
    'hr' => [
        'confirm' => [
            'subject' => 'Potvrdi prijavu u košnicu',
            'sticker' => 'još jedan korak',
            'title'   => 'Još jedan klik i u košnici si.',
            'text'    => ['Potvrdi prijavu i odmah dobivaš kontrolni popis prije redizajna web stranice.', 'Ako se nisi prijavio/-la ti, zanemari ovu poruku.'],
            'button'  => 'Potvrdi prijavu',
        ],
        'welcome' => [
            'subject' => 'Bzzz, potvrđeno – evo tvog kontrolnog popisa',
            'sticker' => 'dobrodošli u košnicu',
            'title'   => 'Bzzz, potvrđeno!',
            'text'    => ['Hvala što si se pridružio/-la. Obećani kontrolni popis prije redizajna web stranice čeka te ispod.', 'Bez redovitih novosti. Javim se samo kad imam nešto što će ti koristiti. Odjava bilo kada odgovorom na ovu poruku.'],
            'button'  => 'Preuzmi kontrolni popis',
            'pdf'     => '/assets/pdf/beezee-kontrolni-seznam-hr.pdf',
        ],
        'fallback' => 'Ako gumb ne radi, kopiraj ovu poveznicu u preglednik:',
        'footer'   => 'BEEZEE.SI Katja Kolšek s.p. · beezee.si',
    ],
];

$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && str_contains($_SERVER['HTTP_ACCEPT'], 'application/json');

function respond(bool $ok, string $redirect, bool $json, string $msg = ''): never {
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'msg' => $msg], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: ' . $redirect . ($ok ? '' : (str_contains($redirect, '?') ? '&' : '?') . 'napaka=1'), true, 303);
    }
    exit;
}

/** HTML predloga v BEEZEE slogu (tabele + inline slogi, da deluje v Outlooku in Gmailu). */
function mailHtml(array $m, string $url, string $lang, string $siteUrl, string $fallback, string $footer): string {
    $e = static fn(string $s): string => htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
    $paras = '';
    foreach ($m['text'] as $i => $p) {
        $color = $i === 0 ? '#141414' : '#6B6459';
        $paras .= '<p style="margin:0 0 14px;font:16px/1.6 \'DM Sans\',Helvetica,Arial,sans-serif;color:' . $color . ';">' . $e($p) . '</p>';
    }
    $img = $siteUrl . '/assets/img/satje.png';
    return '<!DOCTYPE html><html lang="' . $lang . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        . '<meta name="color-scheme" content="light">'
        . '<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700&family=Caveat:wght@700&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet"><title>' . $e($m['subject']) . '</title></head>'
        . '<body style="margin:0;padding:0;background:#F3E6C4;">'
        . '<div style="display:none;max-height:0;overflow:hidden;">' . $e($m['text'][0]) . '</div>'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F3E6C4;"><tr><td align="center" style="padding:28px 12px;">'
        . '<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="width:100%;max-width:560px;background:#FFF8E7;border:1px solid #E6DCC4;border-radius:14px;">'
        // glava
        . '<tr><td style="padding:22px 32px 18px;border-bottom:2px dashed #E6DCC4;">'
        . '<table role="presentation" cellpadding="0" cellspacing="0"><tr>'
        . '<td style="vertical-align:middle;"><img src="' . $e($img) . '" width="67" height="51" alt="" style="display:block;border:0;"></td>'
        . '<td style="vertical-align:middle;padding-left:12px;font:700 20px \'Baloo 2\',Helvetica,Arial,sans-serif;letter-spacing:.06em;color:#141414;">BEEZEE</td>'
        . '</tr></table></td></tr>'
        // vsebina
        . '<tr><td style="padding:30px 32px 8px;">'
        . '<p style="margin:0 0 6px;font:italic 700 20px \'Caveat\',Georgia,serif;color:#6B6459;">' . $e($m['sticker']) . '</p>'
        . '<h1 style="margin:0 0 18px;font:700 30px/1.15 \'Baloo 2\',Helvetica,Arial,sans-serif;color:#141414;">' . $e($m['title']) . '</h1>'
        . $paras
        // gumb
        . '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:10px 0 22px;"><tr>'
        . '<td style="background:#FFDD55;border-radius:10px;border:2px solid #141414;">'
        . '<a href="' . $e($url) . '" style="display:inline-block;padding:14px 28px;font:700 16px \'DM Sans\',Helvetica,Arial,sans-serif;color:#141414;text-decoration:none;">' . $e($m['button']) . '</a>'
        . '</td></tr></table>'
        . '<p style="margin:0 0 6px;font:12px/1.5 Helvetica,Arial,sans-serif;color:#6B6459;">' . $e($fallback) . '<br>'
        . '<a href="' . $e($url) . '" style="color:#6B6459;word-break:break-all;">' . $e($url) . '</a></p>'
        . '<p style="margin:22px 0 26px;"><img src="' . $e($siteUrl . '/assets/img/podpis.png') . '" width="82" height="40" alt="Katja" style="display:block;border:0;"></p>'
        . '</td></tr>'
        // noga
        . '<tr><td style="background:#141414;border-radius:0 0 13px 13px;padding:14px 32px;font:12px Helvetica,Arial,sans-serif;color:#B8B0A3;">'
        . '<a href="' . $e($siteUrl) . '" style="color:#FFDD55;text-decoration:none;font-weight:700;">beezee.si</a> &nbsp;·&nbsp; BEEZEE.SI Katja Kolšek s.p.'
        . '</td></tr>'
        . '</table></td></tr></table></body></html>';
}

function mailText(array $m, string $url): string {
    return $m['title'] . "\n\n" . implode("\n\n", $m['text']) . "\n\n" . $m['button'] . ":\n" . $url . "\n\nKatja\nbeezee.si\n";
}

function sendMail(string $to, string $subject, string $text, string $from, string $replyTo = '', string $html = ''): bool {
    $h = ['From: BEEZEE <' . $from . '>', 'MIME-Version: 1.0', 'X-Mailer: beezee.si'];
    if ($replyTo !== '') { $h[] = 'Reply-To: ' . $replyTo; }
    if ($html === '') {
        $h[] = 'Content-Type: text/plain; charset=UTF-8';
        $body = $text;
    } else {
        $b = 'bz_' . bin2hex(random_bytes(8));
        $h[] = 'Content-Type: multipart/alternative; boundary="' . $b . '"';
        $body = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text))
              . "--$b\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html))
              . "--$b--\r\n";
    }
    return @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $h));
}

function secret(string $dir, array $config): string {
    if (!empty($config['secret'])) { return (string)$config['secret']; }
    if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
    $f = $dir . '/.secret';
    if (!file_exists($f)) { @file_put_contents($f, bin2hex(random_bytes(32))); @chmod($f, 0600); }
    return (string)@file_get_contents($f);
}
function token(string $email, string $lang, string $secret): string {
    return hash_hmac('sha256', strtolower($email) . '|' . $lang, $secret);
}

$lang = $_POST['lang'] ?? $_GET['lang'] ?? 'sl';
if (!isset($PATHS[$lang])) { $lang = 'sl'; }
$L = $MAIL[$lang];

/* ---------- predogled e-pošte: /panj.php?predogled=confirm|welcome&lang=sl ---------- */
if (isset($_GET['predogled']) && in_array($_GET['predogled'], ['confirm', 'welcome'], true)) {
    header('Content-Type: text/html; charset=utf-8');
    header('X-Robots-Tag: noindex');
    $m = $L[$_GET['predogled']];
    $url = isset($m['pdf']) ? $siteUrl . $m['pdf'] : $siteUrl . '/panj.php?primer=1';
    echo mailHtml($m, $url, $lang, $siteUrl, $L['fallback'], $L['footer']);
    exit;
}

/* ---------- potrditev (GET ?potrdi=...) ---------- */
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['potrdi'], $_GET['t'])) {
    $email = (string)base64_decode(strtr((string)$_GET['potrdi'], '-_', '+/'), true);
    if (!filter_var($email, FILTER_VALIDATE_EMAIL) || !hash_equals(token($email, $lang, secret($dataDir, $config)), (string)$_GET['t'])) {
        header('Location: ' . $PATHS[$lang]['home'] . '?napaka=potrditev', true, 303); exit;
    }
    if (!is_dir($dataDir)) { @mkdir($dataDir, 0700, true); }
    $file = $dataDir . '/clani.csv';
    $exists = false;
    if (file_exists($file)) {
        foreach (file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [] as $line) {
            if (stripos($line, strtolower($email) . ';') === 0) { $exists = true; break; }
        }
    }
    if (!$exists) {
        $fh = fopen($file, 'a');
        if ($fh) {
            if (filesize($file) === 0) { fwrite($fh, "email;jezik;potrjeno;ip\n"); }
            fwrite($fh, strtolower($email) . ';' . $lang . ';' . date('Y-m-d H:i:s') . ';' . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n");
            fclose($fh);
        }
        $w = $L['welcome']; $pdf = $siteUrl . $w['pdf'];
        sendMail($email, $w['subject'], mailText($w, $pdf), $from, $owner, mailHtml($w, $pdf, $lang, $siteUrl, $L['fallback'], $L['footer']));
        sendMail($owner, '[beezee.si] Nov član panja: ' . $email, "Nov potrjen član panja.\n\nE-pošta: $email\nJezik: $lang\nČas: " . date('Y-m-d H:i:s') . "\n\nSeznam: $file\n", $from);
    }
    header('Location: ' . $PATHS[$lang]['welcome'], true, 303); exit;
}

/* ---------- prijava (POST) ---------- */
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { respond(false, $PATHS[$lang]['home'], $wantsJson, 'method'); }
if (!empty($_POST['website'])) { respond(true, $PATHS[$lang]['thanks'], $wantsJson); } // honeypot

$email = trim((string)($_POST['email'] ?? ''));
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 200) { respond(false, $PATHS[$lang]['home'], $wantsJson, 'validation'); }

// omejitev: 1 prijava na 30 s z istega IP
$lock = sys_get_temp_dir() . '/beezee-panj-' . md5($_SERVER['REMOTE_ADDR'] ?? '0');
if (file_exists($lock) && time() - filemtime($lock) < 30) { respond(false, $PATHS[$lang]['home'], $wantsJson, 'rate'); }
touch($lock);

if ($mlKey !== '' && $mlGrp !== '') {
    /* ---- B) MailerLite ---- */
    $payload = json_encode(['email' => $email, 'groups' => [$mlGrp], 'status' => 'unconfirmed', 'fields' => ['language' => $lang],
        'ip_address' => $_SERVER['REMOTE_ADDR'] ?? null, 'optin_ip' => $_SERVER['REMOTE_ADDR'] ?? null]);
    $ch = curl_init('https://connect.mailerlite.com/api/subscribers');
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $payload, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'Accept: application/json', 'Authorization: Bearer ' . $mlKey]]);
    $res = curl_exec($ch); $code = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE); curl_close($ch);
    $ok = $res !== false && in_array($code, [200, 201], true);
    respond($ok, $ok ? $PATHS[$lang]['thanks'] : $PATHS[$lang]['home'], $wantsJson, $ok ? 'joined' : 'api:' . $code);
}

/* ---- A) samostojno: potrditvena e-pošta ---- */
$c = $L['confirm'];
$link = $siteUrl . '/panj.php?potrdi=' . rtrim(strtr(base64_encode($email), '+/', '-_'), '=') . '&t=' . token($email, $lang, secret($dataDir, $config)) . '&lang=' . $lang;
$ok = sendMail($email, $c['subject'], mailText($c, $link), $from, $owner, mailHtml($c, $link, $lang, $siteUrl, $L['fallback'], $L['footer']));
respond($ok, $ok ? $PATHS[$lang]['thanks'] : $PATHS[$lang]['home'], $wantsJson, $ok ? 'confirm-sent' : 'mail');
