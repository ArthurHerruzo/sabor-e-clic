// ==========================================
// PROJETO SABOR E CLIC - SCRIPT PRINCIPAL
// Autor: Guilherme
// Turma: 231 - Artes Visuais e design 
// ==========================================

// Variaveis globais do carrinho de compras
let itensCarrinho = [];
let valorTotal = 0.0;
let statusKds = "aguardando";

// Aguarda o carregamento do HTML da pagina
document.addEventListener("DOMContentLoaded", function() {
    console.log("Iniciando scripts da aplicação Sabor e Clic...");
    
    // Pegando elementos da tela pelo ID
    let btnFinalizar = document.getElementById("btn-finalizar");
    let btnLimpar = document.getElementById("btn-limpar");
    let divCarrinho = document.getElementById("lista-carrinho");
    let spanTotal = document.getElementById("valor-total-exibido");

    // Verificacao simples se os botoes existem na tela
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

    // Chamada inicial para verificar o estado
    atualizarResumo();
});

// Funcao para adicionar item ao carrinho
function adicionarItem(idProduto, nomeProduto, precoProduto) {
    if (!idProduto || !nomeProduto) {
        console.log("Erro: Dados do produto incompletos.");
        return;
    }

    let produtoExistente = false;

    // Percorrendo o array para ver se ja existe o item
    for (let i = 0; i < itensCarrinho.length; i++) {
        if (itensCarrinho[i].id === idProduto) {
            itensCarrinho[i].qtd += 1;
            produtoExistente = true;
            break;
        }
    }

    // Se nao existir, adiciona como novo
    if (!produtoExistente) {
        let novoItem = {
            id: idProduto,
            nome: nomeProduto,
            preco: parseFloat(precoProduto),
            qtd: 1
        };
        itensCarrinho.push(novoItem);
    }

    console.log("Item adicionado: " + nomeProduto);
    atualizarResumo();
}

// Funcao para remover item do carrinho
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
    atualizarResumo();
}

// Recalcula o valor total da compra
function calcularTotal() {
    let soma = 0;
    for (let i = 0; i < itensCarrinho.length; i++) {
        soma += itensCarrinho[i].preco * itensCarrinho[i].qtd;
    }
    valorTotal = soma;
    return valorTotal;
}

// Atualiza os valores exibidos no HTML
function atualizarResumo() {
    let total = calcularTotal();
    let spanTotal = document.getElementById("valor-total-exibido");
    
    if (spanTotal) {
        spanTotal.innerText = "R$ " + total.toFixed(2).replace(".", ",");
    }
    
    console.log("Resumo atualizado. Total de itens: " + itensCarrinho.length);
}

// Limpa todos os itens do carrinho
function limparCarrinho() {
    itensCarrinho = [];
    valorTotal = 0.0;
    atualizarResumo();
    console.log("Carrinho zerado.");
}

// Simula o envio do pedido para o KDS da cozinha
function finalizarPedido() {
    if (itensCarrinho.length === 0) {
        alert("O carrinho esta vazio!");
        return;
    }

    console.log("Enviando pedido para a cozinha...");
    console.log("Itens do pedido:", itensCarrinho);
    console.log("Total:", valorTotal);

    alert("Pedido enviado com sucesso para a cozinha!");
    limparCarrinho();
}

// Funcao utilitaria para formatar valores em Reais
function formatarMoeda(valor) {
    return "R$ " + parseFloat(valor).toFixed(2).replace(".", ",");
}

// Funcoes secundarias para controle do painel KDS
function atualizarStatusKDS(novoStatus) {
    statusKds = novoStatus;
    console.log("Status do KDS alterado para: " + statusKds);
}

function validarCamposFormulario() {
    let nomeCliente = document.getElementById("nome-cliente");
    let mesa = document.getElementById("numero-mesa");

    if (nomeCliente && nomeCliente.value === "") {
        console.log("Nome do cliente nao preenchido.");
        return false;
    }

    return true;
         }
