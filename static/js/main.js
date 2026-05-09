// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// Hamburger menu
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
hamburger?.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Close menu on link click
navLinks?.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

// Contact form submission
const form = document.getElementById('contactForm');
const formMsg = document.getElementById('formMsg');

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = form.querySelector('button[type="submit"]');
  btn.textContent = 'Sending...';
  btn.disabled = true;

  const data = {};
  new FormData(form).forEach((v, k) => data[k] = v);

  try {
    const res = await fetch('/submit-form', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    formMsg.textContent = result.message;
    formMsg.className = 'form-msg success';
    form.reset();
  } catch {
    formMsg.textContent = 'Something went wrong. Please call us directly.';
    formMsg.className = 'form-msg error';
  } finally {
    btn.textContent = 'Send Enquiry';
    btn.disabled = false;
  }
});

// Fade-in animation on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.step-card, .testi-card, .doc-card, .imp-card, .city-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity .6s ease, transform .6s ease';
  observer.observe(el);
});

// Testimonial Slider Logic
const testiGrid = document.querySelector('.testimonials-grid');
const indicatorBar = document.getElementById('testimonialScrollProgress');

if (testiGrid && indicatorBar) {
  const updateProgress = () => {
    const scrollWidth = testiGrid.scrollWidth - testiGrid.clientWidth;
    if (scrollWidth <= 0) {
      indicatorBar.style.width = '100%';
      indicatorBar.style.transform = 'translateX(0)';
      return;
    }
    const barWidth = 60; // px
    const trackWidth = 200; // px
    const progress = (testiGrid.scrollLeft / scrollWidth);
    const moveX = progress * (trackWidth - barWidth);
    indicatorBar.style.width = `${barWidth}px`;
    indicatorBar.style.transform = `translateX(${moveX}px)`;
  };

  testiGrid.addEventListener('scroll', updateProgress);
  window.addEventListener('resize', updateProgress);
  updateProgress(); // Initial call

  // Drag to scroll
  let isDown = false;
  let startX;
  let scrollLeft;

  testiGrid.addEventListener('mousedown', (e) => {
    isDown = true;
    testiGrid.classList.add('active');
    startX = e.pageX - testiGrid.offsetLeft;
    scrollLeft = testiGrid.scrollLeft;
  });

  testiGrid.addEventListener('mouseleave', () => {
    isDown = false;
    testiGrid.classList.remove('active');
  });

  testiGrid.addEventListener('mouseup', () => {
    isDown = false;
    testiGrid.classList.remove('active');
  });

  testiGrid.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - testiGrid.offsetLeft;
    const walk = (x - startX) * 2;
    testiGrid.scrollLeft = scrollLeft - walk;
  });
}
