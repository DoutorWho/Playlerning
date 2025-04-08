// Função para abrir o modal de novo tópico
function openForm() {
    document.getElementById("new-topic-modal").style.display = "block";
}

// Função para fechar o modal
function closeForm() {
    document.getElementById("new-topic-modal").style.display = "none";
}



// Quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", function () {
    // parte de cargos
    cargo_usuario_topico = document.getElementById('user-role_topico'); // esse aqui é padrão
    var nome_topico = cargo_usuario_topico.textContent 

    if (nome_topico == 'Aluno') {
        cargo_usuario_topico.style.color = "blue"; // Altera a cor para azul
    };
    if (nome_topico == 'Professor') {
        cargo_usuario_topico.style.color = "#228B22"; 
    }

    if (nome_topico == 'Administrador') {
        cargo_usuario_topico.style.color = "red"; 
    }

    if (nome_topico == 'Ceo') {
        cargo_usuario_topico.style.color = "#DAA520"; 
    }

    // aqui é porque intera
    var elementos = document.querySelectorAll('[id^="user-role_coment"]');

    // Itera sobre os elementos e altera a cor do texto
    elementos.forEach(function(elemento) {
        var nome = elemento.textContent;
        console.log("Aqui é muito mais!" + nome);
        if (nome == 'Aluno') {
            elemento.style.color = "blue"; // Altera a cor para azul
        };
        if (nome == 'Professor') {
            elemento.style.color = "#228B22"; 
        }

        if (nome == 'Administrador') {
            elemento.style.color = "red"; 
        }

        if (nome == 'Ceo') {
            elemento.style.color = "#DAA520"; 
        }
    });



    

    // Botões de ação
    const newTopicBtn = document.getElementById("new-topic-btn"); 
    const closeBtn = document.getElementById("close-btn");

    // Ações ao clicar
    newTopicBtn.addEventListener("click", openForm);
    closeBtn.addEventListener("click", closeForm);


    
    
});
