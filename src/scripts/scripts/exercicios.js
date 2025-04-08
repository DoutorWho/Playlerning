// Função para fazer requisição à API
// Obtém a query string da URL (tudo após o '?')
const queryString = window.location.search;

// Cria um objeto URLSearchParams para trabalhar com os parâmetros
const urlParams = new URLSearchParams(queryString);

// Exemplo: Obtendo o valor de um parâmetro específico (por exemplo, "modo")
const curso = urlParams.get('curso');
const disciplina = urlParams.get('disciplina');

// Exibindo o valor de 'modo' no console

fetch(`/api/atividadesapi?curso=${curso}&disciplina=${disciplina}`, { 
    method: 'POST', // Caso precise enviar algo, ajuste o método e o corpo aqui
    headers: {
        'Content-Type': 'application/json'
    }
})
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error(`Erro na API: ${resposta.statusText}`);
        }
        return resposta.json();
    })
    .then(atividade => {
        const perguntas = atividade; // Supondo que a API retorna as perguntas
        console.log("As perguntas são: ", perguntas)

        let perguntaAtual = 0;
        let acertos = 0;

        const perguntaEl = document.getElementById("pergunta");
        const alternativa1El = document.getElementById("alternativa1");
        const alternativa2El = document.getElementById("alternativa2");
        const alternativa3El = document.getElementById("alternativa3");
        const alternativa4El = document.getElementById("alternativa4");
        const confirmarBtn = document.getElementById("confirmar");
        const resultadoArea = document.getElementById("resultado");
        const resultadoForm = document.getElementById("resultado-form");
        const voltarBtn = document.getElementById("voltar-inicio");

        // Função para carregar a pergunta
        function carregarPergunta() {
            let pergunta = perguntas[perguntaAtual];
            perguntaEl.innerHTML = pergunta.pergunta;
            alternativa1El.innerHTML = pergunta.alternativas[0];
            alternativa2El.innerHTML = pergunta.alternativas[1];
            alternativa3El.innerHTML = pergunta.alternativas[2];
            alternativa4El.innerHTML = pergunta.alternativas[3];
        }

        // Função para verificar a resposta e atualizar o progresso
        confirmarBtn.addEventListener("click", function() {
            let respostaSelecionada = document.querySelector('input[name="resposta"]:checked');
            if (respostaSelecionada) {
                let respostaSelecionadaTexto = parseInt(respostaSelecionada.value) - 1; // Ajuste do índice da resposta

                let respostaCorretaTexto = parseInt(perguntas[perguntaAtual]['resposta']); // Resposta correta da API

                if (respostaSelecionadaTexto === respostaCorretaTexto) {
                    acertos++;
                }

                perguntaAtual++;

                if (perguntaAtual < perguntas.length) {
                    carregarPergunta();
                } else {
                    let porcentagemAcertos = (acertos / perguntas.length) * 100;
                    let mensagemFinal;
                    if (acertos >= perguntas.length / 2) {
                        mensagemFinal = `Parabéns, você passou! Você acertou ${porcentagemAcertos.toFixed(2)}% das perguntas.`;
                        resultadoForm.querySelector("#respostas").value = porcentagemAcertos.toFixed(2);
                        resultadoForm.submit(); // Envia os resultados
                    } else {
                        mensagemFinal = `Você não passou. Acertou ${porcentagemAcertos.toFixed(2)}% das perguntas. Tente novamente!`;
                        resultadoArea.innerHTML = mensagemFinal;
                        confirmarBtn.style.display = 'none';
                        voltarBtn.style.display = 'block';
                    }
                }
            }
        });

        voltarBtn.addEventListener("click", function() {
            window.location.reload(); // Reinicia a página ao clicar
        });

        carregarPergunta(); // Carrega a primeira pergunta
    })
    .catch(error => console.error('Erro ao carregar atividades:', error));
