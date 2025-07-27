#!/usr/bin/env python3
"""
Script para configuração inicial do banco de dados do sistema de telemonitoramento CEUB.
Cria todas as tabelas necessárias e insere dados iniciais.
"""

import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
import hashlib

# Carregar variáveis de ambiente
dotenv_path = find_dotenv()
load_dotenv(dotenv_path, override=True)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def hash_senha(senha):
    """Gera hash SHA-256 da senha."""
    return hashlib.sha256(senha.encode()).hexdigest()

def conectar_db():
    """Estabelece conexão com o banco de dados."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )

def criar_tabelas():
    """Cria todas as tabelas necessárias para o sistema."""
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("🔧 Criando tabelas do sistema...")
    
    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            senha VARCHAR(256) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            status BOOLEAN DEFAULT TRUE,
            primeiro_acesso BOOLEAN DEFAULT TRUE,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'usuarios' criada/verificada")
    
    # Tabela de profissionais
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
            especialidade VARCHAR(100),
            registro_profissional VARCHAR(50),
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'profissionais' criada/verificada")
    
    # Tabela de pacientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id SERIAL PRIMARY KEY,
            id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
            id_profissional_responsavel INTEGER NOT NULL REFERENCES usuarios(id),
            dados_medicos TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'pacientes' criada/verificada")
    
    # Tabela de sinais vitais
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sinais_vitais (
            id SERIAL PRIMARY KEY,
            paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
            temperatura FLOAT NOT NULL,
            pressao VARCHAR(10) NOT NULL,
            frequencia_cardiaca INTEGER NOT NULL,
            saturacao INTEGER NOT NULL,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'sinais_vitais' criada/verificada")
    
    # Tabela de alertas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id SERIAL PRIMARY KEY,
            paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
            tipo_alerta VARCHAR(50) NOT NULL,
            descricao TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'pendente',
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'alertas' criada/verificada")
    
    # Tabela de mensagens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id SERIAL PRIMARY KEY,
            id_remetente INTEGER NOT NULL REFERENCES usuarios(id),
            id_destinatario INTEGER NOT NULL REFERENCES usuarios(id),
            texto TEXT NOT NULL,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'mensagens' criada/verificada")
    
    # Tabela de auditoria
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
            acao VARCHAR(100) NOT NULL,
            detalhes TEXT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'auditoria' criada/verificada")
    
    # Tabela de parâmetros de alerta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parametros_alerta (
            id SERIAL PRIMARY KEY,
            temp_min FLOAT DEFAULT 35.0,
            temp_max FLOAT DEFAULT 38.0,
            freq_min INTEGER DEFAULT 50,
            freq_max INTEGER DEFAULT 120,
            sat_min INTEGER DEFAULT 90,
            pressao_min VARCHAR(10) DEFAULT '90/60',
            pressao_max VARCHAR(10) DEFAULT '140/90',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Tabela 'parametros_alerta' criada/verificada")
    
    conn.commit()
    conn.close()
    print("🎉 Todas as tabelas foram criadas com sucesso!")

def inserir_dados_iniciais():
    """Insere dados iniciais necessários para o sistema."""
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("📝 Inserindo dados iniciais...")
    
    # Verificar se já existe um administrador
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'Administrador'")
    admin_count = cursor.fetchone()[0]
    
    if admin_count == 0:
        # Criar administrador padrão
        admin_senha = hash_senha("Admin@123")
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo, status, primeiro_acesso)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("Administrador", "admin@ceub.edu.br", admin_senha, "Administrador", True, False))
        print("✅ Administrador padrão criado (admin@ceub.edu.br / Admin@123)")
    
    # Verificar se já existem parâmetros de alerta
    cursor.execute("SELECT COUNT(*) FROM parametros_alerta")
    param_count = cursor.fetchone()[0]
    
    if param_count == 0:
        # Inserir parâmetros padrão
        cursor.execute("""
            INSERT INTO parametros_alerta (temp_min, temp_max, freq_min, freq_max, sat_min, pressao_min, pressao_max)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (35.0, 38.0, 50, 120, 90, "90/60", "140/90"))
        print("✅ Parâmetros de alerta padrão inseridos")
    
    conn.commit()
    conn.close()
    print("🎉 Dados iniciais inseridos com sucesso!")

def verificar_conexao():
    """Verifica se a conexão com o banco está funcionando."""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        conn.close()
        print(f"✅ Conexão com banco estabelecida. PostgreSQL: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def main():
    """Função principal do script."""
    print("🚀 Configuração do banco de dados - Telemonitoramento CEUB")
    print("=" * 60)
    
    # Verificar conexão
    if not verificar_conexao():
        print("❌ Não foi possível conectar ao banco. Verifique as configurações no .env")
        return
    
    # Criar tabelas
    try:
        criar_tabelas()
        inserir_dados_iniciais()
        print("\n🎉 Configuração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Execute: python main.py")
        print("2. Acesse: http://localhost:8501")
        print("3. Login: admin@ceub.edu.br / Admin@123")
        
    except Exception as e:
        print(f"❌ Erro durante a configuração: {e}")

if __name__ == "__main__":
    main() 