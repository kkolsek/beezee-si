<?php
/**
 * beezee.si – prijava v Panj z dvojno potrditvijo.
 *
 * Dva načina (izbere se glede na config.php):
 *  A) samostojno (privzeto, brez zunanje storitve): pošlje potrditveno e-pošto s podpisano povezavo;
 *     po kliku shrani naslov v CSV izven spletne mape in obvesti Katjo.
 *  B) MailerLite: če je v config.php vpisan 'mailerlite_key' + 'mailerlite_group', doda naročnika
 *     s statusom 'unconfirmed' (MailerLite sam pošlje potrditev).
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
    'sl' => ['thanks' => '/hvala/',      'welcome' => '/panj/dobrodosli/',     'home' => '/#panj'],
    'en' => ['thanks' => '/en/thanks/',  'welcome' => '/en/hive/welcome/',     'home' => '/en/#panj'],
    'hr' => ['thanks' => '/hr/hvala/',   'welcome' => '/hr/kosnica/dobrodosli/', 'home' => '/hr/#panj'],
];
$WELCOME = [
    'sl' => ['subj' => 'Dobrodošel/-a v panju 🐝 – tukaj je kontrolni seznam', 'body' => "Živjo!\n\nPrijava je potrjena, dobrodošel/-a v panju.\n\nObljubljeni kontrolni seznam pred prenovo spletne strani (PDF):\n%s\n\nPisala bom samo, ko bom imela kaj sladkega. Odjava kadar koli z odgovorom na to sporočilo.\n\nKatja\nbeezee.si", 'pdf' => '/assets/pdf/beezee-kontrolni-seznam-sl.pdf'],
    'en' => ['subj' => 'Welcome to the hive 🐝 – here is your checklist', 'body' => "Hi!\n\nYour subscription is confirmed, welcome to the hive.\n\nThe promised website redesign checklist (PDF):\n%s\n\nI only write when I have something sweet. Unsubscribe any time by replying to this email.\n\nKatja\nbeezee.si", 'pdf' => '/assets/pdf/beezee-kontrolni-seznam-en.pdf'],
    'hr' => ['subj' => 'Dobrodošao/-la u košnicu 🐝 – evo kontrolnog popisa', 'body' => "Bok!\n\nPrijava je potvrđena, dobrodošao/-la u košnicu.\n\nObećani kontrolni popis prije redizajna web stranice (PDF):\n%s\n\nPišem samo kad imam nešto slatko. Odjava bilo kada odgovorom na ovu poruku.\n\nKatja\nbeezee.si", 'pdf' => '/assets/pdf/beezee-kontrolni-seznam-hr.pdf'],
];
$MAIL = [
    'sl' => ['subj' => 'Potrdi prijavo v panj 🐝', 'body' => "Živjo!\n\nŠe en klik in si v panju. Potrdi prijavo tukaj:\n%s\n\nČe se nisi prijavil/-a, to sporočilo prezri.\n\nKatja\nbeezee.si"],
    'en' => ['subj' => 'Confirm your hive subscription 🐝', 'body' => "Hi!\n\nOne more click and you're in the hive. Confirm here:\n%s\n\nIf you didn't sign up, just ignore this email.\n\nKatja\nbeezee.si"],
    'hr' => ['subj' => 'Potvrdi prijavu u košnicu 🐝', 'body' => "Bok!\n\nJoš jedan klik i u košnici si. Potvrdi prijavu ovdje:\n%s\n\nAko se nisi prijavio/-la, zanemari ovu poruku.\n\nKatja\nbeezee.si"],
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
function sendMail(string $to, string $subject, string $body, string $from, string $replyTo = ''): bool {
    $h = ['From: BEEZEE <' . $from . '>', 'Content-Type: text/plain; charset=UTF-8', 'X-Mailer: beezee.si'];
    if ($replyTo !== '') { $h[] = 'Reply-To: ' . $replyTo; }
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
        sendMail($email, $WELCOME[$lang]['subj'], sprintf($WELCOME[$lang]['body'], $siteUrl . $WELCOME[$lang]['pdf']), $from, $owner);
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
$t = token($email, $lang, secret($dataDir, $config));
$link = $siteUrl . '/panj.php?potrdi=' . rtrim(strtr(base64_encode($email), '+/', '-_'), '=') . '&t=' . $t . '&lang=' . $lang;
$ok = sendMail($email, $MAIL[$lang]['subj'], sprintf($MAIL[$lang]['body'], $link), $from, $owner);
respond($ok, $ok ? $PATHS[$lang]['thanks'] : $PATHS[$lang]['home'], $wantsJson, $ok ? 'confirm-sent' : 'mail');
