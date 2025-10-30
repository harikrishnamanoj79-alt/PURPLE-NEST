// HERO SLIDER
let slides = document.querySelectorAll('.hero-slider .slide');
let currentSlide = 0;
let slideInterval = setInterval(nextSlide, 5000);

function nextSlide() {
  slides[currentSlide].classList.remove('active');
  currentSlide = (currentSlide+1) % slides.length;
  slides[currentSlide].classList.add('active');
}

slides[0].classList.add('active');

// MOBILE NAV TOGGLE
const menuToggle = document.createElement('div');
menuToggle.className = 'menu-toggle';
menuToggle.innerHTML = '&#9776;';
document.querySelector('.navbar').prepend(menuToggle);

const navLinks = document.querySelector('.nav-links');
menuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('show');
});
