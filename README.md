<h1 align="center">📚 Plataforma Interativa de Estudos</h1>

<p align="center">
  Uma plataforma gamificada para aprender de forma divertida e eficiente! 🚀<br>
  Desenvolvida com <strong>HTML, CSS, JavaScript, Python (Flask) e SQL (Flask_SQLAlchemy)</strong>.
</p>

<hr>

<h2>📌 Sobre o Projeto</h2>

<p>
  Esta é uma plataforma de estudos interativa com elementos de gamificação, onde os usuários evoluem por meio de ranks, missões e atividades. A estrutura é dividida em dois modos: <strong>Aluno</strong> e <strong>Professor</strong>.
</p>

<ul>
  <li>🎯 <strong>Ranks:</strong> Bronze, Prata, Ouro, Platina e Diamante</li>
  <li>🎮 <strong>Modos de Estudo:</strong> ENEM e Informática</li>
  <li>📖 <strong>Estrutura:</strong> Unidades, Livros, Seções e Questionários</li>
  <li>🧠 <strong>Sistema de XP:</strong> Ganhe experiência de acordo com seus acertos!</li>
  <li>🧵 <strong>Fórum:</strong> Dúvidas, respostas e exibição de insígnias (missões)</li>
  <li>👨‍🏫 <strong>Modo Professor:</strong> Criação de conteúdos e interação no fórum</li>
  <li>⚖️ <strong>Políticas de Uso:</strong> Termos de uso, moderação e privacidade</li>
</ul>

<hr>

<h2>🗂 Estrutura de Pastas</h2>

<pre>
📁 public
 ┣ 📂 images        # Imagens públicas
 ┣ 📂 fonts         # Fontes personalizadas
 ┗ 📂 ...           # Outros arquivos estáticos (CSS, JS, etc.)

📁 src
 ┣ 📂 models        # Modelos do banco de dados (SQLAlchemy)
 ┣ 📂 routes        # Rotas da aplicação (Flask)
 ┣ 📂 templates     # Templates HTML (Jinja2)
 ┗ 📂 ...           # Lógica principal do backend
</pre>

<hr>

<h2>📚 Modos de Estudo</h2>

<h3>🔸 ENEM</h3>
<ul>
  <li>Exatas</li>
  <li>Linguagens</li>
  <li>Ciências Humanas</li>
  <li>Ciências da Natureza</li>
</ul>

<h3>🔸 Informática</h3>
<ul>
  <li>Lógica de Programação</li>
  <li>Banco de Dados</li>
</ul>

<p>
  Cada disciplina possui 5 unidades, cada unidade contém:
  <ul>
    <li>📘 Um livro explicativo</li>
    <li>📝 5 seções com 10 perguntas cada</li>
    <li>🏆 Sistema de XP baseado no desempenho</li>
    <li>❌ Reprovação caso acerte menos de 50%</li>
  </ul>
</p>

<hr>

<h2>🏅 Missões e Insígnias</h2>

<p>
  O sistema de missões permite que o usuário conquiste insígnias:
</p>

<ul>
  <li>🔥 <strong>Ofensiva de 10 dias:</strong> Acesse por 10 dias seguidos</li>
  <li>🎯 <strong>Meta de XP:</strong> Alcance uma certa quantidade de experiência</li>
</ul>

<p>
  As insígnias são exibidas no perfil do usuário no fórum.
</p>

<hr>

<h2>👥 Modo Aluno vs. Modo Professor</h2>

<table>
  <thead>
    <tr>
      <th>Função</th>
      <th>Aluno</th>
      <th>Professor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Ler Livros</td>
      <td>✅</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Responder Atividades</td>
      <td>✅</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Participar do Fórum</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Criar Atividades</td>
      <td>❌</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Criar Livros</td>
      <td>❌</td>
      <td>✅</td>
    </tr>
  </tbody>
</table>

<p>
  Para se tornar professor, é necessário:
  <ul>
    <li>📄 Enviar currículo</li>
    <li>⏳ Aguardar aprovação da equipe</li>
  </ul>
</p>

<hr>

<h2>🛡 Termos e Privacidade</h2>

<ul>
  <li>📜 Termos de uso bem definidos</li>
  <li>🔐 Política de privacidade</li>
  <li>🛑 Moderação ativa para usuários que descumprirem as regras</li>
</ul>

<hr>

<h2>🧰 Tecnologias Utilizadas</h2>

<ul>
  <li><strong>Frontend:</strong> HTML, CSS, JavaScript</li>
  <li><strong>Backend:</strong> Python com Flask</li>
  <li><strong>Banco de Dados:</strong> SQL com Flask_SQLAlchemy</li>
</ul>

<hr>

<h2>📌 Contribuições</h2>

<p>
  Sinta-se à vontade para contribuir com sugestões, melhorias ou correções!
</p>

<pre>
1. Fork este repositório
2. Crie uma branch: git checkout -b feature/MinhaFuncionalidade
3. Commit suas alterações: git commit -m 'Minha nova funcionalidade'
4. Push para a branch: git push origin feature/MinhaFuncionalidade
5. Abra um Pull Request
</pre>

<hr>

<h2>📧 Contato</h2>

<p>
  Dúvidas ou sugestões? Entre em contato pelo GitHub ou envie uma mensagem!
</p>

<p align="center">
  Feito com ❤️ para transformar o aprendizado em algo divertido e recompensador!
</p>
