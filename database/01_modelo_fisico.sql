-- Criação do Modelo Físico - Sabor & Clic

-- Tabela de Usuários (Gerencia RBAC: Administrador, Cliente, Cozinheiro)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    nivel_acesso TEXT NOT NULL CHECK(nivel_acesso IN ('ADMIN', 'CLIENTE', 'COZINHEIRO'))
);

-- Tabela de Itens do Cardápio
CREATE TABLE IF NOT EXISTS itens_cardapio (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    status_ativo BOOLEAN DEFAULT 1
);

-- Tabela de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    status_pedido TEXT NOT NULL DEFAULT 'AGUARDANDO' CHECK(status_pedido IN ('AGUARDANDO', 'PREPARO', 'PRONTO', 'FINALIZADO')),
    valor_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id_usuario)
);

-- Tabela Relacional de Itens do Pedido (N para N entre Pedido e Cardápio)
CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    id_item INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_item) REFERENCES itens_cardapio(id_item)
