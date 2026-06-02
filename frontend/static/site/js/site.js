const revealItems = document.querySelectorAll(".reveal");
const preloader = document.getElementById("preloader");
const cursorGlow = document.getElementById("cursor-glow");
const tiltCards = document.querySelectorAll(".tilt-card");
const scrollProgress = document.getElementById("scroll-progress");
const heroStage = document.querySelector(".hero-stage");
const parallaxLayers = document.querySelectorAll(".parallax-layer");
const siteHeader = document.getElementById("site-header");
const htmlRoot = document.getElementById("html-root");
const langButtons = document.querySelectorAll(".lang-btn");
const countupItems = document.querySelectorAll("[data-countup]");
const navLinks = document.querySelectorAll(".site-nav a");
const gameTabs = document.querySelectorAll(".js-game-tab");
const gamePanels = document.querySelectorAll("[data-game-panel]");
const gameShowcaseTitle = document.getElementById("game-showcase-title");
const gameCatalogTitle = document.getElementById("game-catalog-title");
const gameFilterTitle = document.getElementById("game-filter-title");

const translations = {
  uz: {
    brand_tagline: "Premium gaming account showcase",
    nav_catalog: "Catalog",
    nav_filter: "Filter",
    nav_preview: "Preview",
    nav_dashboard: "Kabinet",
    nav_logout: "Chiqish",
    nav_login: "Kirish",
    nav_signup: "Ro'yxatdan o'tish",
    footer_text: "Telegram bot orqali savdo, account videolari va to'g'ridan-to'g'ri bog'lanish uchun premium showcase.",
    hero_badge: "Elite PUBG Accounts",
    hero_title: "Sheikh premium marketplace for elite gaming accounts",
    hero_text: "Accountlar narxi, category, video preview, rank, skins, K/D va boshqa ma'lumotlar professional katalog ko'rinishida chiqadi. Sotib olingandan keyin credential ochiladi, buyurtma esa Telegramga ham yuboriladi.",
    hero_cta_catalog: "Catalogni ko'rish",
    hero_cta_filter: "Qidiruv va filter",
    inventory_pulse: "Inventory Pulse",
    inventory_text: "Filter, category va provider bo'yicha sotuvga tayyor lotlar.",
    sold_access: "Sold Access",
    successful_orders: "Successful orders",
    stat_account: "Account",
    stat_featured: "Featured",
    stat_platform: "Platform",
    stat_provider: "Payment provider",
    categories: "Kategoriler",
    why_build: "Why This Build",
    why_build_title: "Payment, media upload, filter va premium motion bir loyihada",
    feature_media: "Admin media",
    feature_media_text: "Admin panelda rasm upload, video file yoki embed link orqali kontent boshqariladi.",
    feature_provider: "Telegram savdo",
    feature_provider_text: "Har bir account bo'yicha botga tayyor buyurtma xabari va lichkaga tez bog'lanish oqimi qo'shilgan.",
    feature_telegram: "Telegram alert",
    feature_telegram_text: "To'lov tasdiqlangach buyurtma ma'lumoti Telegram botga yuboriladi.",
    search_filter: "Search & Filter",
    filter_btn: "Filterlash",
    all: "Barchasi",
    game_note: "Tanlangan o'yin uchun alohida vitrin katalog ochilgan. Pastdagi kartalardan kerakli lotni tanlashingiz mumkin.",
    catalog: "Catalog",
    website_login: "Website Login",
    login_title: "Accountga kirish",
    no_account: "Account yo'qmi?",
    signup_now: "Ro'yxatdan o'ting",
    create_website_account: "Create Website Account",
    new_user: "Yangi foydalanuvchi",
    already_have_account: "Oldin account ochilganmi?",
    my_purchases: "Mening sotib olgan accountlarim",
    no_purchase: "Hali xarid yo'q. Catalogdan account tanlang.",
    transactions: "Transactions",
    recent_payments: "So'nggi payment harakatlari",
    purchase_complete: "Purchase complete",
    credential_open: "Credential endi sizga ochiq. Kabinetda ham saqlanadi.",
    choose_provider: "Telegram botga o'tib account bo'yicha tayyor xabar yuboring.",
    login_to_buy: "Telegram orqali sotib olish",
    login_to_view: "Website login yo'q. Savdo va bog'lanish Telegram orqali qilinadi.",
    video_showcase: "Video showcase",
    payment_log: "Payment Log",
    recent_transactions: "So'nggi transactionlar",
    related: "Related",
    other_accounts: "Yana boshqa accountlar",
  },
  ru: {
    brand_tagline: "Премиальная витрина игровых аккаунтов",
    nav_catalog: "Каталог",
    nav_filter: "Фильтр",
    nav_preview: "Превью",
    nav_dashboard: "Кабинет",
    nav_logout: "Выход",
    nav_login: "Войти",
    nav_signup: "Регистрация",
    footer_text: "Продажа через Telegram-бота, видео аккаунтов и прямая связь в премиальном showcase.",
    hero_badge: "Элитные PUBG аккаунты",
    hero_title: "Sheikh — премиальный маркетплейс игровых аккаунтов",
    hero_text: "Здесь показываются цены аккаунтов, категории, видео-превью, ранги, скины, K/D и другие данные в профессиональном каталоге. После покупки открываются креды, а заказ уходит в Telegram.",
    hero_cta_catalog: "Открыть каталог",
    hero_cta_filter: "Поиск и фильтр",
    inventory_pulse: "Инвентарь",
    inventory_text: "Готовые к продаже лоты по фильтру, категории и провайдеру.",
    sold_access: "Продано",
    successful_orders: "Успешные заказы",
    stat_account: "Аккаунты",
    stat_featured: "Витрина",
    stat_platform: "Платформы",
    stat_provider: "Платёжные системы",
    categories: "Категории",
    why_build: "Почему это",
    why_build_title: "Платежи, загрузка медиа, фильтры и премиальная анимация в одном проекте",
    feature_media: "Медиа в админке",
    feature_media_text: "Через админку можно управлять изображениями, видеофайлами и embed-ссылками.",
    feature_provider: "Продажа в Telegram",
    feature_provider_text: "Для каждого аккаунта добавлены готовое сообщение в бота и быстрая связь в личке.",
    feature_telegram: "Telegram уведомления",
    feature_telegram_text: "После подтверждения оплаты заказ отправляется в Telegram-бот.",
    search_filter: "Поиск и фильтр",
    filter_btn: "Фильтровать",
    all: "Все",
    game_note: "Для выбранной игры открыт отдельный витринный каталог. Ниже можно выбрать нужный лот.",
    catalog: "Каталог",
    website_login: "Вход на сайт",
    login_title: "Вход в аккаунт",
    no_account: "Нет аккаунта?",
    signup_now: "Зарегистрируйтесь",
    create_website_account: "Создать аккаунт",
    new_user: "Новый пользователь",
    already_have_account: "Уже есть аккаунт?",
    my_purchases: "Мои купленные аккаунты",
    no_purchase: "Покупок пока нет. Выберите аккаунт в каталоге.",
    transactions: "Транзакции",
    recent_payments: "Последние платежи",
    purchase_complete: "Покупка завершена",
    credential_open: "Данные аккаунта теперь открыты и сохранены в кабинете.",
    choose_provider: "Перейдите в Telegram-бот и отправьте готовое сообщение по аккаунту.",
    login_to_buy: "Купить через Telegram",
    login_to_view: "Вход на сайте не нужен. Продажа и связь идут через Telegram.",
    video_showcase: "Видео-превью",
    payment_log: "Журнал оплат",
    recent_transactions: "Последние транзакции",
    related: "Похожие",
    other_accounts: "Другие аккаунты",
  },
  en: {
    brand_tagline: "Premium gaming account showcase",
    nav_catalog: "Catalog",
    nav_filter: "Filter",
    nav_preview: "Preview",
    nav_dashboard: "Dashboard",
    nav_logout: "Logout",
    nav_login: "Login",
    nav_signup: "Sign up",
    footer_text: "A premium showcase for Telegram bot sales, account videos, and direct contact.",
    hero_badge: "Elite PUBG Accounts",
    hero_title: "Sheikh premium marketplace for elite gaming accounts",
    hero_text: "Account prices, categories, video previews, ranks, skins, K/D, and more are presented in a professional catalog. After purchase, credentials unlock and the order is sent to Telegram.",
    hero_cta_catalog: "View catalog",
    hero_cta_filter: "Search and filter",
    inventory_pulse: "Inventory Pulse",
    inventory_text: "Ready-to-sell lots by filter, category, and provider.",
    sold_access: "Sold Access",
    successful_orders: "Successful orders",
    stat_account: "Accounts",
    stat_featured: "Featured",
    stat_platform: "Platforms",
    stat_provider: "Payment providers",
    categories: "Categories",
    why_build: "Why This Build",
    why_build_title: "Payments, media upload, filters, and premium motion in one project",
    feature_media: "Admin media",
    feature_media_text: "Images, video files, and embed links are managed from the admin panel.",
    feature_provider: "Telegram sales",
    feature_provider_text: "Each account includes a ready-to-send bot message and a direct contact route.",
    feature_telegram: "Telegram alert",
    feature_telegram_text: "Once payment is confirmed, order details are sent to a Telegram bot.",
    search_filter: "Search & Filter",
    filter_btn: "Filter",
    all: "All",
    game_note: "A dedicated showcase catalog is open for the selected game. Pick the lot you want below.",
    catalog: "Catalog",
    website_login: "Website Login",
    login_title: "Sign in to your account",
    no_account: "No account yet?",
    signup_now: "Create one",
    create_website_account: "Create Website Account",
    new_user: "New user",
    already_have_account: "Already have an account?",
    my_purchases: "My purchased accounts",
    no_purchase: "No purchases yet. Choose an account from the catalog.",
    transactions: "Transactions",
    recent_payments: "Recent payment activity",
    purchase_complete: "Purchase complete",
    credential_open: "Your credentials are now unlocked and also saved in the dashboard.",
    choose_provider: "Open the Telegram bot and send the prepared message for this account.",
    login_to_buy: "Buy via Telegram",
    login_to_view: "No website login is needed. Sales and contact happen through Telegram.",
    video_showcase: "Video showcase",
    payment_log: "Payment Log",
    recent_transactions: "Recent transactions",
    related: "Related",
    other_accounts: "Other accounts",
  },
};

