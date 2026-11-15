-- Triggers e Automações de Regras de Negócio - Sabor & Clic
-- Turma 231-DS

-- Trigger simples para garantir que o status do pedido inicie como 'AGUARDANDO' 
-- caso venha vazio na inserção (Exemplo acadêmico prático)
CREATE TRIGGER IF NOT EXISTS trg_padronizar_status_pedido
AFTER INSERT ON pedidos
WHEN NEW.status_pedido IS NULL
BEGIN
    UPDATE pedidos 
    SET status_pedido = 'AGUARDANDO' 
    WHERE id_pedido = NEW.id_pedido;
END;