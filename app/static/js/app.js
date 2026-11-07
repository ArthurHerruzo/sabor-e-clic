/**
 * Gerenciador da API do Sabor & Clic
 * Atende aos requisitos de POO (ES6+), encasulamento (#) e Fetch API.
 */
class SaborClicAPI {
    // Campo privado para encapsulamento real (#)
    #baseUrl;

    constructor(baseUrl = '/api') {
        this.#baseUrl = baseUrl;
    }

    async listarCardapio() {
        try {
            const response = await fetch(`${this.#baseUrl}/cardapio`);
            if (!response.ok) throw new Error('Erro ao carregar o cardápio.');
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição (listarCardapio):', error);
            return [];
        }
    }

    async criarPedido(dadosPedido) {
        try {
            const response = await fetch(`${this.#baseUrl}/pedidos`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dadosPedido)
            });

            if (!response.ok) throw new Error('Erro ao registrar o pedido.');
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição (criarPedido):', error);
            return { erro: true, mensagem: error.message };
        }
    }
}

/**
 * Entidade Carrinho com estado encapsulado (#)
 */
class Carrinho {
    #itens;

    constructor() {
        this.#itens = [];
    }

    adicionarItem(item) {
        this.#itens.push(item);
    }

    limpar() {
        this.#itens = [];
    }

    get itens() {
        return [...this.#itens];
    }

    get total() {
        return this.#itens.reduce((sum, item) => sum + (item.preco * item.quantidade), 0);
    }
}

/**
 * Gerenciador de Interface de Usuário (DOM)
 */
class SaborClicUI {
    #api;
    #carrinho;

    constructor() {
        this.#api = new SaborClicAPI();
        this.#carrinho = new Carrinho();
    }

    async inicializarCardapio(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '<p>Carregando cardápio...</p>';
        const itens = await this.#api.listarCardapio();

        if (itens.length === 0) {
            container.innerHTML = '<p>Nenhum item disponível.</p>';
            return;
        }

        container.innerHTML = '';
        itens.forEach(item => {
            const card = document.createElement('div');
            card.className = 'item-cardapio';
            card.innerHTML = `
                <h3>${item.nome}</h3>
                <p>${item.descricao}</p>
                <span>R$ ${Number(item.preco).toFixed(2)}</span>
                <button onclick="appUI.adicionarItem(${item.id}, '${item.nome}', ${item.preco})">Adicionar</button>
            `;
            container.appendChild(card);
        });
    }

    adicionarItem(id, nome, preco) {
        this.#carrinho.adicionarItem({ id, nome, preco, quantidade: 1 });
        alert(`${nome} adicionado ao carrinho!`);
    }

    async finalizarPedido() {
        if (this.#carrinho.itens.length === 0) {
            alert('Seu carrinho está vazio!');
            return;
        }

        const payload = {
            id_cliente: 1,
            total: this.#carrinho.total,
            itens: this.#carrinho.itens.map(i => ({ id: i.id, quantidade: i.quantidade }))
        };

        const resposta = await this.#api.criarPedido(payload);

        if (!resposta.erro) {
            alert(`Pedido #${resposta.id_pedido} realizado com sucesso!`);
            this.#carrinho.limpar();
        } else {
            alert('Falha ao registrar pedido.');
        }
    }
}

const appUI = new SaborClicUI();