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

    # Verifica as colunas existentes na tabela
    colunas = [
        linha[1]
        for linha in cursor.execute(
            "PRAGMA table_info(itens_cardapio)"
        ).fetchall()
    ]

    # Adiciona categoria caso ainda não exista
    if 'categoria' not in colunas:
        cursor.execute("""
            ALTER TABLE itens_cardapio
            ADD COLUMN categoria TEXT DEFAULT 'Outros'
        """)

    # Adiciona imagem caso ainda não exista
    if 'imagem' not in colunas:
        cursor.execute("""
            ALTER TABLE itens_cardapio
            ADD COLUMN imagem TEXT
        """)

    # Produtos do novo cardápio
    produtos = [
        ('Cheeseburger Duplo', 'Dois hambúrgueres, cheddar e cebola caramelizada.', 39.90, 'Hambúrgueres', 'https://images.unsplash.com/photo-1553979459-d2229ba7433a?w=700'),
        ('Burger Bacon', 'Hambúrguer artesanal com bacon e barbecue.', 37.90, 'Hambúrgueres', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700'),
        ('Pizza Margherita', 'Molho de tomate, queijo e manjericão.', 42.00, 'Pizzas', 'https://images.unsplash.com/photo-1579751626657-72bc17010498?w=700'),
        ('Pizza Calabresa', 'Calabresa, cebola e queijo.', 46.00, 'Pizzas', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=700'),
        ('Pizza Quatro Queijos', 'Mozzarella, parmesão, provolone e gorgonzola.', 49.90, 'Pizzas', 'https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=700'),
        ('Lasanha à Bolonhesa', 'Massa, molho bolonhesa e queijo gratinado.', 34.90, 'Massas', 'https://images.unsplash.com/photo-1619895092538-128341789043?w=700'),
        ('Fettuccine ao molho branco', 'Massa cremosa com parmesão.', 32.00, 'Massas', 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=700'),
        ('Espaguete à Bolonhesa', 'Espaguete com molho de tomate e carne.', 29.90, 'Massas', 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=700'),
        ('Batata Rústica', 'Batatas temperadas com alecrim e páprica.', 18.00, 'Porções', 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=700'),
        ('Frango Crocante', 'Tiras de frango empanadas.', 27.90, 'Porções', 'https://images.unsplash.com/photo-1562967914-608f82629710?w=700'),
        ('Anéis de Cebola', 'Porção crocante de onion rings.', 21.90, 'Porções', 'https://images.unsplash.com/photo-1639024471283-03518883512d?w=700'),
        ('Brownie com Sorvete', 'Brownie de chocolate com sorvete.', 19.90, 'Sobremesas', 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=700'),
        ('Cheesecake', 'Cheesecake com frutas vermelhas.', 18.90, 'Sobremesas', 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=700'),
        ('Pudim da Casa', 'Pudim tradicional com caramelo.', 12.90, 'Sobremesas', 'https://images.unsplash.com/photo-1551024506-0accd828d307?w=700'),
        ('Suco Natural de Laranja', 'Suco natural feito na hora.', 8.50, 'Bebidas', 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=700'),
        ('Limonada Suíça', 'Limão batido com gelo.', 10.90, 'Bebidas', 'https://images.unsplash.com/photo-1513558161293-cacab7c8e8b8?w=700'),
        ('Refrigerante Lata', 'Refrigerante de 350 ml.', 6.50, 'Bebidas', 'https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=700')
    ]

    for produto in produtos:
        existe = cursor.execute(
            "SELECT id_item FROM itens_cardapio WHERE nome = ?",
            (produto[0],)
        ).fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO itens_cardapio
                (nome, descricao, preco, status_ativo, categoria, imagem)
                VALUES (?, ?, ?, 1, ?, ?)
            """, produto)

    # Atualiza os três produtos que já existiam
    atualizacoes = [
        ('Hambúrguer Artesanal', 'Hambúrgueres',
         'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700'),
        ('Batata Rústica', 'Porções',
         'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=700'),
        ('Suco Natural', 'Bebidas',
         'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=700')
    ]

    for nome, categoria, imagem in atualizacoes:
        cursor.execute("""
            UPDATE itens_cardapio
            SET categoria = ?, imagem = ?
            WHERE nome = ?
        """, (categoria, imagem, nome))

    banco.commit()

    print("Banco atualizado com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro ao atualizar o banco: {e}")

finally:
    banco.close()