function addBan() {
    const banInput = document.getElementById('banInput');
    const bannedList = document.getElementById('bannedList');

    if (banInput.value) {
        const newBan = document.createElement('li');
        newBan.innerHTML = `${banInput.value} <button onclick="removeBan('${banInput.value}')">Remover</button>`;
        bannedList.appendChild(newBan);
        banInput.value = ''; // Limpar o campo de entrada
    }
}

function removeBan(user) {
    const bannedList = document.getElementById('bannedList');
    const items = bannedList.getElementsByTagName('li');

    for (let i = 0; i < items.length; i++) {
        if (items[i].textContent.includes(user)) {
            bannedList.removeChild(items[i]);
            break;
        }
    }
}

function showTeacherInfo(teacher) {
    const teacherInfo = document.getElementById('teacherInfo');
    teacherInfo.innerHTML = `<strong>Informações sobre ${teacher}:</strong><br>Email: ${teacher.toLowerCase().replace(' ', '.')}@example.com<br>Curso: Matemática`;
    teacherInfo.classList.remove('hidden');
}

function toggleVisibility(id) {
    const element = document.getElementById(id);
    element.classList.toggle('hidden');
}

function addActivity() {
    const activityInput = document.getElementById('activityInput');
    const activityType = document.getElementById('activityType').value;
    const activityList = document.getElementById('activityList');

    if (activityInput.value) {
        const newActivity = document.createElement('li');
        newActivity.textContent = `${activityType.toUpperCase()}: ${activityInput.value}`;
        activityList.appendChild(newActivity);
        activityInput.value = ''; // Limpar o campo de entrada
    }
}
