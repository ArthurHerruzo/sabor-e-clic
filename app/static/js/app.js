class SaborClicAPI {

    #baseUrl = '/api';

    async listarCardapio() {

        const resposta = await fetch(`${this.#baseUrl}/cardapio`);

        if (!resposta.ok) {
            throw new Error('Erro ao carregar o cardápio.');
        }

        return resposta.json();
    }


    async criarPedido(dados) {

        const resposta = await fetch(`${this.#baseUrl}/pedidos`, {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)

        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || 'Erro ao realizar pedido.');
        }

        return resultado;
    }

}


class Carrinho {

    #itens = [];


    adicionar(produto) {

        const existente = this.#itens.find(
            item => item.id === produto.id
        );

        if (existente) {

            existente.quantidade++;

        } else {

            this.#itens.push({
                ...produto,
                quantidade: 1
            });

        }

    }


    alterarQuantidade(id, variacao) {

        const item = this.#itens.find(
            produto => produto.id === id
        );

        if (!item) return;

        item.quantidade += variacao;

        if (item.quantidade <= 0) {
            this.remover(id);
        }

    }


    remover(id) {

        this.#itens = this.#itens.filter(
            item => item.id !== id
        );

    }


    limpar() {

        this.#itens = [];

    }


    get itens() {

        return this.#itens.map(item => ({ ...item }));

    }


    get total() {

        return this.#itens.reduce(
            (soma, item) => soma + item.preco * item.quantidade,
            0
        );

    }

}


class SaborClicUI {


    #api = new SaborClicAPI();

    #carrinho = new Carrinho();

    #produtos = [];

    #categoriaAtual = 'Todas';

     #container = null;


    async inicializarCardapio(containerId) {

        this.#container = document.getElementById(containerId);

        try {

            this.#produtos = await this.#api.listarCardapio();

            this.#renderizarProdutos();

            this.#renderizarCarrinho();

        } catch (erro) {

            this.#container.innerHTML = 'Erro ao carregar produtos.';

        }

    }


    filtrarCategoria(categoria) {

        this.#categoriaAtual = categoria;

        this.#renderizarProdutos();

    }


    #renderizarProdutos() {

        const produtos = this.#categoriaAtual === 'Todas'
            ? this.#produtos
            : this.#produtos.filter(
                item => item.categoria === this.#categoriaAtual
            );

        document.getElementById('quantidade-produtos').textContent =
            `${produtos.length} opções`;

        this.#container.innerHTML = '';

        if (produtos.length === 0) {

            this.#container.innerHTML =
                '<p>Nenhum produto encontrado.</p>';

            return;

        }


        produtos.forEach(item => {

            const card = document.createElement('article');

            card.className = 'produto-card';


            const imagem = document.createElement('img');

            imagem.src = item.imagem || '';

            imagem.alt = item.nome;

            imagem.loading = 'lazy';

           imagem.onerror = () => {

            imagem.src = '';
            imagem.style.display = 'none';

            };


            const conteudo = document.createElement('div');

            conteudo.className = 'produto-conteudo';


            const categoria = document.createElement('span');

            categoria.className = 'tag-categoria';

            categoria.textContent = item.categoria;


            const nome = document.createElement('h3');

            nome.textContent = item.nome;


            const descricao = document.createElement('p');

            descricao.textContent = item.descricao;


            const rodape = document.createElement('div');

            rodape.className = 'produto-rodape';


            const preco = document.createElement('strong');

            preco.textContent = this.#moeda(item.preco);


            const botao = document.createElement('button');

            botao.className = 'btn-adicionar';

            botao.textContent = '+ Adicionar';


            botao.addEventListener('click', () => {

                this.#carrinho.adicionar(item);

                this.#renderizarCarrinho();

            });


            rodape.append(preco, botao);

            conteudo.append(categoria, nome, descricao, rodape);

            card.append(imagem, conteudo);

            this.#container.appendChild(card);

        });

    }


    #moeda(valor) {

        return Number(valor).toLocaleString('pt-BR', {

            style: 'currency',

            currency: 'BRL'

        });

    }


    #renderizarCarrinho() {

        const lista = document.getElementById('lista-carrinho');

        const itens = this.#carrinho.itens;

        lista.innerHTML = '';


        const quantidadeTotal = itens.reduce(
            (soma, item) => soma + item.quantidade,
            0
        );

        document.getElementById('contador-carrinho').textContent =
            quantidadeTotal;


        if (itens.length === 0) {

            lista.innerHTML =
                '<li class="carrinho-vazio">Seu carrinho está vazio.</li>';

        }


        itens.forEach(item => {

            const li = document.createElement('li');

            li.className = 'item-carrinho';


            const info = document.createElement('div');

            info.className = 'item-carrinho-info';


            const nome = document.createElement('strong');

            nome.textContent = item.nome;


            const preco = document.createElement('span');

            preco.textContent = this.#moeda(
                item.preco * item.quantidade
            );


            info.append(nome, preco);


            const controles = document.createElement('div');

            controles.className = 'controles-qtd';


            const menos = document.createElement('button');

            menos.textContent = '−';

            menos.onclick = () => {

                this.#carrinho.alterarQuantidade(item.id, -1);

                this.#renderizarCarrinho();

            };


            const quantidade = document.createElement('span');

            quantidade.textContent = item.quantidade;


            const mais = document.createElement('button');

            mais.textContent = '+';

            mais.onclick = () => {

                this.#carrinho.alterarQuantidade(item.id, 1);

                this.#renderizarCarrinho();

            };


            const remover = document.createElement('button');

            remover.textContent = 'Remover';

            remover.className = 'remover-item';

            remover.onclick = () => {

                this.#carrinho.remover(item.id);

                this.#renderizarCarrinho();

            };


            controles.append(menos, quantidade, mais, remover);

            li.append(info, controles);

            lista.appendChild(li);

        });


        const total = this.#moeda(this.#carrinho.total);

        document.getElementById('subtotal-carrinho').textContent = total;

        document.getElementById('total-carrinho').textContent = total;


        document.getElementById('btn-finalizar').disabled =
            itens.length === 0;

    }


    async finalizarPedido() {

        const itens = this.#carrinho.itens;

        if (itens.length === 0) return;


        const botao = document.getElementById('btn-finalizar');

        botao.disabled = true;

        botao.textContent = 'Enviando...';


        try {

            const resposta = await this.#api.criarPedido({

                itens: itens.map(item => ({

                    id: item.id,

                    quantidade: item.quantidade

                }))

            });


            alert(
                `Pedido #${resposta.id_pedido} realizado com sucesso!\n` +
                `Total: ${this.#moeda(resposta.total)}`
            );


            this.#carrinho.limpar();

            this.#renderizarCarrinho();


        } catch (erro) {

            alert(erro.message);

        } finally {

            botao.textContent = 'Finalizar pedido';

            botao.disabled = this.#carrinho.itens.length === 0;

        }

    }

}


const appUI = new SaborClicUI();