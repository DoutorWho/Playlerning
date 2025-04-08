document.addEventListener('DOMContentLoaded', function() {
  // parte do playlearning
  const profileLink = document.getElementById("profile-link");
  const learnLink = document.getElementById('learn-link');
  const missionsLink = document.getElementById('missions-link');
  const ranksLink = document.getElementById("ranks-link");
  const settingsLink = document.getElementById("settings-link");  // Corrigido o nome
  
  // Toggle dark mode
  const darkModeToggle = document.getElementById('dark-mode-toggle');

  // playlearning links
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

  if (settingsLink) {
    settingsLink.addEventListener("click", function() {
      window.location.href = "/status/configuracoes";
    });
  }

  // dark mode toggle
  if (darkModeToggle) {
    darkModeToggle.addEventListener('change', () => {
      document.body.classList.toggle('dark-mode');
    });
  }

  // Placeholder for changing password
  const changePasswordBtn = document.getElementById('change-password');
  if (changePasswordBtn) {
    changePasswordBtn.addEventListener('click', () => {
      window.location.href = "/configuracoes/mudar-senha";
    });

  }    

  // Placeholder for opening a ticket
  const openTicketBtn = document.getElementById('open-ticket');
  if (openTicketBtn) {
    openTicketBtn.addEventListener('click', () => {
      window.location.href = "/forum";
    });
  }

  // Placeholder for logging out
  const logoutBtn = document.getElementById('logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      window.location.href = "/configuracoes/sair-conta";
    });
  }

  const deletarConta = document.getElementById("delete-account");
  if (deletarConta) {
    deletarConta.addEventListener("click", () => {
      window.location.href = "/configuracoes/excluir-conta"
    });
  }

  // Handle navigation to settings
  const contentSection = document.querySelector('.custom-content');
  const settingsSection = document.querySelector('.settings-section');
  const blocksSection = document.querySelector('.blocks-container');

  if (settingsLink && blocksSection && settingsSection && contentSection) {
    settingsLink.addEventListener('click', () => {
      blocksSection.classList.add('hidden');  // Hide blocks
      settingsSection.style.display = 'block';  // Show settings
      contentSection.style.transform = 'translateX(100%)';  // Slide the content to the right
    });
  }

});
