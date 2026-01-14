// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

tg.expand(); // Открыть на весь экран
tg.ready();  // Показать, что приложение готово

// Основной цвет из Telegram
document.documentElement.style.setProperty(
  '--tg-theme-bg-color', 
  tg.themeParams.bg_color || '#ffffff'
);

function search() {
  const price = document.getElementById('price').value;
  const rooms = document.getElementById('rooms').value;
  
  // Имитация поиска
  document.getElementById('results').innerHTML = `
    <div class="apartment">
      <h3>Квартира ${rooms}</h3>
      <p>Цена: ${price} руб.</p>
      <p>Адрес: ул. Примерная, 10</p>
    </div>
  `;
}
