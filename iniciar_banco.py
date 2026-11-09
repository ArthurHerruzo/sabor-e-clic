import sqlite3
import os

# Garante que a pasta 'database' exista no projeto
os.makedirs('database', exist_ok=True)

# Conecta ao banco de dados (se não existir, ele será criado)
banco = sqlite3.connect('database/sabor_clic.db')
cursor = banco.cursor()

# Executa o seu script SQL completo
script_sql = """
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    nivel_acesso TEXT NOT NULL CHECK(nivel_acesso IN ('ADMIN', 'CLIENTE', 'COZINHEIRO'))
);

CREATE TABLE IF NOT EXISTS itens_cardapio (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    status_ativo BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    status_pedido TEXT NOT NULL DEFAULT 'AGUARDANDO' CHECK(status_pedido IN ('AGUARDANDO', 'PREPARO', 'PRONTO', 'FINALIZADO')),
    valor_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_item) REFERENCES itens_cardapio(id_item)
);

-- Usa INSERT OR IGNORE para não duplicar os dados se você rodar o script mais de uma vez
INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, nivel_acesso) VALUES 
('Administrador Geral', 'admin@saborclic.com', 'sc_hash_admin_123', 'ADMIN'),
('Cliente Teste', 'cliente@saborclic.com', 'sc_hash_cliente_123', 'CLIENTE'),
('Cozinheiro Chefe', 'cozinha@saborclic.com', 'sc_hash_cozinha_123', 'COZINHEIRO');

INSERT OR IGNORE INTO itens_cardapio (nome, descricao, preco, status_ativo) VALUES 
('Hambúrguer Artesanal', 'Pão brioche, blend bovino 160g e queijo cheddar', 32.50, 1),
('Batata Rústica', 'Batatas rústicas temperadas com alecrim e páprica', 18.00, 1),
('Suco Natural', 'Suco natural de laranja fresco 400ml', 8.50, 1);

CREATE TRIGGER IF NOT EXISTS trg_padronizar_status_pedido
AFTER INSERT ON pedidos
WHEN NEW.status_pedido IS NULL
BEGIN
    UPDATE pedidos 
    SET status_pedido = 'AGUARDANDO' 
    WHERE id_pedido = NEW.id_pedido;
END;
"""

try:
    cursor.executescript(script_sql)
    banco.commit()
    print("Banco de dados, tabelas e dados iniciais criados com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro ao criar o banco: {e}")
finally:
    banco.close()