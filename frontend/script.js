const api = 'http://localhost:8000';

async function feed() {
  const res = await fetch(`${api}/feed`, { method: 'POST' });
  const data = await res.json();
  alert(data.message);
  checkFeelings(); // Перевіряємо стан після кожної дії
}

async function play() {
  const res = await fetch(`${api}/play`, { method: 'POST' });
  const data = await res.json();
  alert(data.message);
  checkFeelings(); // Перевіряємо стан після кожної дії
}

async function checkStatus() {
  const res = await fetch(`${api}/status`);
  const data = await res.json();
  document.getElementById('status').innerText = 
    `Hunger: ${data.state.hunger}, Happiness: ${data.state.happiness}`;
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
