const api = 'http://localhost:8000';
let userId = ''; // Ідентифікатор користувача

// Встановлення userId з модального вікна
function setUserId() {
  const input = document.getElementById('modal-user-id');
  userId = input.value.trim();
  if (userId) {
    document.getElementById('user-id-modal').style.display = 'none';
    alert(`Ваш ID встановлено: ${userId}`);
  } else {
    alert('Будь ласка, введіть ваш ID.');
  }
}

// Створення нового тамагочі
async function createNewTamagochi(event) {
  event.preventDefault(); // Запобігаємо перезавантаженню сторінки

  const newUserId = document.getElementById('new-user-id').value.trim();
  const tamagochiName = document.getElementById('new-tamagochi-name').value.trim();

  if (!newUserId || !tamagochiName) {
    alert('Будь ласка, введіть UID та ім\'я тамагочі.');
    return;
  }

  try {
    const res = await fetch(`${api}/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: newUserId, name: tamagochiName }),
    });

    if (!res.ok) {
      throw new Error('Помилка сервера при створенні тамагочі.');
    }

    const data = await res.json();
    if (data.message) {
      alert(data.message); // Відображаємо повідомлення сервера
    } else {
      alert('Сервер не повернув повідомлення.');
    }

    userId = newUserId;
    document.getElementById('tamagochi-name').innerText = tamagochiName; // Відображаємо ім'я
    document.getElementById('user-id-modal').style.display = 'none';
  } catch (error) {
    console.error('Error creating tamagochi:', error);
    alert('Не вдалося створити тамагочі. Спробуйте ще раз.');
  }
}

// Повернення до існуючого тамагочі
async function returnToExistingTamagochi(event) {
  event.preventDefault(); // Запобігаємо перезавантаженню сторінки

  const existingUserId = document.getElementById('existing-user-id').value.trim();

  if (!existingUserId) {
    alert('Будь ласка, введіть UID.');
    return;
  }

  try {
    const res = await fetch(`${api}/status/${existingUserId}`);
    if (!res.ok) throw new Error('Тамагочі з таким UID не знайдено.');

    const data = await res.json();
    userId = existingUserId;
    document.getElementById('tamagochi-name').innerText = data.state.name;
    document.getElementById('user-id-modal').style.display = 'none';
    alert('Ви успішно повернулися до свого тамагочі!');
  } catch (error) {
    console.error('Error returning to tamagochi:', error);
    alert('Не вдалося знайти тамагочі. Спробуйте ще раз.');
  }
}

// Показати поле для зміни userId
function showUserIdInput() {
  const container = document.getElementById('user-id-container');
  container.classList.remove('hidden');
}

// Оновлення userId
function updateUserId() {
  const input = document.getElementById('user-id');
  userId = input.value.trim();
  if (userId) {
    alert(`Ваш ID оновлено: ${userId}`);
  } else {
    alert('Будь ласка, введіть ваш ID.');
  }
}

// Універсальна функція для виконання дій (feed/play)
async function performAction(endpoint, successMessage) {
  try {
    changeImageToGif(); // Змінюємо зображення на гіфку
    const res = await fetch(`${api}/${endpoint}/${userId}`, { method: 'POST' });
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
    const statusRes = await fetch(`${api}/status/${userId}`);
    const statusData = await statusRes.json();
    console.log(statusData);
    document.getElementById('status').innerText = 
      `Ситість: ${statusData.state.satiety}, Щастя: ${statusData.state.happiness}`;

    // Оновлюємо емоції
    const feelingsRes = await fetch(`${api}/feelings/${userId}`);
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
