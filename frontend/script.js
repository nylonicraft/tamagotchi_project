const api = 'http://localhost:8000';

async function feed() {
  changeImageToGif(); // Змінюємо зображення на гіфку
  const res = await fetch(`${api}/feed`, { method: 'POST' });
  const data = await res.json();
  alert(data.message);
  checkFeelings(); // Перевіряємо стан після кожної дії
  setTimeout(changeImageToJpg, 3000); // Повертаємо зображення через 3 секунди
}

async function play() {
  changeImageToGif(); // Змінюємо зображення на гіфку
  const res = await fetch(`${api}/play`, { method: 'POST' });
  const data = await res.json();
  alert(data.message);
  checkFeelings(); // Перевіряємо стан після кожної дії
  setTimeout(changeImageToJpg, 3000); // Повертаємо зображення через 3 секунди
}

async function checkStatus() {
  const res = await fetch(`${api}/status`);
  const data = await res.json();
  document.getElementById('status').innerText = 
    `Ситість: ${data.state.hunger}, Щастя: ${data.state.happiness}`;
  checkFeelings(); // Перевіряємо стан після кожної дії
}

async function checkFeelings() {
  const res = await fetch(`${api}/feelings`);
  const data = await res.json();
  const emotionDiv = document.getElementById('emotion');
  
  // Очищаємо попереднє повідомлення
  emotionDiv.classList.remove('happy', 'sad');
  
  if (data.emotion.includes("щасливий")) {
    emotionDiv.classList.add('happy');
  } else {
    emotionDiv.classList.add('sad');
  }
  
  emotionDiv.innerText = data.emotion;
}

function changeImageToGif() {
  const img = document.getElementById('tamagochi-image');
  img.src = '/static/media/tamagotchi_dance.gif'; // Шлях до гіфки
}

function changeImageToJpg() {
  const img = document.getElementById('tamagochi-image');
  img.src = '/static/media/tamagotchi.png'; // Шлях до світлини
}
