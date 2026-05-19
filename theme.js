(function () {
  var STORAGE_KEY = 'ielts-theme';
  var root = document.documentElement;

  // Apply saved theme immediately (before render) to avoid flash
  if (localStorage.getItem(STORAGE_KEY) === 'dark') {
    root.classList.add('dark');
  }

  function getIsDark() {
    return root.classList.contains('dark');
  }

  function updateButton(btn) {
    if (!btn) return;
    var isDark = getIsDark();
    // Sun icon for dark mode (click to go light), Moon icon for light mode (click to go dark)
    btn.innerHTML = isDark
      ? '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
      : '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    btn.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
    btn.setAttribute('aria-label', btn.title);
  }

  function toggle() {
    var isDark = root.classList.toggle('dark');
    localStorage.setItem(STORAGE_KEY, isDark ? 'dark' : 'light');
    document.querySelectorAll('#theme-toggle').forEach(updateButton);
  }

  function init() {
    document.querySelectorAll('#theme-toggle').forEach(function (btn) {
      updateButton(btn);
      btn.addEventListener('click', toggle);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose globally so pages can call toggle programmatically if needed
  window.themeToggle = toggle;
})();