function applyLanguage(lang) {
  const dict = translations[lang] || translations.uz;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (dict[key]) {
      element.textContent = dict[key];
    }
  });
  langButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.lang === lang);
  });
  if (htmlRoot) {
    htmlRoot.lang = lang;
  }
  window.localStorage.setItem("sheikh_lang", lang);
}

window.addEventListener("load", () => {
  window.setTimeout(() => {
    preloader?.classList.add("is-hidden");
  }, 500);
  const savedLang = window.localStorage.getItem("sheikh_lang") || "uz";
  applyLanguage(savedLang);
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
      }
    });
  },
  { threshold: 0.14 },
);

revealItems.forEach((item, index) => {
  item.style.transitionDelay = `${index * 45}ms`;
  observer.observe(item);
});

function animateCountup(element) {
  if (!element || element.dataset.counted === "true") return;
  const target = Number(element.dataset.countup || 0);
  const duration = 900;
  const start = performance.now();

  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const value = Math.round(target * (1 - (1 - progress) * (1 - progress)));
    element.textContent = String(value);
    if (progress < 1) {
      window.requestAnimationFrame(frame);
    } else {
      element.dataset.counted = "true";
      element.textContent = String(target);
    }
  }

  window.requestAnimationFrame(frame);
}

const countupObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCountup(entry.target);
        countupObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.5 },
);

