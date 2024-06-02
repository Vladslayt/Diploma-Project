document.addEventListener('DOMContentLoaded', () => {
    const coefficientInputs = document.querySelectorAll('input[type="number"].coefficient');
    const modal = document.getElementById("myModal");
    const span = document.querySelector(".close");
    const fieldsButton = document.querySelector('.filter-fields-button');
    const fieldsMenu = document.getElementById('fields-menu');

    coefficientInputs.forEach(input => {
        input.addEventListener('input', () => {
            input.value = Math.max(1, Math.min(5, input.value));
        });

        input.addEventListener('blur', () => {
            if (input.value === '') {
                input.value = 1;
            }
        });
    });

    window.addEventListener('beforeunload', function() {
        localStorage.setItem('scrollPosition', document.getElementById('results').scrollTop);
        localStorage.setItem('scrollPositionSelected', document.getElementById('selectedList').scrollTop);
    });

    if (localStorage.getItem('scrollPosition') !== null) {
        document.getElementById('results').scrollTop = localStorage.getItem('scrollPosition');
    }

    if (localStorage.getItem('scrollPositionSelected') !== null) {
        document.getElementById('selectedList').scrollTop = localStorage.getItem('scrollPositionSelected');
    }

    span.onclick = () => modal.style.display = "none";
    window.onclick = event => {
        if (event.target === modal) modal.style.display = "none";
    };

    fieldsButton.addEventListener('click', () => {
        fieldsMenu.style.display = fieldsMenu.style.display === 'block' ? 'none' : 'block';
    });
});

function toggleParticipants() {
    const participantsList = document.getElementById("participants-list");
    participantsList.style.display = participantsList.style.display === "block" ? "none" : "block";
}
