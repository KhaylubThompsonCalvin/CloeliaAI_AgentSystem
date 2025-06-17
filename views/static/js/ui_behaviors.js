document.addEventListener('DOMContentLoaded',() => {
  document.querySelectorAll('.card-toggle').forEach(card => {
    card.addEventListener('touchstart',()=>card.classList.toggle('expanded'));
  });
});
