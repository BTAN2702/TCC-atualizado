<?php
require 'conexao.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $senha = $_POST['senha'] ?? '';

    $stmt = $pdo->prepare("SELECT * FROM usuarios WHERE email = ?");
    $stmt->execute([$email]);
    $usuario = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($usuario && password_verify($senha, $usuario['senha'])) {
        if (!$usuario['status']) {
            echo "Usuário inativo.";
        } else {
            echo "Login realizado com sucesso! Bem-vindo, " . htmlspecialchars($usuario['nome']);
            // Aqui você pode iniciar uma sessão, redirecionar, etc.
        }
    } else {
        echo "E-mail ou senha inválidos!";
    }
}
?>

<!-- Formulário HTML simples -->
<form method="post">
    E-mail: <input type="email" name="email"><br>
    Senha: <input type="password" name="senha"><br>
    <button type="submit">Entrar</button>
</form> 