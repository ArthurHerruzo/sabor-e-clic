-- Consultas e Relatórios Analíticos - Sabor & Clic
-- Turma 231-DS

-- 1. Listar todos os pedidos com o nome do cliente e o status atual
SELECT p.id_pedido, u.nome AS cliente, p.status_pedido, p.valor_total 
FROM pedidos p
JOIN usuarios u ON p.id_cliente = u.id_usuario;

-- 2. Consultar os itens detalhados de um pedido específico (Ex: Pedido ID 1)
SELECT p.id_pedido, i.nome AS prato, ip.quantidade, i.preco 
FROM itens_pedido ip
JOIN pedidos p ON ip.id_pedido = p.id_pedido
JOIN itens_cardapio i ON ip.id_item = i.id_item
WHERE p.id_pedido = 1;

-- 3. Calcular o faturamento total do sistema (Soma de todos os pedidos)
SELECT SUM(valor_total) AS faturamento_total FROM pedidos;

-- 4. Listar apenas os pratos que estão ativos no cardápio
SELECT id_item, nome, preco FROM itens_cardapio WHERE status_ativo = 1;