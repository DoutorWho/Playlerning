document.addEventListener('DOMContentLoaded', () => {
    const botaoestudante = document.getElementById('botaoestudante');
    const botaoprofessor = document.getElementById('botaoprofessor');
    const registroFormProfessor = document.getElementById('registroFormProfessor');
    const registroFormAluno = document.getElementById('registroFormAluno');
    const campoEstudante = document.getElementById('campoEstudante');
    const campoProfessor = document.getElementById('campoProfessor');
    const curriculoInput = document.getElementById('curriculo');

    // Função para exibir campos do aluno
    function MostrarFormEstudante() {
        registroFormAluno.classList.remove('hidden');
        registroFormProfessor.classList.add('hidden');
        campoEstudante.classList.remove('hidden');
        campoProfessor.classList.add('hidden');
    }

    // Função para exibir campos do professor
    function MostrarFormProfessor() {
        registroFormProfessor.classList.remove('hidden');
        registroFormAluno.classList.add('hidden');
        campoProfessor.classList.remove('hidden');
        campoEstudante.classList.add('hidden');
    }

    botaoestudante.addEventListener('click', () => {
        MostrarFormEstudante();
    });

    botaoprofessor.addEventListener('click', () => {
        MostrarFormProfessor();
    });


    // Função para validar o tipo de arquivo
    function validarArquivo(event) {
        const file = curriculoInput.files[0];
        if (file) {
            const fileType = file.type;
            const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!validTypes.includes(fileType)) {
                event.preventDefault(); // Impede o envio do formulário
                alert('Por favor, envie um arquivo no formato PDF ou DOC.');
            }
        }
    }

    // Verifica o envio do formulário para professor
    registroFormProfessor.addEventListener('submit', validarArquivo);
});
