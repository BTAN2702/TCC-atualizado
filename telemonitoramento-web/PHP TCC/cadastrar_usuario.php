<?php
require 'conexao.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome = $_POST['nome'] ?? '';
    $email = $_POST['email'] ?? '';
    $senha = $_POST['senha'] ?? '';
    $tipo = $_POST['tipo'] ?? 'Paciente';

    if (!$nome || !$email || !$senha) {
        echo "Preencha todos os campos!";
        exit;
    }

    // Hash seguro da senha
    $senhaHash = password_hash($senha, PASSWORD_DEFAULT);

    // Verifica se o e-mail já existe
    $stmt = $pdo->prepare("SELECT id FROM usuarios WHERE email = ?");
    $stmt->execute([$email]);
    if ($stmt->fetch()) {
        echo "E-mail já cadastrado!";
        exit;
    }

    // Insere o usuário
    $stmt = $pdo->prepare("INSERT INTO usuarios (nome, email, senha, tipo, status, primeiro_acesso) VALUES (?, ?, ?, ?, true, true)");
    if ($stmt->execute([$nome, $email, $senhaHash, $tipo])) {
        echo "Usuário cadastrado com sucesso!";
    } else {
        echo "Erro ao cadastrar usuário!";
    }
}
?>

<!-- Formulário HTML simples -->
<form method="post">
    Nome: <input type="text" name="nome"><br>
    E-mail: <input type="email" name="email"><br>
    Senha: <input type="password" name="senha"><br>
    Tipo: 
    <select name="tipo">
        <option value="Administrador">Administrador</option>
        <option value="Profissional">Profissional</option>
        <option value="Paciente" selected>Paciente</option>
    </select><br>
    <button type="submit">Cadastrar</button>
</form> 