# Telemonitoramento CEUB 🩺

Sistema de telemonitoramento para acompanhamento remoto de sinais vitais, desenvolvido para o CEUB (Centro Universitário de Brasília).

## 📁 Estrutura do Projeto

```
telemonitoramento-web/
├── telemonitoramento/          # Código-fonte principal
│   ├── __init__.py
│   ├── app.py                  # Aplicação principal Streamlit
│   ├── database.py             # Configurações de banco de dados
│   └── utils.py                # Funções utilitárias
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   ├── test_app.py             # Testes da aplicação
│   └── teste_email.py          # Testes de envio de e-mail
├── scripts/                    # Scripts utilitários e manutenção
│   ├── __init__.py
│   ├── checar_db.py            # Verificação de integridade do banco
│   └── setup_database.py       # Configuração inicial do banco
├── docs/                       # Documentação
├── PHP TCC/                    # Código PHP (projeto separado)
├── main.py                     # Ponto de entrada principal
├── requirements.txt            # Dependências Python
├── env.example                 # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- PostgreSQL
- Conta Gmail para envio de e-mails

### Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd telemonitoramento-web
```

2. **Crie um ambiente virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
```

Exemplo do arquivo `.env`:
```env
# Configurações do Banco de Dados PostgreSQL
DB_HOST=localhost
DB_NAME=telemonitoramento
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
DB_PORT=5432

# Configurações de E-mail (Gmail)
EMAIL_SENDER=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-de-app-gmail

# Chave de Criptografia (Gere uma nova para produção)
FERNET_KEY=sua-chave-criptografia-aqui
```

5. **Configure o banco de dados:**
```bash
# Execute o script de configuração
python scripts/setup_database.py
```

6. **Execute o aplicativo:**
```bash
# Opção 1: Via main.py
python main.py

# Opção 2: Direto via Streamlit
streamlit run telemonitoramento/app.py
```

## 🧪 Executando Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar teste específico
python -m pytest tests/test_app.py

# Executar com cobertura
python -m pytest tests/ --cov=telemonitoramento
```

## 🔧 Scripts de Manutenção

```bash
# Configurar banco de dados (primeira vez)
python scripts/setup_database.py

# Verificar integridade do banco de dados
python scripts/checar_db.py

# Testar envio de e-mails
python tests/teste_email.py
```

## 📊 Funcionalidades

- **Autenticação segura** com 2FA e recuperação de senha
- **Cadastro de usuários** (Administradores, Profissionais, Pacientes)
- **Registro de sinais vitais** com validação automática
- **Sistema de alertas** configurável
- **Mensagens internas** entre usuários
- **Relatórios e gráficos** interativos
- **Auditoria completa** de ações
- **Criptografia** de dados sensíveis
- **Notificações por e-mail** automáticas

## 🔒 Segurança

- Senhas hasheadas com SHA-256
- Dados médicos criptografados com Fernet
- Autenticação em duas etapas (2FA)
- Auditoria de todas as ações
- Validação de entrada de dados
- Proteção contra SQL Injection

## 🛠️ Tecnologias Utilizadas

- **Frontend:** Streamlit
- **Backend:** Python
- **Banco de Dados:** PostgreSQL
- **Criptografia:** Fernnet (cryptography)
- **E-mail:** SMTP (Gmail)
- **Testes:** pytest
- **Gráficos:** Plotly, Matplotlib

## 📞 Suporte

Para dúvidas ou problemas, entre em contato:
- **E-mail:** suporte@ceub.edu.br
- **Documentação:** Consulte a pasta `docs/`

## 📝 Licença

Este projeto foi desenvolvido para o CEUB. Todos os direitos reservados.

---

**Desenvolvido com ❤️ pelo CEUB**