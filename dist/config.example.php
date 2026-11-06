<?php
/**
 * Kopiraj v config.php (config.php je v .htaccess zaščiten pred branjem prek spleta) in vpiši prave vrednosti.
 */
return [
    // kam prispejo sporočila s kontaktnega obrazca
    'contact_to'   => 'katja@beezee.si',
    // pošiljatelj (naj bo naslov na domeni beezee.si, da pošta ne pristane v spamu)
    'contact_from' => 'noreply@beezee.si',

    // Panj (samostojno): mapa s seznamom članov (clani.csv) – privzeto ena raven NAD spletno mapo
    // 'panj_dir' => '/home/beezeesi/beezee-panj',
    // javni naslov strani (za potrditveno povezavo); privzeto se vzame iz HTTP_HOST
    // 'site_url' => 'https://beezee.si',

    // neobvezno: MailerLite namesto samostojnega Panja (če sta oba vpisana, se uporablja MailerLite)
    'mailerlite_key'   => '',
    'mailerlite_group' => '',
];
