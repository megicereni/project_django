const qa = [
  // Packages
  { keys: ['package','packages','paketa','destination','where','trip','travel'],
    answer: '✈️ We offer packages to:\n• 🇦🇱 Albania (Berat, Gjirokaster, Sarande)\n• 🇪🇺 Europe (Santorini, Paris, Rome)\n• 🌍 World (Maldives, Tokyo, Bali)\n\nType a destination for details!' },

  // Albania
  { keys: ['berat'],
    answer: '🏛️ <b>Berat – City of 1000 Windows</b>\n📅 1 Day | 💰 €65/person\n🎒 Includes: Transport, Guide, Lunch\n\nVisit the UNESCO Castle, Onufri Museum & the famous Mangalem quarter.' },
  { keys: ['gjirokaster','gjirokastra'],
    answer: '🏰 <b>Gjirokaster – City of Stone</b>\n📅 2 Days | 💰 €100/person\n🎒 Includes: Hotel, Guide, Breakfast\n\nA UNESCO World Heritage site with Ottoman architecture and rich history.' },
  { keys: ['sarande','saranda','ksamil'],
    answer: '🏖️ <b>Sarande & Ksamil</b>\n📅 3 Days | 💰 €180/person\n🎒 Includes: Hotel, Transport, Breakfast\n\nCrystal-clear waters, Butrint UNESCO site & vibrant beach life.' },

  // Europe
  { keys: ['santorini','greece','greek'],
    answer: '🇬🇷 <b>Santorini, Greece</b>\n📅 7 Days | 💰 €799/person\n🎒 Includes: Flight, Hotel, Breakfast, Transfers\n\nWhitewashed villages, volcanic beaches & legendary sunsets from Oia.' },
  { keys: ['paris','france','eiffel'],
    answer: '🇫🇷 <b>Paris, France</b>\n📅 5 Days | 💰 €899/person\n🎒 Includes: Flight, Hotel, Metro Pass, Concert Ticket\n\nEiffel Tower, Louvre, Versailles & a live concert experience!' },
  { keys: ['rome','italy','colosseum','vatican'],
    answer: '🇮🇹 <b>Rome, Italy</b>\n📅 6 Days | 💰 €699/person\n🎒 Includes: Flight, Hotel, Skip-the-line Tickets\n\nColosseum, Vatican, Trevi Fountain & the best pasta of your life!' },

  // World
  { keys: ['maldives','maldive','lagoon','overwater'],
    answer: '🌊 <b>Maldives</b>\n📅 8 Days | 💰 €1,499/person\n🎒 Includes: Flight, Seaplane, Overwater Villa, All-Inclusive\n\nParadise on Earth — perfect for a romantic escape.' },
  { keys: ['tokyo','japan','concert'],
    answer: '🇯🇵 <b>Tokyo + Concert</b>\n📅 9 Days | 💰 €1,299/person\n🎒 Includes: Flight, Hotel, JR Pass, Concert Ticket\n\nNeon lights, temples, cherry blossoms & live music at Tokyo Dome!' },
  { keys: ['bali','indonesia','temple'],
    answer: '🌴 <b>Bali, Indonesia</b>\n📅 10 Days | 💰 €1,149/person\n🎒 Includes: Flight, Villa, Private Driver, Spa, Cooking Class\n\nRice terraces, sacred temples & world-class spa retreats.' },

  // Sport
  { keys: ['sport','football','champions','f1','formula','monaco','wimbledon','tennis'],
    answer: '⚽ <b>Sport Packages</b>\n• Champions League Final – €1,200/person\n• 🏎️ Formula 1 Monaco GP – €1,800/person\n• 🎾 Wimbledon Tennis – €1,100/person\n\nAll include: flight, hotel & event ticket!' },

  // Concert
  { keys: ['concert','music','live','show','london'],
    answer: '🎵 <b>Concert Packages</b>\n• Paris Concert – €899/person\n• London Concert – €950/person\n• Tokyo Concert – included in Tokyo package\n\nAll include: flight, hotel & concert ticket!' },

  // Booking
  { keys: ['book','booking','reserve','reservation','how to book'],
    answer: '📋 <b>How to Book</b>\n1. Go to our Packages page\n2. Choose your destination\n3. Click "Book Now"\n4. Fill in your details\n5. Complete payment\n\n✅ You will receive a confirmation immediately!' },

  // Payment
  { keys: ['pay','payment','card','credit','price','cost','how much'],
    answer: '💳 <b>Payment</b>\nWe accept all major credit/debit cards.\n\nPrices start from:\n• Albania from €65\n• Europe from €699\n• World from €1,149\n\nAll prices are per person and include the listed items.' },

  // Cancellation
  { keys: ['cancel','cancellation','refund','change','modify'],
    answer: '❌ <b>Cancellation Policy</b>\n• 30+ days before: Full refund ✅\n• 15–29 days before: 50% refund\n• Under 15 days: No refund\n\nTo cancel or modify, contact us at miatravel@gmail.com' },

  // Contact
  { keys: ['contact','email','phone','call','reach','support','help'],
    answer: '📞 <b>Contact Us</b>\n📧 miatravel@gmail.com\n📱 +355 69 123 4567\n🌐 www.miatravel.com\n📍 Tirane, Albania\n\nWe\'re available Mon–Sat, 9:00–18:00.' },

  // About
  { keys: ['about','who','company','mia travel','agency'],
    answer: '🌍 <b>About Mia Travel</b>\nWe are a professional travel agency based in Tirana, Albania.\n\nWe specialize in:\n• Cultural & adventure tours\n• Beach holidays\n• Concert & sport event packages\n• Custom travel experiences\n\nYour dream journey starts here! ✈️' },

  // Visa
  { keys: ['visa','passport','document','entry','requirement'],
    answer: '🛂 <b>Visa Information</b>\nRequirements vary by destination:\n• 🇬🇷 Greece: Schengen visa required\n• 🇫🇷 France: Schengen visa required\n• 🇮🇹 Italy: Schengen visa required\n• 🌊 Maldives: Visa on arrival\n• 🇯🇵 Japan: Visa required\n\nWe can assist with visa guidance — contact us!' },

  // Insurance
  { keys: ['insurance','insure','travel insurance','safe','safety'],
    answer: '🛡️ <b>Travel Insurance</b>\nWe strongly recommend travel insurance for all trips.\n\nIt covers:\n• Medical emergencies\n• Trip cancellation\n• Lost luggage\n• Flight delays\n\nAsk us for our recommended insurance partners!' },

  // Hello
  { keys: ['hi','hello','hey','good morning','good afternoon','greet','start'],
    answer: '👋 Hello! Welcome to <b>Mia Travel</b>!\n\nI\'m Mia, your virtual travel assistant. I can help you with:\n• 🗺️ Destination information\n• 💰 Prices & packages\n• 📋 Booking process\n• 📞 Contact details\n\nWhat can I help you with today?' },

  // Thank you
  { keys: ['thank','thanks','thank you','thx','great','awesome','perfect'],
    answer: '😊 You\'re welcome! It\'s my pleasure to help.\n\nIs there anything else you\'d like to know? I\'m always here for you! ✈️' },

  // Bye
  { keys: ['bye','goodbye','see you','ciao','take care'],
    answer: '👋 Goodbye! Have a wonderful day!\n\nWhenever you\'re ready to explore the world, Mia Travel is here. Safe travels! ✈️🌍' },
];

