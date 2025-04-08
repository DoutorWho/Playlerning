// Função para buscar tópicos
async function buscarTopicos() {
  // Suponha que a URL seja: https://example.com/?nome=Joao&idade=25

  // Primeiro, obtenha a string da URL completa
  const urlString = window.location.href;

  // Crie um objeto URL a partir da string
  const url = new URL(urlString);

  // Use URLSearchParams para obter os parâmetros
  const params = new URLSearchParams(url.search);

  // Agora você pode acessar os parâmetros
  const pesquisa = params.get('pesquisa'); // "Joao"

  const response = await fetch(`/api/pesquisartopico?pesquisa=${pesquisa}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ pesquisa: pesquisa })
  });
  const topicos = await response.json();
  return topicos; // Retorna o array de tópicos
}


// Função para exibir tópicos
function displayTopics(topics, page = 1) {
  const topicsPerPage = 10;
  const start = (page - 1) * topicsPerPage;
  const end = start + topicsPerPage;
  const selectedTopics = topics.slice(start, end);

  const topicsList = document.getElementById('topics-list');
  topicsList.innerHTML = ''; // Limpa os tópicos atuais

  selectedTopics.forEach(topic => {
    const topicDiv = document.createElement('div');
    topicDiv.classList.add('topic');

    // Adiciona um evento de clique para redirecionar para a página do tópico
    topicDiv.onclick = () => {
      window.location.href = `/forum/comentarios?topico=${topic.idTopico}`;
    };
    topicDiv.innerHTML = `
      <h2>${topic.nome}</h2>
      <div class="topic-info">
        <span>Categoria: ${topic.categoria}</span>
        <span>Comentários: ${topic.quantidade_comentarios}</span>
        <span>Enviado por: ${topic.autor}</span>
        <span>Data: ${topic.data}</span>
        <span class="status ${topic.status}">
          ${topic.status === 'Ativa' ? 'Sessão Ativa' : 'Sessão Encerrada'}
        </span>
      </div>
    `;

    topicsList.appendChild(topicDiv);
  });
}

// Função para gerar a paginação
function generatePagination(topics) {
  const topicsPerPage = 10;
  const totalPages = Math.ceil(topics.length / topicsPerPage);
  const pagination = document.getElementById('pagination');
  pagination.innerHTML = '';

  const maxPagesToShow = Math.min(totalPages, 4);

  for (let i = 1; i <= maxPagesToShow; i++) {
    const button = document.createElement('button');
    button.textContent = i;
    button.onclick = () => displayTopics(topics, i);
    pagination.appendChild(button);
  }
}

// Exibe a primeira página quando a página carregar
window.onload = async function() {
  try {
    // Busca os tópicos
    const topics = await buscarTopicos();

    // Gera a paginação e exibe a primeira página com os tópicos
    generatePagination(topics);
    displayTopics(topics, 1);

  } catch (error) {
    console.error('Erro ao buscar tópicos:', error);
  }
};

