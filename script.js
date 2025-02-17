let slideIndex = 0;
const slides = document.getElementsByClassName('slides');

function showSlide(index) {
  for (let i = 0; i < slides.length; i++) {
    slides[i].classList.remove('active');
  }
  slides[index].classList.add('active');
}

function changeSlide(n) {
  slideIndex += n;
  if (slideIndex >= slides.length) {
    slideIndex = 0;
  }
  if (slideIndex < 0) {
    slideIndex = slides.length - 1;
  }
  showSlide(slideIndex);
}

// Cambio slide automatico ogni 5 secondi
setInterval(() => {
  changeSlide(1);
}, 5000);