countupItems.forEach((item) => {
  countupObserver.observe(item);
});

document.addEventListener("pointermove", (event) => {
  if (!cursorGlow) return;
  cursorGlow.style.left = `${event.clientX}px`;
  cursorGlow.style.top = `${event.clientY}px`;
});

document.addEventListener("scroll", () => {
  if (!scrollProgress) return;
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const progress = maxScroll > 0 ? (window.scrollY / maxScroll) * 100 : 0;
  scrollProgress.style.width = `${progress}%`;
});

if (heroStage && parallaxLayers.length > 0) {
  heroStage.addEventListener("pointermove", (event) => {
    const rect = heroStage.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;

    parallaxLayers.forEach((layer) => {
      const depth = Number(layer.dataset.depth || 10);
      const moveX = x * depth;
      const moveY = y * depth;
      layer.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
    });
  });

  heroStage.addEventListener("pointerleave", () => {
    parallaxLayers.forEach((layer) => {
      layer.style.transform = "";
    });
  });
}

if (siteHeader) {
  siteHeader.addEventListener("pointermove", (event) => {
    const rect = siteHeader.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    siteHeader.style.transform = `perspective(1200px) rotateX(${y * -2.4}deg) rotateY(${x * 3.2}deg)`;
  });

  siteHeader.addEventListener("pointerleave", () => {
    siteHeader.style.transform = "";
  });
}

