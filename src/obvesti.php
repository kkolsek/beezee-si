<?php
/**
 * beezee.si – »Obvesti me« za nove vtičnike (npr. GLS).
 * Shrani e-naslov v CSV izven spletne mape (beezee-panj/obvesti-<vticnik>.csv) in obvesti Katjo.
 * Ni novic: naslov se uporabi samo za eno obvestilo ob izidu.
 * Z JS vrne JSON, brez JS preusmeri nazaj na stran (?obvesti=ok|napaka#gls).
 */
declare(strict_types=1);
header('X-Content-Type-Options: nosniff');

$config  = file_exists(__DIR__ . '/config.php') ? require __DIR__ . '/config.php' : [];
$owner   = $config['contact_to']   ?? 'katja@beezee.si';
$from    = $config['contact_from'] ?? 'noreply@beezee.si';
$dataDir = $config['panj_dir'] ?? dirname(__DIR__) . '/beezee-panj';

$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && str_contains($_SERVER['HTTP_ACCEPT'], 'application/json');
$plugins = ['gls' => 'GLS'];
$plugin  = (string)($_POST['vticnik'] ?? 'gls');
if (!isset($plugins[$plugin])) { $plugin = 'gls'; }
$lang = (string)($_POST['lang'] ?? 'sl');
if (!in_array($lang, ['sl', 'hr', 'en'], true)) { $lang = 'sl'; }
$back = ['sl' => '/posiljke/gls/', 'hr' => '/hr/posiljke/gls/', 'en' => '/posiljke/gls/'][$lang];

function done(bool $ok, string $back, bool $json, string $msg = ''): never {
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'msg' => $msg], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: ' . $back . '?obvesti=' . ($ok ? 'ok' : 'napaka') . '#obvesti', true, 303);
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { done(false, $back, $wantsJson, 'method'); }
if (!empty($_POST['website'])) { done(true, $back, $wantsJson); }   // honeypot

$email = mb_substr(trim(str_replace(["\r", "\n"], '', (string)($_POST['email'] ?? ''))), 0, 200);
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) { done(false, $back, $wantsJson, 'validation'); }

$ip   = $_SERVER['REMOTE_ADDR'] ?? '0';
$lock = sys_get_temp_dir() . '/beezee-obvesti-' . md5($ip);
if (file_exists($lock) && time() - filemtime($lock) < 30) { done(false, $back, $wantsJson, 'rate'); }
touch($lock);

if (!is_dir($dataDir)) { @mkdir($dataDir, 0750, true); }
$file = $dataDir . '/obvesti-' . $plugin . '.csv';
$new  = !file_exists($file);
$fh   = @fopen($file, 'ab');
if (!$fh) { done(false, $back, $wantsJson, 'storage'); }
flock($fh, LOCK_EX);
if ($new) { fputcsv($fh, ['cas', 'email', 'jezik', 'vticnik']); }
fputcsv($fh, [date('Y-m-d H:i:s'), $email, $lang, $plugin]);
flock($fh, LOCK_UN);
fclose($fh);

$subject = '=?UTF-8?B?' . base64_encode('[beezee.si] Obvesti me: ' . $plugins[$plugin] . ' – ' . $email) . '?=';
$headers = ['From: BEEZEE.SI <' . $from . '>', 'Reply-To: ' . $email, 'Content-Type: text/plain; charset=UTF-8', 'X-Mailer: beezee.si'];
@mail($owner, $subject, "Nova prijava na obvestilo ob izidu vtičnika {$plugins[$plugin]}.\n\nE-pošta: $email\nJezik: $lang\nČas: " . date('Y-m-d H:i:s') . "\nSeznam: $file\n", implode("\r\n", $headers));

done(true, $back, $wantsJson, 'ok');
