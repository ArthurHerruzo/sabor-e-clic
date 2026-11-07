from flask import Blueprint, jsonify, request
from database import get_db

api_bp = Blueprint('api', _name_)

# 1. Rota para listar o cardápio do banco de dados (GET)
@api_bp.route('/cardapio', methods=['GET'])
def listar_cardapio():
    db = get_db()
    cursor = db.execute('SELECT id_item, nome, descricao, preco, status_ativo FROM itens_cardapio WHERE status_ativo = 1')
    itens = cursor.fetchall()
    
    # Transforma os registros do SQLite em uma lista de dicionários para JSON
    lista_pratos = []
    for item in itens:
        lista_pratos.append({
            "id": item["id_item"],
            "nome": item["nome"],
            "descricao": item["descricao"],
            "preco": item["preco"],
            "ativo": bool(item["status_ativo"])
        })
        
    return jsonify(lista_pratos), 200

# 2. Rota para registrar um novo pedido (POST)
@api_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.get_json()
    
    if not dados or 'itens' not in dados:
        return jsonify({"erro": "Lista de itens obrigatória"}), 400
        
    id_cliente = dados.get("id_cliente", 1) # Cliente padrão caso venha anônimo
    valor_total = dados.get("total", 0.0)
    
    db = get_db()
    
    # Insere o pedido na tabela pedidos
    cursor = db.execute(
        'INSERT INTO pedidos (id_cliente, status_pedido, valor_total) VALUES (?, ?, ?)',
        (id_cliente, 'AGUARDANDO', valor_total)
    )
    db.commit()
    
    id_pedido_criado = cursor.lastrowid
    
    # Insere os itens vinculados ao pedido na tabela itens_pedido
    for item in dados['itens']:
        db.execute(
            'INSERT INTO itens_pedido (id_pedido, id_item, quantidade) VALUES (?, ?, ?)',
            (id_pedido_criado, item['id'], item.get('quantidade', 1))
        )
    db.commit()
    
    return jsonify({
        "mensagem": "Pedido criado com sucesso!",
        "id_pedido": id_pedido_criado,
        "status": "AGUARDANDO",
        "total": valor_total
    }), 201

# 3. Rota para listar a fila do KDS / Cozinha (GET)
@api_bp.route('/pedidos/kds', methods=['GET'])
def obter_fila_kds():
    db = get_db()
    cursor = db.execute('SELECT id_pedido, id_cliente, status_pedido, valor_total FROM pedidos')
    pedidos = cursor.fetchall()
    
    lista_pedidos = []
    for p in pedidos:
        lista_pedidos.append({
            "id_pedido": p["id_pedido"],
            "id_cliente": p["id_cliente"],
            "status": p["status_pedido"],
            "total": p["valor_total"]
        })
        
    return jsonify(lista_pedidos), 200