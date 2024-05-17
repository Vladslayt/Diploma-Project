// Получаем модальное окно
const modal = document.getElementById("myModal");
// Получаем элемент <span>, который закрывает модальное окно
const span = document.getElementsByClassName("close")[0];

// Когда пользователь нажимает на <span> (x), закрываем модальное окно
span.onclick = function() {
    modal.style.display = "none";
}

// Когда пользователь нажимает в любое место за пределами модального окна, закрываем его
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}