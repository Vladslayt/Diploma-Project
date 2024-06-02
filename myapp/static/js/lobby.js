document.addEventListener('DOMContentLoaded', () => {
    const coefficientInputs = document.querySelectorAll('input[type="number"].coefficient');
    const modal = document.getElementById("myModal");
    const span = document.querySelector(".close");
    const fieldsButton = document.querySelector('.filter-fields-button');
    const fieldsMenu = document.getElementById('fields-menu');

    // Event listeners for coefficient inputs
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

    // Close modal when clicking on <span> (x) or anywhere outside the modal
    span.onclick = () => modal.style.display = "none";
    window.onclick = event => {
        if (event.target === modal) modal.style.display = "none";
    };

    // Toggle fields menu display
    fieldsButton.addEventListener('click', () => {
        fieldsMenu.style.display = fieldsMenu.style.display === 'block' ? 'none' : 'block';
    });
});

function toggleParticipants() {
    const participantsList = document.getElementById("participants-list");
    participantsList.style.display = participantsList.style.display === "block" ? "none" : "block";
}
