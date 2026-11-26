/* IntelliCareer interactions: theme, mobile navigation, validation and animations. */
document.addEventListener('DOMContentLoaded', () => {
  // Restore the user's theme preference from localStorage.
  const savedTheme = localStorage.getItem('intell career-theme');
  if (savedTheme === 'dark') document.body.classList.add('dark-mode');
  document.querySelectorAll('.theme-toggle').forEach(button => {
    button.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      localStorage.setItem('intell career-theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    });
  });

  // Mobile hamburger menu.
  const menuButton = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (menuButton && navLinks) menuButton.addEventListener('click', () => navLinks.classList.toggle('open'));

  // Animate numeric dashboard cards when they enter the viewport.
  const counters = document.querySelectorAll('.count-up');
  const countObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting || entry.target.dataset.done) return;
    const element = entry.target, target = Number(element.dataset.count || 0), start = performance.now(), duration = 900;
    element.dataset.done = 'true';
    const tick = now => {
      const progress = Math.min((now - start) / duration, 1);
      element.textContent = Math.round(target * progress);
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }), { threshold: 0.4 });
  counters.forEach(counter => countObserver.observe(counter));

  // Reveal cards on scroll.
  const revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('visible'); revealObserver.unobserve(entry.target); }
  }), { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(item => revealObserver.observe(item));

  // Progress bars use data-width, keeping template expressions out of style attributes.
  document.querySelectorAll('.progress-fill[data-width]').forEach(bar => {
    const width = Math.max(0, Math.min(100, Number(bar.dataset.width) || 0));
    requestAnimationFrame(() => { bar.style.width = `${width}%`; });
  });

  // FAQ accordion: only one item stays open at a time.
  document.querySelectorAll('.faq-question').forEach(button => button.addEventListener('click', () => {
    const item = button.closest('.faq-item');
    document.querySelectorAll('.faq-item').forEach(other => { if (other !== item) other.classList.remove('open'); });
    item.classList.toggle('open');
  }));

  // Client-side required-field validation; server validation remains authoritative.
  const form = document.getElementById('assessmentForm');
  if (form) form.addEventListener('submit', event => {
    let valid = true;
    form.querySelectorAll('select[required]').forEach(select => {
      const error = select.parentElement.querySelector('.field-error');
      if (!select.value) { valid = false; if (error) error.textContent = 'Please choose an option.'; select.classList.add('invalid'); }
      else { if (error) error.textContent = ''; select.classList.remove('invalid'); }
    });
    if (!valid) { event.preventDefault(); return; }
    const button = document.getElementById('submitAssessment');
    if (button) { button.disabled = true; button.textContent = 'Analyzing...'; }
  });

  // Back-to-top control appears after scrolling down.
  const topButton = document.getElementById('backToTop');
  if (topButton) {
    window.addEventListener('scroll', () => topButton.classList.toggle('show', window.scrollY > 400));
    topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }
});
