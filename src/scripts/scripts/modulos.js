document.addEventListener('DOMContentLoaded', function() {
    // Interactivity for the sidebar menu
    const profileLink = document.getElementById("profile-link");
    const learnLink = document.getElementById('learn-link');
    const missionsLink = document.getElementById('missions-link');
    const ranksLink = document.getElementById("ranks-link");
    const settingsLinks = document.getElementById("settings-link");
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
            window.location.href = "/";
        });
    }

    if (missionsLink) {
        missionsLink.addEventListener("click", function() {
            window.location.href = "/status/missoes";
        });
    }

    if (settingsLinks) {
        settingsLinks.addEventListener("click", function() {
            window.location.href = "/status/configuracoes";
        });
    }

    // Redirect functionality for blocks
    // aqui é o redirecionamento do enem
    const languagesBlock = document.getElementById("languages-block");
    const humanitiesBlock = document.getElementById("humanities-block");
    const exactSciencesBlock = document.getElementById("exact-sciences-block");
    const naturalSciencesBlock = document.getElementById("natural-sciences-block");
    // aqui é o redirecionamento de informatica
    const logicblock = document.getElementById('logic-block');
    const cProgrammingBlock = document.getElementById('c-programming-block');
    const databaseBlock = document.getElementById('database-block');

    // aqui é para a parte de progresso
    const tipo = document.getElementById("tipo_categoria").innerHTML; // às vezes o curso não da informática, indentificar e corrigir!
    console.log("O curso é: ", tipo)
    async function progresso() {
        const response = await fetch(`/api/atividades-progresso?tipo_curso=${tipo}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          }
        });
        const disicplinas = await response.json();
        return disicplinas; // Retorna o array de tópicos
      };

      window.onload = async function() {
        try {
          // Busca os tópicos
            const disicplinas = await progresso();

            if (tipo == 'informatica') {
                document.getElementById("progresso_informatica_logica").innerHTML = '📊 Progresso: ' + disicplinas[0].porcentagem
            }
            if (tipo == 'enem') {
                document.getElementById("progresso_enem_linguagens").innerHTML = '📊 Progresso: ' + disicplinas[0].porcentagem // linguaguem
                document.getElementById("progresso_enem_humanas").innerHTML = '📊 Progresso: ' + disicplinas[1].porcentagem // humanas
                document.getElementById("progresso_enem_naturais").innerHTML = '📊 Progresso: ' + disicplinas[2].porcentagem // naturais
                document.getElementById("progresso_enem_exatas").innerHTML = '📊 Progresso: ' + disicplinas[3].porcentagem  // exatas
            }
      
        } catch (error) {
          console.error('Erro ao buscar tópicos:', error);
        }
      };
      
      

    // parte do enem
    if (languagesBlock) {
        languagesBlock.addEventListener("click", function() {
            window.location.href = "/atividades/enem/linguagens"; // Link para Línguas
        });
    }

    if (humanitiesBlock) {
        humanitiesBlock.addEventListener("click", function() {
            window.location.href = "/atividades/enem/humanas"; // Link para Ciências Humanas
        });
    }

    if (exactSciencesBlock) {
        exactSciencesBlock.addEventListener("click", function() {
            window.location.href = "/atividades/enem/exatas"; // Link para Ciências Exatas
        });
    }

    if (naturalSciencesBlock) {
        naturalSciencesBlock.addEventListener("click", function() {
            window.location.href = "/atividades/enem/naturais"; // Link para Ciências Naturais
        });
    }
    
    // parte da informatica
    if (logicblock) {
        logicblock.addEventListener("click", function() {
            window.location.href = "/atividades/informatica/logica"; // Link para Línguas
        });
    }
    if (cProgrammingBlock) {
        cProgrammingBlock.addEventListener("click", function() {
            window.location.href = "/atividades/informatica/programacao"; // Link para Línguas
        });
    }
    if (databaseBlock) {
        databaseBlock.addEventListener("click", function() {
            window.location.href = "/atividades/informatica/bancodedados"; // Link para Línguas
        });
    }
});
