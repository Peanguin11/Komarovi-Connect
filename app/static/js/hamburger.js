const hamburger = document.querySelector(".hamburger");

const center_section = document.querySelector(".center-section");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  center_section.classList.toggle("active");
});
