document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu
  const navToggle = document.getElementById('navToggle');
  if (navToggle) {
    navToggle.onclick = () => {
      document.getElementById('mobileMenu')?.classList.toggle('hidden');
    };
  }

  // Dark mode
  const root = document.documentElement;

  const toggleTheme = () => {
    const isDark = root.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  };

  document
    .getElementById('themeToggle')
    ?.addEventListener('click', toggleTheme);
  document
    .getElementById('themeToggleMobile')
    ?.addEventListener('click', toggleTheme);

  // Tema guardado
  if (localStorage.getItem('theme') === 'dark') {
    root.classList.add('dark');
  }
});
