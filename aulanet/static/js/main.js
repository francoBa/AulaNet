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

  const toggleTheme = () => {
    const isDark = root.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  };

  themeToggleBtn?.addEventListener('click', toggleTheme);
  themeToggleMobileBtn?.addEventListener('click', toggleTheme);

  const savedTheme = localStorage.getItem('theme');

  if (savedTheme === 'dark') {
    root.classList.add('dark');
  } else if (savedTheme === 'light') {
    root.classList.remove('dark');
  }

  // sticky header
  document.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (!header) return;

    if (window.scrollY > 10) {
      header.classList.add('bg-[#101e37]/60', 'dark:bg-gray-800/60');
    } else {
      header.classList.remove('bg-[#101e37]/60', 'dark:bg-gray-800/60');
    }
  });

  // redirect del form
  const successMessage = document.querySelector('[data-redirect]');
  if (successMessage) {
    setTimeout(() => {
      window.location.href = successMessage.dataset.redirect;
    }, 2500);
  }

  // Input de Archivos
  const fileInputs = document.querySelectorAll('.js-file-input');

  fileInputs.forEach((input) => {
    input.addEventListener('change', function () {
      // Buscamos el contenedor
      const container = this.closest('label') || this.parentElement;
      const fileDisplay = container.querySelector('.js-file-name');

      if (!fileDisplay) return;

      if (this.files && this.files.length > 0) {
        if (this.files.length === 1) {
          fileDisplay.textContent = this.files[0].name;
        } else {
          fileDisplay.textContent = `${this.files.length} archivos seleccionados`;
        }
        // Estilos de "Activo"
        fileDisplay.classList.remove(
          'italic',
          'text-gray-500',
          'dark:text-gray-400'
        );
        fileDisplay.classList.add(
          'font-medium',
          'text-gray-800',
          'dark:text-white'
        );
      } else {
        // Estilos de "Reset"
        const defaultText =
          fileDisplay.dataset.defaultText || 'Seleccionar archivo...';
        fileDisplay.textContent = defaultText;

        fileDisplay.classList.add(
          'italic',
          'text-gray-500',
          'dark:text-gray-400'
        );
        fileDisplay.classList.remove(
          'font-medium',
          'text-gray-800',
          'dark:text-white'
        );
      }
    });
  });
});
