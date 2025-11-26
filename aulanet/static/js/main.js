document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const navToggle = document.getElementById('navToggle');
  if (navToggle) {
    navToggle.onclick = () => {
      document.getElementById('mobileMenu')?.classList.toggle('hidden');
    };
  }

  // Dark mode logic
  const root = document.documentElement;
  const themeToggleBtn = document.getElementById('themeToggle');
  const themeToggleMobileBtn = document.getElementById('themeToggleMobile');

  // 1. Función para cambiar el tema
  const toggleTheme = () => {
    const isDark = root.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  };

  // 2. Asignar eventos
  themeToggleBtn?.addEventListener('click', toggleTheme);
  themeToggleMobileBtn?.addEventListener('click', toggleTheme);

  // 3. Cargar tema guardado
  const savedTheme = localStorage.getItem('theme');

  if (savedTheme === 'dark') {
    root.classList.add('dark');
  } else if (savedTheme === 'light') {
    root.classList.remove('dark');
  }
});
