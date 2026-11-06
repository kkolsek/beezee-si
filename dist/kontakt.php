<?php
/**
 * beezee.si – kontaktni obrazec
 * Pošlje sporočilo na $to. Z JS vrne JSON, brez JS preusmeri na stran »hvala«.
 */
declare(strict_types=1);
header('X-Content-Type-Options: nosniff');

$config = file_exists(__DIR__ . '/config.php') ? require __DIR__ . '/config.php' : [];
$to     = $config['contact_to']   ?? 'katja@beezee.si';
$from   = $config['contact_from'] ?? 'noreply@beezee.si';

$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && str_contains($_SERVER['HTTP_ACCEPT'], 'application/json');
$langs  = ['sl' => '/hvala/', 'en' => '/en/thanks/', 'hr' => '/hr/hvala/'];
$lang   = $_POST['lang'] ?? 'sl';
if (!isset($langs[$lang])) { $lang = 'sl'; }
$homeAnchor = ['sl' => '/#kontakt', 'en' => '/en/#kontakt', 'hr' => '/hr/#kontakt'][$lang];

function respond(bool $ok, string $redirect, bool $json, string $msg = ''): never {
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'msg' => $msg], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: ' . $redirect . ($ok ? '' : '?napaka=1'), true, 303);
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { respond(false, $homeAnchor, $wantsJson, 'method'); }

// honeypot – pravi obiskovalci polja ne vidijo
if (!empty($_POST['website'])) { respond(true, $langs[$lang], $wantsJson); }

$clean = static fn(string $k, int $max): string => mb_substr(trim(str_replace(["\r", "\n"], ' ', (string)($_POST[$k] ?? ''))), 0, $max);
$ime   = $clean('ime', 120);
$email = $clean('email', 200);
$msg   = mb_substr(trim((string)($_POST['sporocilo'] ?? '')), 0, 5000);
$needs = array_filter(array_map(static fn($v) => mb_substr(trim((string)$v), 0, 60), (array)($_POST['potrebujem'] ?? [])));
$consent = !empty($_POST['soglasje']);

if ($ime === '' || $msg === '' || !$consent || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, $homeAnchor, $wantsJson, 'validation');
}

// enostavna zaščita pred poplavo: največ 1 sporočilo na 30 s z istega IP (datoteka v tmp)
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$lock = sys_get_temp_dir() . '/beezee-contact-' . md5($ip);
if (file_exists($lock) && time() - filemtime($lock) < 30) { respond(false, $homeAnchor, $wantsJson, 'rate'); }
touch($lock);

$subject = '[beezee.si] ' . ($lang === 'sl' ? 'Novo sporočilo od ' : ($lang === 'hr' ? 'Nova poruka od ' : 'New message from ')) . $ime;
$body = "Ime: $ime\nE-pošta: $email\nJezik: $lang\n"
      . ($needs ? "Potrebuje: " . implode(', ', $needs) . "\n" : '')
      . "IP: $ip\nČas: " . date('Y-m-d H:i:s') . "\n\n" . $msg . "\n";

$headers = [
    'From: BEEZEE.SI <' . $from . '>',
    'Reply-To: ' . $ime . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: beezee.si',
];
$encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$ok = @mail($to, $encSubject, $body, implode("\r\n", $headers));

respond((bool)$ok, $ok ? $langs[$lang] : $homeAnchor, $wantsJson, $ok ? 'sent' : 'mail');
