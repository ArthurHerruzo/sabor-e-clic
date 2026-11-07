/**
 * Classe responsável por centralizar todas as requisições HTTP (API Client)
 * Utiliza o padrão OOP e Fetch API para comunicar com o Backend Flask.
 */
class SaborClicAPI {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }

    // 1. Buscar o cardápio ativo do banco de dados (GET)
    async listarCardapio() {
        try {
            const response = await fetch(`${this.baseUrl}/cardapio`);
            if (!response.ok) {
                throw new Error('Erro ao carregar o cardápio do servidor.');
            }
            const itens = await response.json();
            return itens;
        } catch (error) {
            console.error('Erro na API (listarCardapio):', error);
            return [];
        }
    }

    // 2. Enviar um novo pedido para o backend salvar no SQLite (POST)
    async criarPedido(dadosPedido) {
        try {
            const response = await fetch(`${this.baseUrl}/pedidos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dadosPedido)
            });

            if (!response.ok) {
                throw new Error('Erro ao registrar o pedido.');
            }

            const resultado = await response.json();
            return resultado;
        } catch (error) {
            console.error('Erro na API (criarPedido):', error);
            return { erro: true, mensagem: error.message };
        }
    }

    // 3. Buscar a fila de pedidos para a Cozinha / KDS (GET)
    async obterFilaKDS() {
        try {
            const response = await fetch(`${this.baseUrl}/pedidos/kds`);
            if (!response.ok) {
                throw new Error('Erro ao carregar a fila da cozinha.');
            }
            return await response.json();
        } catch (error) {
            console.error('Erro na API (obterFilaKDS):', error);
            return [];
        }
    }
}


/**
 * Classe responsável por gerenciar a interface do usuário (UI) e renderizar os dados na tela.
 */
class SaborClicUI {
    constructor() {
        this.api = new SaborClicAPI();
        this.carrinho = []; // Armazena os itens selecionados pelo cliente
    }

    // Inicializa a aplicação na página principal
    async inicializarCardapio(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '<p>Carregando cardápio fresquinho...</p>';

        const itensCardapio = await this.api.listarCardapio();

        if (itensCardapio.length === 0) {
            container.innerHTML = '<p>Nenhum item disponível no momento.</p>';
            return;
        }

        container.innerHTML = '';
        itensCardapio.forEach(item => {
            const card = document.createElement('div');
            card.classList.add('item-cardapio');
            card.innerHTML = `
                <h3>${item.nome}</h3>
                <p>${item.descricao}</p>
                <span>R$ ${Number(item.preco).toFixed(2)}</span>
                <button onclick="appUI.adicionarAoCarrinho(${item.id}, '${item.nome}', ${item.preco})">Adicionar</button>
            `;
            container.appendChild(card);
        });
    }

    adicionarAoCarrinho(id, nome, preco) {
        this.carrinho.push({ id, nome, preco, quantidade: 1 });
        alert(`${nome} adicionado ao pedido!`);
        console.log('Carrinho atual:', this.carrinho);
    }

    // Finalizar o pedido atual enviando para a API
    async finalizarPedido() {
        if (this.carrinho.length === 0) {
            alert('Seu carrinho está vazio!');
            return;
        }

        const totalGeral = this.carrinho.reduce((total, item) => total + (item.preco * item.quantidade), 0);

        const payload = {
            id_cliente: 1, // Exemplo de ID de cliente logado
            total: totalGeral,
            itens: this.carrinho.map(i => ({ id: i.id, quantidade: i.quantidade }))
        };

        const resposta = await this.api.criarPedido(payload);

        if (!resposta.erro) {
            alert(`Pedido #${resposta.id_pedido} realizado com sucesso! Status: ${resposta.status}`);
            this.carrinho = []; // Limpa o carrinho
        } else {
            alert('Não foi possível concluir o pedido. Tente novamente.');
        }
    }
}

// Instância global para ser chamada nos elementos HTML
const appUI = new SaborClicUI();