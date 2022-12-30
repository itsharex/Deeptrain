const messageBox = document.querySelector('.js-message');
const btn = document.querySelector('.js-message-btn');
const card = document.querySelector('.js-profile-card');
const closeBtn = document.querySelectorAll('.js-message-close');
let closeEditInterface = function() {
    card.classList.remove('active');
}
redirect = function() {
    document.getElementById("profile").innerText = document.getElementById("id_textarea").value.trim();
    closeEditInterface();
}
btn.addEventListener('click',function (e) {
      e.preventDefault();
      card.classList.add('active');
  });

closeBtn.forEach(function (element, index) {
    element.addEventListener('click',function (e) {
        e.preventDefault();
        closeEditInterface();
    });
});