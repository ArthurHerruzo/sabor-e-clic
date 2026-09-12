
let itensCarrinho = [];
let valorTotal = 0;
let mesaSelecionada = null;

document.addEventListener("DOMContentLoaded", function() {
    let btnFinalizar = document.getElementById("btn-finalizar");
    let btnLimpar = document.getElementById("btn-limpar");
    let inputCupom = document.getElementById("cupom-desconto");

    if (btnFinalizar) {
        btnFinalizar.addEventListener("click", function() {
            finalizarPedido();
        });
    }

    if (btnLimpar) {
        btnLimpar.addEventListener("click", function() {
            limparCarrinho();
        });
    }

    if (inputCupom) {
        inputCupom.addEventListener("change", function() {
            aplicarCupom(inputCupom.value);
        });
    }

    carregarCarrinhoSalvo();
});

function adicionarItem(idProduto, nomeProduto, precoProduto) {
    if (!idProduto || !nomeProduto || precoProduto <= 0) {
        return;
    }

    let itemEncontrado = false;

    for (let i = 0; i < itensCarrinho.length; i++) {
        if (itensCarrinho[i].id === idProduto) {
            itensCarrinho[i].qtd += 1;
            itemEncontrado = true;
            break;
        }
    }

    if (!itemEncontrado) {
        let produto = {
            id: idProduto,
            nome: nomeProduto,
            preco: parseFloat(precoProduto),
            qtd: 1
        };
        itensCarrinho.push(produto);
    }

    salvarCarrinhoLocal();
    atualizarInterface();
}

function removerItem(idProduto) {
    for (let i = 0; i < itensCarrinho.length; i++) {
        if (itensCarrinho[i].id === idProduto) {
            if (itensCarrinho[i].qtd > 1) {
                itensCarrinho[i].qtd -= 1;
            } else {
                itensCarrinho.splice(i, 1);
            }
            break;
        }
    }

    salvarCarrinhoLocal();
    atualizarInterface();
}

function calcularTotal() {
    let soma = 0;
    for (let i = 0; i < itensCarrinho.length; i++) {
        soma += itensCarrinho[i].preco * itensCarrinho[i].qtd;
    }
    valorTotal = soma;
    return valorTotal;
}

function atualizarInterface() {
    let total = calcularTotal();
    let spanTotal = document.getElementById("valor-total");
    let contadorItens = document.getElementById("qtd-itens");

    if (spanTotal) {
        spanTotal.innerText = formatarPreco(total);
    }

    if (contadorItens) {
        contadorItens.innerText = obterTotalItens();
    }
}

function obterTotalItens() {
    let totalItens = 0;
    for (let i = 0; i < itensCarrinho.length; i++) {
        totalItens += itensCarrinho[i].qtd;
    }
    return totalItens;
}

function limparCarrinho() {
    itensCarrinho = [];
    valorTotal = 0;
    localStorage.removeItem("carrinho_sabor_clic");
    atualizarInterface();
}

function aplicarCupom(codigo) {
    let cupomFormatado = codigo.trim().toUpperCase();
    
    if (cupomFormatado === "SABOR10") {
        valorTotal = valorTotal * 0.9;
        atualizarInterfaceComDesconto(10);
    } else if (cupomFormatado === "IFSP20") {
        valorTotal = valorTotal * 0.8;
        atualizarInterfaceComDesconto(20);
    }
}

function atualizarInterfaceComDesconto(porcentagem) {
    let spanTotal = document.getElementById("valor-total");
    if (spanTotal) {
        spanTotal.innerText = formatarPreco(valorTotal) + " (" + porcentagem + "% off)";
    }
}

function finalizarPedido() {
    if (itensCarrinho.length === 0) {
        alert("Adicione pelo menos um item ao carrinho antes de enviar.");
        return;
    }

    let nomeCliente = document.getElementById("nome-cliente");
    let observacao = document.getElementById("obs-pedido");

    let resumoPedido = {
        cliente: nomeCliente ? nomeCliente.value : "Cliente Balcão",
        obs: observacao ? observacao.value : "",
        itens: itensCarrinho,
        total: valorTotal,
        hora: new Date().toLocaleTimeString()
    };

    console.log("Enviando pedido para o KDS:", resumoPedido);
    alert("Pedido enviado com sucesso!");
    limparCarrinho();
}

function salvarCarrinhoLocal() {
    localStorage.setItem("carrinho_sabor_clic", JSON.stringify(itensCarrinho));
}

function carregarCarrinhoSalvo() {
    let dadosSalvos = localStorage.getItem("carrinho_sabor_clic");
    if (dadosSalvos) {
        itensCarrinho = JSON.parse(dadosSalvos);
        atualizarInterface();
    }
}

function formatarPreco(valor) {
    return "R$ " + valor.toFixed(2).replace(".", ",");
}

function selecionarMesa(numero) {
    mesaSelecionada = numero;
    let labelMesa = document.getElementById("mesa-atual");
    if (labelMesa) {
        labelMesa.innerText = "Mesa: " + numero;
    }
}
