
const botaoTema = document.createElement('button');

botaoTema.id = 'botao-tema';
botaoTema.type = 'button';

function aplicarTema(tema) {
    document.documentElement.setAttribute('data-tema', tema);

    if (tema === 'escuro') {
        botaoTema.textContent = '☀️ Modo claro';
        botaoTema.setAttribute('aria-label', 'Ativar modo claro');
        botaoTema.setAttribute('aria-pressed', 'true');
    } else {
        botaoTema.textContent = '🌙 Modo escuro';
        botaoTema.setAttribute('aria-label', 'Ativar modo escuro');
        botaoTema.setAttribute('aria-pressed', 'false');
    }

    localStorage.setItem('tema-sabor-clic', tema);
}

const temaSalvo = localStorage.getItem('tema-sabor-clic') || 'claro';

aplicarTema(temaSalvo);

botaoTema.addEventListener('click', function () {
    const temaAtual = document.documentElement.getAttribute('data-tema');

    aplicarTema(temaAtual === 'escuro' ? 'claro' : 'escuro');
});

document.body.appendChild(botaoTema);
