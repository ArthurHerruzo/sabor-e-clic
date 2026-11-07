-- Inserções Básicas para Inicialização do Sistema

-- Inserção de Usuários Padrão (Senhas em hash simuladas / bcrypt)
INSERT INTO usuarios (nome, email, senha_hash, nivel_acesso) VALUES 
('Administrador Geral', 'admin@saborclic.com', 'sc_hash_admin_123', 'ADMIN'),
('Cliente Teste', 'cliente@saborclic.com', 'sc_hash_cliente_123', 'CLIENTE'),
('Cozinheiro Chefe', 'cozinha@saborclic.com', 'sc_hash_cozinha_123', 'COZINHEIRO');

-- Inserção dos Itens do Cardápio (Catálogo inicial)
INSERT INTO itens_cardapio (nome, descricao, preco, status_ativo) VALUES 
('Hambúrguer Artesanal', 'Pão brioche, blend bovino 160g e queijo cheddar', 32.50, 1),
('Batata Rústica', 'Batatas rústicas temperadas com alecrim e páprica', 18.00, 1),
('Suco Natural', 'Suco natural de laranja fresco 400ml', 8.50, 1);