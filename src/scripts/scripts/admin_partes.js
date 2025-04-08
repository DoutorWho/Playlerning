// Parte geral

async function buscarDados(nome) {

    const response = await fetch(`/api/buscardadosusuario?nome=${nome}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nome: nome })
    });
    const dados = await response.json();    
    return dados; // Retorna o array de tópicos
  }
  

async function pesquisarUsuarioGeral() {
    const nome = document.getElementById('searchUser').value;
    const informacoes = document.getElementById('informacoes_usuario');
    dados = await buscarDados(nome);
    try {
        const informacoes = document.getElementById('informacoes_usuario');
        document.getElementById('cargo').textContent = dados.cargo; // Altera para o valor do cargo
        document.getElementById('rank').textContent = dados.rank;   // Altera para o valor do rank
        document.getElementById('email').textContent = dados.email; // Altera para o valor do email
        document.getElementById('xp').textContent = dados.xp;       // Altera para o valor do XP
        informacoes.style.display = 'block'
    } catch (error) {
        const informacoes = document.getElementById('informacoes_usuario'); 
        const erroMensagem = document.getElementById('mensagem_erro_usuario');
        informacoes.style.display = 'none';
        erroMensagem.style.display = 'block';

    }
}

// Parte de punição

async function BuscaPunicao(pesquisa) {

    const response = await fetch('/api/listadebanidos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pesquisa: pesquisa })
    });
    const dados = await response.json();

    return dados; // Retorna o array de tópicos
  }
  

async function VerificarPunicao() {
    const nickname = document.getElementById('searchPunishment').value;
    dados = await BuscaPunicao(nickname);
    const erroMensagem = document.getElementById('mensagem_erro_usuario');
    const punicao = document.getElementById('punicao_status');
    if (dados.indentificao == 'Usuário não encontrado' ) {
        punicao.style.display = 'none';
        erroMensagem.textContent = 'Usuário não encontrado';
        erroMensagem.style.display = 'block';
    }
    else if (dados.indentificao == 'Usuário não está banido') {
        punicao.style.display = 'none';
        erroMensagem.textContent = 'Usuário não está banido';
        erroMensagem.style.display = 'block';
    }
    else {
        erroMensagem.style.display = 'none';
        const punicaoStatus = document.getElementById('punicao_status');
        document.getElementById('nome').innerHTML  = `<strong>Nome</strong>: ${dados.nome}`;  
        document.getElementById('email').innerHTML  = `<strong>Email</strong>: ${dados.email}`;  
        document.getElementById('data').innerHTML  = `<strong>Data da Punição</strong>: ${dados.data}`;  
        document.getElementById('status_mensagem').innerHTML  = `<strong>Status</strong>: ${dados.status}`;  
        document.getElementById('motivo').innerHTML  = `<strong>Motivo</strong>: ${dados.motivo}`;  
        document.getElementById('prova').innerHTML  = `<strong>Prova</strong>: ${dados.prova}`;  
        punicaoStatus.style.display = 'block'
    }
}


// Parte de adicionar atividades

var informacoes = '';

// parte para mostrar as atividades no inicial
pesquisarUsuario() // aqui é para chamar a função
async function enem_informatica() {

    const response = await fetch(`/api/veraatividades`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const dados = await response.json();
    return dados; // Retorna o array com as informações de enem ou informática
  }
  

async function pesquisarUsuario() {
    dados = await enem_informatica();
    document.getElementById('quantidade_atividades_informatica').innerHTML = `${dados.informatica} atividades`
    document.getElementById('quantidade_atividades_enem').innerHTML = `${dados.enem} atividades`

};

// continuação

function updateForm() {
    const category = document.getElementById("category").value;
    const programmingSection = document.getElementById("programming-section");
    const enemSection = document.getElementById("enem-section");

    if (category === "informatica") {
        programmingSection.classList.remove("hidden");
        enemSection.classList.add("hidden");
    } else if (category === "enem") {
        enemSection.classList.remove("hidden");
        programmingSection.classList.add("hidden");
    } else {
        programmingSection.classList.add("hidden");
        enemSection.classList.add("hidden");
    }
}

function updateEnemFields() {
    // Função para atualizar campos do ENEM, se necessário
}

function showConfirmation(details) {
    // Cria uma sobreposição com a confirmação das informações
    const overlay = document.createElement('div');
    overlay.classList.add('confirmation-overlay');
    const confirmation = `
        <div class="confirmation-box">
            <h2>Confirme as Informações</h2>
            <p><strong>Unidade:</strong> ${details.unit}</p>
            <p><strong>Pergunta:</strong> ${details.question}</p>
            <p><strong>Respostas:</strong></p>
            <ul>
                ${details.answers.map((answer, index) => `<li>Resposta ${index + 1}: ${answer}</li>`).join('')}
            </ul>
            <p><strong>Resposta Correta:</strong> Resposta ${details.correctAnswerId}</p>
            <button onclick="confirmAndSend()">Enviar Atividade</button>
            <button onclick="cancelConfirmation()">Cancelar</button>
        </div>
    `;


    overlay.innerHTML = confirmation;
    document.body.appendChild(overlay);
}

function cancelConfirmation() {
    // Remove a sobreposição de confirmação
    const overlay = document.querySelector('.confirmation-overlay');
    if (overlay) overlay.remove();
}


function confirmAndSend() {
    // Crie um novo objeto FormData
    const formData = new FormData();

    categoria = document.getElementById("category").value;
    formData.append("categoria", categoria);

    if (categoria == 'enem') {
        disciplina = document.getElementById("subject").value;  // aqui é o seguinte, se a categoria for enem, enviamos a disciplina, e lá na categoria, se a categoria for enem, procuramos a disciplina e pronto! 
        formData.append("disciplina", disciplina);
    }

    
    // Adicionando as informações ao FormData
    formData.append("unidade", informacoes.unit);
    formData.append("pergunta", informacoes.question);
    
    // Adicionando as respostas ao FormData
    informacoes.answers.forEach((answer, index) => {
        formData.append(`questao${index + 1}`, answer); // Adicione as respostas ao FormData
    });
    
    formData.append("resposta_correta", informacoes.correctAnswerId); // Adicione a resposta correta ao FormData

    // Enviar o FormData para o backend usando fetch
    fetch('/api/envio-atividades-submit', {
        method: 'POST',
        body: formData,
    })
    window.location.href = '/admin/adicionaratividades';
}

function addActivity() {
    const category = document.getElementById("category").value;
    let details = {};

    if (category === "informatica") {
        const unit = document.getElementById("unit").value;
        const question = document.getElementById("programming-question").value;
        const correctAnswerId = document.getElementById("correct-answer").value;
        const answers = Array.from(document.querySelectorAll('.answer')).slice(0, 4).map(input => input.value);

        // Valida se a unidade está entre 1 e 4
        if (!["1", "2", "3", "4"].includes(unit)) {
            alert("Por favor, selecione uma unidade válida (1, 2, 3 ou 4).");
            return;
        }

        // Valida se o número da resposta correta está entre 1 e 4
        if (!["1", "2", "3", "4"].includes(correctAnswerId)) {
            alert("Por favor, selecione uma resposta correta válida (1, 2, 3 ou 4).");
            return;
        }

        // Valida se existem exatamente 4 respostas
        if (answers.length !== 4 || answers.some(answer => answer.trim() === "")) {
            alert("Por favor, insira exatamente 4 respostas válidas.");
            return;
        }

        const correctAnswerText = answers[correctAnswerId - 1] || 'Resposta inválida';

        details = { unit, question, answers, correctAnswerId, correctAnswerText };

    } else if (category === "enem") {
        const subject = document.getElementById("subject").value;
        const unit = document.getElementById("enem-unit").value;
        const question = document.getElementById("enem-question").value;
        const correctAnswerId = document.getElementById("enem-correct-answer").value;
        let answers = Array.from(document.querySelectorAll('.answer')).map(input => input.value);

        // Valida a unidade
        if (!["1", "2", "3", "4"].includes(unit)) {
            alert("Por favor, selecione uma unidade válida (1, 2, 3 ou 4).");
            return;
        }

        // Valida a resposta correta
        if (!["1", "2", "3", "4"].includes(correctAnswerId)) {
            alert("Por favor, selecione uma resposta correta válida (1, 2, 3 ou 4).");
            return;
        }

        // Valida se existem exatamente 4 respostas     
        answers = answers.slice(4); // aqui é pq tá dando erro, já que os 4 primeiros ão vaioz graças a informática
        if (answers.length !== 4 || answers.some(answer => answer.trim() === "")) {
            alert("Por favor, insira exatamente 4 respostas válidas.");
            return;
        }

        const correctAnswerText = answers[correctAnswerId - 1] || 'Resposta inválida';

        details = { subject, unit, question, answers, correctAnswerId, correctAnswerText };

    } else {
        alert("Por favor, selecione uma categoria.");
        return;
    }

    informacoes = details;

    // Mostra a confirmação antes de enviar
    showConfirmation(details);
}
