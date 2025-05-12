const api = 'http://localhost:8000';

async function feed() {
  const res = await fetch(`${api}/feed`, { method: 'POST' });
  const data = await res.json();
  alert(data.message);
}

async function play() {
  const res = await fetch(`${api}/play`, { method: 'POST' });
  const data = await res.json();
  alert(data.message);
}

async function checkStatus() {
  const res = await fetch(`${api}/status`);
  const data = await res.json();
  document.getElementById('status').innerText = 
    `Hunger: ${data.hunger}, Mood: ${data.mood}`;
}