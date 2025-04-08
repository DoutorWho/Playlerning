document.addEventListener('DOMContentLoaded', () => {
    const sectionButtons = document.querySelectorAll('.section-btn');
    const unitButtons = document.querySelectorAll('.unit-btn');
    const unitSelection = document.querySelector('.unit-selection');
    const activityInfo = document.querySelector('.activity-info');
    const activityContainer = document.getElementById('activity-container');
    const noActivitiesMessage = document.getElementById('no-activities-message');
    const selectedSection = document.getElementById('selected-section');
    const unitNumber = document.getElementById('unit-number');
    const activityCount = document.getElementById('activity-count');

    let currentSection = '';
    let currentUnit = '';

    // Ação ao escolher uma seção
    sectionButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentSection = button.getAttribute('data-section');
            selectedSection.textContent = currentSection;

            // Mostra a seleção de unidades e esconde qualquer atividade anterior
            unitSelection.classList.remove('hidden');
            clearActivities();
        });
    });

    // Ação ao escolher uma unidade
    unitButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentUnit = button.getAttribute('data-unit');
            unitNumber.textContent = currentUnit;

            // Faz a requisição para a API usando a seção e a unidade selecionadas
            fetchActivities(currentSection, currentUnit);
        });
    });

    // Função para fazer a requisição à API
    async function fetchActivities(section, unit) {
        try {
            activityContainer.innerHTML = ''; // Limpa o conteúdo anterior
            activityInfo.classList.add('hidden');
            noActivitiesMessage.classList.add('hidden');

            // Exibe mensagem de carregando
            const loadingMessage = document.createElement('p');
            loadingMessage.textContent = 'Carregando...';
            activityContainer.appendChild(loadingMessage);

            // Faz a requisição para a API passando a seção e unidade no corpo da requisição
            const response = await fetch(`/api/atividades-logicas-submit?nome=${section}&unidade=${unit}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nome: section, unidade: unit })
            });

            const activities = await response.json();

            activityContainer.removeChild(loadingMessage); // Remove mensagem de carregamento

            // Exibe as atividades retornadas
            if (activities.length === 0) {
                noActivitiesMessage.classList.remove('hidden');
                activityContainer.classList.add('hidden');
            } else {
                displayActivities(activities);
            }
        } catch (error) {
            console.error('Erro ao buscar atividades:', error);
            noActivitiesMessage.classList.remove('hidden');
        }
    }

    // Função para exibir as atividades
    function displayActivities(activities) {
        activityContainer.innerHTML = ''; // Limpa o conteúdo anterior
        activityInfo.classList.remove('hidden');
        activityContainer.classList.remove('hidden');
        activityCount.textContent = `${activities.length} Atividades`;

        activities.forEach(activity => {
            const activityDiv = document.createElement('div');
            activityDiv.className = 'activity';

            // Adiciona a pergunta
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            questionDiv.innerHTML = activity.pergunta; // Mostra a pergunta
            activityDiv.appendChild(questionDiv);

            // Adiciona as respostas
            const answersDiv = document.createElement('div');
            answersDiv.className = 'answers';

            activity.alternativas.forEach((alternativa, index) => {
                const answerDiv = document.createElement('div');
                answerDiv.className = 'answer';
                answerDiv.innerHTML = alternativa; // Mostra a alternativa

                // Marca a resposta correta
                if (index.toString() === activity.resposta) {
                    answerDiv.classList.add('correct');
                }

                answersDiv.appendChild(answerDiv);
            });

            activityDiv.appendChild(answersDiv);
            activityContainer.appendChild(activityDiv);
        });
    }

    // Função para limpar atividades anteriores
    function clearActivities() {
        activityContainer.innerHTML = ''; // Limpa o conteúdo
        activityInfo.classList.add('hidden');
        noActivitiesMessage.classList.add('hidden');
        activityContainer.classList.add('hidden');
    }
});
