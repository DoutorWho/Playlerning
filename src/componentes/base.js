document.addEventListener('DOMContentLoaded', function() {
    const profileLink = document.getElementById("profile-link");
    const learnLink = document.getElementById('learn-link');
    const missionsLink = document.getElementById('missions-link');
    const ranksLink = document.getElementById("ranks-link");
    const settingsLink = document.getElementById("settings-link");
    if (profileLink) {
        profileLink.addEventListener("click", function() {
            window.location.href = "/status/perfil";
        });
    }

    if (ranksLink) {
        ranksLink.addEventListener("click", function() {
            window.location.href = "/status/rank";
        });
    }

    if (learnLink) {
        learnLink.addEventListener("click", function() {
            window.location.href = "/"
        });
    }

    if (missionsLink) {
        missionsLink.addEventListener("click", function() {
            window.location.href = "/status/missoes";
        });
    }

    if (settingsLink) {
        settingsLink.addEventListener("click", function() {
            window.location.href = "/status/configuracoes";
        });
    }
    document.querySelectorAll('.nav img').forEach(function(img) {
        img.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            if (document.body.classList.contains('dark-mode')) {
                this.title = "Mudar para modo claro";
                this.src = darkModeIcon;
            } else {
                this.title = "Mudar para modo escuro";
                this.src = lightModeIcon;
            }
        });
    });

// Parte de base para saber se é admin ou não e assim adiviar a nav necessária
fetch('/api/informacoesusarios', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
})
.then(resposta => resposta.json())
.then(cargo => {
    console.log("O cargo é: ", cargo);
    if (cargo['nome'] === null) {
        document.querySelector(".nav").innerHTML += `
        <div class='center-links'>
            <a href="/cursos">Cursos</a>
            <a href="/login">Login</a>
            <a href="/cadastrar">Cadastrar-se</a>
        </div>
        `;
    } else {
        document.querySelector(".nav").innerHTML += `
        <div class='center-links'>
            <a href="/">Página Inicial</a>
            <a href="/cursos">Cursos</a>
            <a href="/admin">Admin</a>
            <a href="/forum">Fórum</a>
        </div>
        <a href="#" id="theme-toggle"  class="left-link emoji"></a>
        `;
        // Adiciona o evento de clique após o elemento ser adicionado ao DOM
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.addEventListener('click', function(event) {
            console.log("Apertei aqui!");
            event.preventDefault(); // Evita o comportamento padrão do link
            alternar(); // Chama a função para alternar o tema
        });
    }
})
.catch(error => console.error('Erro ao carregar constantes:', error));


// Função para alternar o tema
function alternar() {
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    let modo = ''

    // Muda o emoji com base no tema atual
    if (body.classList.contains('dark-mode')) {
        body.classList.remove("dark-mode"); // Remove modo escuro
        modo = 'claro'
        themeToggle.textContent = '🌞'; // Muda para emoji de sol (tema claro)
    } else {
        body.classList.add("dark-mode"); // Adiciona modo escuro
        themeToggle.textContent = '🌜'; // Muda para emoji de lua (tema escuro)
        modo = 'escuro'
    }
    console.log("Enviando!")
    fetch(`/api/modoclaroouescuro?tipo=enviar&modo=${modo}`, { // Altere para a URL da sua API
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    
}

    // Fazer
    fetch('/api/modoclaroouescuro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(resposta => resposta.json())
    .then(modo => {
        const body = document.body;
        if (modo['modo'] === 'claro') { // Aqui é se caso for claro
            body.classList.remove("dark-mode");
        } else {
            body.classList.add("dark-mode"); // Aqui se for escuro
        }
    })
    .catch(error => console.error('Erro ao carregar constantes:', error));

});

