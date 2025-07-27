<?php
$host = 'localhost';
$port = '5432';
$dbname = 'nome_do_banco';
$user = 'usuario';
$password = 'senha';

try {
    $pdo = new PDO("pgsql:host=$host;port=$port;dbname=$dbname", $user, $password, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
} catch (PDOException $e) {
    die("Erro na conexão: " . $e->getMessage());
}
?> 