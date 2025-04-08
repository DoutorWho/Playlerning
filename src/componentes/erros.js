document.addEventListener('DOMContentLoaded', function() {
    const homeButton = document.getElementById('home-button');
    const homeLink = document.getElementById('home-link');
    
    if (homeButton) {
        homeButton.addEventListener('click', function() {
            window.location.href = '/'; // Substitua '/' pela URL da sua página inicial
        });
    }

    if (homeLink) {
        homeLink.addEventListener('click', function(event) {
            event.preventDefault(); // Previne o comportamento padrão do link
            if (homeButton) {
                homeButton.click(); // Simula o clique do botão
            }
        });
    }
});
