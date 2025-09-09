const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const msgInput = document.getElementById('msg');

function appendBubble(text, cls) {
  const el = document.createElement('div');
  el.className = 'chat-bubble ' + cls;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = msgInput.value.trim();
  if (!msg) return;
  appendBubble(msg, 'user');
  msgInput.value = '';
  appendBubble('Typing...', 'bot');
  const typing = chat.lastElementChild;
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: msg})
    });
    const data = await res.json();
    typing.remove();
    appendBubble(data.answer || "I couldn't find an answer.", 'bot');
  } catch (err) {
    typing.remove();
    appendBubble('Network error. Try again later.', 'bot');
  }
});