langButtons.forEach((button) => {
  button.addEventListener("click", () => {
    applyLanguage(button.dataset.lang);
  });
});

tiltCards.forEach((card) => {
  card.addEventListener("pointermove", (event) => {
    const rect = card.getBoundingClientRect();
    const rotateX = ((event.clientY - rect.top) / rect.height - 0.5) * -8;
    const rotateY = ((event.clientX - rect.left) / rect.width - 0.5) * 8;
    card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
  });

  card.addEventListener("pointerleave", () => {
    card.style.transform = "";
  });
});

navLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    const rect = link.getBoundingClientRect();
    const ripple = document.createElement("span");
    ripple.className = "nav-ripple";
    ripple.style.left = `${event.clientX - rect.left}px`;
    ripple.style.top = `${event.clientY - rect.top}px`;
    link.appendChild(ripple);
    window.setTimeout(() => ripple.remove(), 650);
  });
});

function setActiveGame(game) {
  const activeTab = document.querySelector(`.js-game-tab[data-game-tab="${game}"]`);
  if (!activeTab) return;

  gameTabs.forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.gameTab === game);
  });

  gamePanels.forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.gamePanel === game);
  });

  const parentPanel = document.querySelector(`.category-showcase [data-game-panel="${game}"]`);
  if (parentPanel) {
    const label = parentPanel.dataset.gameLabel || activeTab.textContent.trim();
    if (gameShowcaseTitle) gameShowcaseTitle.textContent = `${label} kategoriyalari`;
    if (gameFilterTitle) {
      gameFilterTitle.textContent = game === "pubg-mobile" ? "Accountlarni aniq tanlang" : `${label} bo'yicha tez filter`;
    }
    if (gameCatalogTitle) {
      gameCatalogTitle.textContent = parentPanel.dataset.gameHeading || label;
    }
  }

  const url = new URL(window.location.href);
  url.searchParams.set("game", game);
  window.history.replaceState({}, "", `${url.pathname}?${url.searchParams.toString()}#game-showcase`);
}

gameTabs.forEach((tab) => {
  tab.addEventListener("click", (event) => {
    event.preventDefault();
    setActiveGame(tab.dataset.gameTab);
    document.getElementById("game-showcase")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
