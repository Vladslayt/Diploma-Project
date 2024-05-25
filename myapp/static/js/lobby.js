document.addEventListener('DOMContentLoaded', function() {
    const coefficientInputs = document.querySelectorAll('input[type="number"].coefficient');

    coefficientInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value > 5) {
                this.value = 5;
            } else if (this.value < 1) {
                this.value = 1;
            }
        });

        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.value = 1;
            }
        });
    });

    const modal = document.getElementById("myModal");
    const span = document.querySelector(".close");

    // Close modal when clicking on <span> (x) or anywhere outside the modal
    span.onclick = () => modal.style.display = "none";
    window.onclick = event => {
        if (event.target === modal) modal.style.display = "none";
    };

    // Сохранение положения прокрутки при выходе со страницы
    window.addEventListener('beforeunload', function() {
        localStorage.setItem('scrollPosition', document.getElementById('results').scrollTop);
        localStorage.setItem('scrollPositionSelected', document.getElementById('selectedList').scrollTop);
    });

    // Восстановление положения прокрутки при загрузке страницы
    if (localStorage.getItem('scrollPosition') !== null) {
        document.getElementById('results').scrollTop = localStorage.getItem('scrollPosition');
    }

    if (localStorage.getItem('scrollPositionSelected') !== null) {
        document.getElementById('selectedList').scrollTop = localStorage.getItem('scrollPositionSelected');
    }
});

function toggleParticipants() {
    var participantsList = document.getElementById("participants-list");
    if (participantsList.style.display === "none" || participantsList.style.display === "") {
        participantsList.style.display = "block";
    } else {
        participantsList.style.display = "none";
    }
}