/* ── QUICK REPLY SUGGESTIONS ─────────────── */
const suggestions = [
  '✈️ Packages', '🇦🇱 Albania', '🇪🇺 Europe',
  '🌍 World', '💰 Prices', '📋 How to Book',
  '📞 Contact', '🎵 Concerts', '⚽ Sport'
];

/* ── STATE ───────────────────────────────── */
let isOpen = false;
let isTyping = false;

/* ── TOGGLE ──────────────────────────────── */
function toggleChat() {
  isOpen = !isOpen;
  const win = document.getElementById('chat-window');
  win.style.display = isOpen ? 'flex' : 'none';
  document.getElementById('notifDot').style.display = isOpen ? 'none' : 'flex';
  if (isOpen && document.getElementById('chatMessages').children.length === 0) {
    setTimeout(() => botReply('👋 Hello! Welcome to <b>Mia Travel</b>!\n\nI\'m Mia, your virtual travel assistant 😊\n\nHow can I help you today?'), 400);
    renderQuickReplies();
  }
  if (isOpen) setTimeout(() => document.getElementById('chatInput').focus(), 300);
}

/* ── RENDER QUICK REPLIES ────────────────── */
function renderQuickReplies() {
  const qr = document.getElementById('quickReplies');
  qr.innerHTML = suggestions.map(s =>
    `<button class="qr-btn" onclick="handleQR('${s}')">${s}</button>`
  ).join('');
}

function handleQR(text) {
  addMessage(text, 'user');
  document.getElementById('quickReplies').innerHTML = '';
  processAnswer(text);
}

/* ── SEND MESSAGE ────────────────────────── */
function sendMsg() {
  const input = document.getElementById('chatInput');
  const text  = input.value.trim();
  if (!text || isTyping) return;
  input.value = '';
  addMessage(text, 'user');
  document.getElementById('quickReplies').innerHTML = '';
  processAnswer(text);
}

/* ── FIND ANSWER ─────────────────────────── */
function processAnswer(text) {
  const lower = text.toLowerCase();
  let answer  = null;

  for (const item of qa) {
    if (item.keys.some(k => lower.includes(k))) {
      answer = item.answer;
      break;
    }
  }

  if (!answer) {
    answer = '🤔 I\'m not sure about that, but I can help you with:\n• Package information\n• Prices & booking\n• Destinations\n• Contact details\n\nOr call us: <b>+355 69 123 4567</b>';
  }

  showTyping(answer);
}

/* ── TYPING ANIMATION ────────────────────── */
function showTyping(answer) {
  isTyping = true;
  const msgs = document.getElementById('chatMessages');

  const typingEl = document.createElement('div');
  typingEl.className = 'msg bot typing';
  typingEl.id = 'typingIndicator';
  typingEl.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="msg-bubble">
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>`;
  msgs.appendChild(typingEl);
  msgs.scrollTop = msgs.scrollHeight;

  const delay = Math.min(800 + answer.length * 8, 2200);
  setTimeout(() => {
    typingEl.remove();
    isTyping = false;
    botReply(answer);
    setTimeout(renderQuickReplies, 400);
  }, delay);
}

/* ── ADD MESSAGE ─────────────────────────── */
function addMessage(text, sender) {
  const msgs = document.getElementById('chatMessages');
  const div  = document.createElement('div');
  div.className = `msg ${sender}`;

  if (sender === 'bot') {
    div.innerHTML = `
      <div class="msg-avatar">🤖</div>
      <div class="msg-bubble">${text.replace(/\n/g,'<br>')}</div>`;
  } else {
    div.innerHTML = `<div class="msg-bubble">${text}</div>`;
  }

  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function botReply(text) { addMessage(text, 'bot'); }