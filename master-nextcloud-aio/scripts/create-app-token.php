#!/usr/bin/env php
<?php
// Print a permanent app password for uid admin (Deck import).
require '/var/www/html/lib/base.php';

$uid = $argv[1] ?? 'admin';
$name = $argv[2] ?? 'deck-import';
$server = \OC::$server;
$user = $server->getUserManager()->get($uid);
if ($user === null) {
    fwrite(STDERR, "no user $uid\n");
    exit(1);
}
$random = $server->get(\OCP\Security\ISecureRandom::class);
$token = $random->generate(
    72,
    \OCP\Security\ISecureRandom::CHAR_UPPER
    . \OCP\Security\ISecureRandom::CHAR_LOWER
    . \OCP\Security\ISecureRandom::CHAR_DIGITS
);
$provider = $server->get(\OC\Authentication\Token\IProvider::class);
$provider->generateToken(
    $token,
    $user->getUID(),
    $user->getUID(),
    null,
    $name,
    \OC\Authentication\Token\IToken::PERMANENT_TOKEN,
    \OC\Authentication\Token\IToken::DO_NOT_REMEMBER
);
echo $token, "\n";
