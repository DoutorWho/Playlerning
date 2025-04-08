function abrirAba() {
    // Exibe a aba com o conteúdo do livro
    document.getElementById('nova-aba').style.display = 'block';
    document.getElementById('modal-overlay').style.display = 'block'; // Exibe o overlay

    // parte para chamar o titulo e a descrição
    titulo = document.getElementById("titulo");
    descricao = document.getElementById("descricao");

    // Obtém os valores de data-unidade e data-disciplina
    var secao = this.getAttribute('data-secao');
    var disciplina = this.getAttribute('data-disciplina');
    var unidade = parseInt(this.getAttribute('data-unidade'));
    // configurar aqui oq vai aparecer na tela do usuário
    if ((secao == 'informatica') && (disciplina == 'logica') && (unidade == 1)) {
        titulo.textContent = "Unidade 1 | Lógica Básica"
        descricao.textContent  = 'Nessa unidade, você aprenderá sobre lógica básica'
    }
}

function fecharAba() {
    // Oculta a nova aba
    document.getElementById('nova-aba').style.display = 'none';
    document.getElementById('modal-overlay').style.display = 'none'; // Esconde o overlay
}

// Quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", function () {
    // Ação
    var abrir = document.getElementById('livro');
    var fechar = document.getElementById('fechar');

    // Ações ao clicar
    abrir.addEventListener('click', abrirAba);
    fechar.addEventListener('click', fecharAba);
});
