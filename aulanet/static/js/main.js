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

  // 4. sticky header
  document.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 10) {
      header.classList.add('bg-white/60', 'dark:bg-gray-800/60');
    } else {
      header.classList.remove('bg-white/60', 'dark:bg-gray-800/60');
    }
  });

  // 5. redirect del form
  const successMessage = document.querySelector('[data-redirect]');
  if (successMessage) {
    setTimeout(() => {
      window.location.href = successMessage.dataset.redirect;
    }, 2500); // 2.5 segundos (para que coincida un poco con tu animación)
  }

  // 6. Input de Archivos
  const fileInput = document.getElementById('imagenes');
  const fileDisplay = document.getElementById('file-name-display');

  if (fileInput && fileDisplay) {
    fileInput.addEventListener('change', function () {
      if (this.files && this.files.length > 0) {
        if (this.files.length === 1) {
          fileDisplay.textContent = this.files[0].name;
        } else {
          fileDisplay.textContent = `${this.files.length} archivos seleccionados`;
        }
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
        fileDisplay.textContent = 'Seleccionar imágenes...';
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
  }
});
