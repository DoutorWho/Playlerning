document.addEventListener('DOMContentLoaded', () => {
    const faqQuestions = document.querySelectorAll('.faq-question');
    const carouselImages = document.querySelector('.carousel-images');
    const images = Array.from(carouselImages.querySelectorAll('img'));
    const prevButton = document.querySelector('.carousel-control.prev');
    const nextButton = document.querySelector('.carousel-control.next');


    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;

            if (answer.classList.contains('hidden')) {
                answer.classList.remove('hidden');
                answer.style.display = 'block'; // Força a exibição quando removido o 'hidden'
            } else {
                answer.classList.add('hidden');
                answer.style.display = 'none'; // Força o ocultamento quando adicionado o 'hidden'
            }
        });
    });

    // Exemplo para o botão "Saiba mais" se você ainda precisar
    const showMoreBtn = document.getElementById('show-more-btn');
    const extraInfo = document.getElementById('extra-info');

    showMoreBtn.addEventListener('click', () => {
        if (extraInfo.classList.contains('hidden')) {
            extraInfo.classList.remove('hidden');
            showMoreBtn.textContent = 'Mostrar menos';
        } else {
            extraInfo.classList.add('hidden');
            showMoreBtn.textContent = 'Saiba mais';
        }
    });

    let index = 0;

    function updateCarousel() {
        const offset = -index * 100;
        carouselImages.style.transform = `translateX(${offset}%)`;
    }

    nextButton.addEventListener('click', () => {
        index = (index + 1) % images.length;
        updateCarousel();
    });

    prevButton.addEventListener('click', () => {
        index = (index - 1 + images.length) % images.length;
        updateCarousel();
    });

    // Initialize carousel position
    updateCarousel();
});
