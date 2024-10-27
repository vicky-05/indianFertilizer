// fade animation
document.addEventListener("DOMContentLoaded", function () {
  var elements = document.querySelectorAll('.fade-in');

  function checkVisibility() {
    var windowHeight = window.innerHeight;
    elements.forEach(function (element) {
      var elementTop = element.getBoundingClientRect().top;
      if (elementTop < windowHeight) {
        element.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', checkVisibility);
  checkVisibility();  // Check visibility on page load
});
