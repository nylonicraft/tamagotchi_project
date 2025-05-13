const api = 'http://localhost:8000';

// Універсальна функція для виконання дій (feed/play)
async function performAction(endpoint, successMessage) {
  try {
    changeImageToGif(); // Змінюємо зображення на гіфку
    const res = await fetch(`${api}/${endpoint}`, { method: 'POST' });
    const data = await res.json();
    alert(successMessage || data.message);
    await updateStatusAndFeelings(); // Оновлюємо статус і емоції
    setTimeout(changeImageToJpg, 2000); // Повертаємо зображення через 2 секунди
  } catch (error) {
    console.error(`Error performing action: ${endpoint}`, error);
    alert('Щось пішло не так. Спробуйте ще раз.');
  }
}

// Функція для нагодування
function feed() {
  performAction('feed', 'Тамагочі нагодовано!');
}

// Функція для гри
function play() {
  performAction('play', 'Тамагочі пограв!');
}

// Оновлення статусу та емоцій
async function updateStatusAndFeelings() {
  try {
    // Оновлюємо статус
    const statusRes = await fetch(`${api}/status`);
    const statusData = await statusRes.json();
    document.getElementById('status').innerText = 
      `Ситість: ${statusData.state.satiety}, Щастя: ${statusData.state.happiness}`;

    // Оновлюємо емоції
    const feelingsRes = await fetch(`${api}/feelings`);
    const feelingsData = await feelingsRes.json();
    const emotionDiv = document.getElementById('emotion');

    // Очищаємо попередні класи
    emotionDiv.classList.remove('happy', 'sad');

    // Додаємо відповідний клас
    if (feelingsData.emotion.includes("щасливий")) {
      emotionDiv.classList.add('happy');
    } else {
      emotionDiv.classList.add('sad');
    }

    emotionDiv.innerText = feelingsData.emotion;
  } catch (error) {
    console.error('Error updating status or feelings', error);
    alert('Не вдалося оновити статус або емоції.');
  }
}

// Зміна зображення на гіфку
function changeImageToGif() {
  const img = document.getElementById('tamagochi-image');
  img.src = '/static/media/tamagotchi_dance.gif'; // Шлях до гіфки
}

// Зміна зображення на світлину
function changeImageToJpg() {
  const img = document.getElementById('tamagochi-image');
  img.src = '/static/media/tamagotchi.png'; // Шлях до світлини
}
