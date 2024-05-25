document.addEventListener("DOMContentLoaded", function() {
    // Modal functionality
    setupModalFunctionality();

    // Scroll position functionality
    setupScrollPosition();

    // Password field toggle functionality
    setupPasswordFieldToggle();
});

// Modal functionality
function setupModalFunctionality() {
    const span = document.querySelector(".close");

    // Close modal when clicking on <span> (x)
   if (span) {
        span.onclick = () => closeAllModals();
    }

    // Close modal when clicking outside the modal
    window.onclick = event => {
        if (event.target.classList.contains("modal")) {
            closeAllModals();
        }
    };
}

function closeAllModals() {
    const modals = document.querySelectorAll(".modal");
    modals.forEach(modal => modal.style.display = "none");
}

// Scroll position functionality
function setupScrollPosition() {
    const allLobbies = document.getElementById('allLobbies');
    const userLobbies = document.getElementById('userLobbies');

    // Restore scroll position
    if (allLobbies) {
        allLobbies.scrollTop = localStorage.getItem('allLobbiesScrollPosition') || 0;
    }
    if (userLobbies) {
        userLobbies.scrollTop = localStorage.getItem('userLobbiesScrollPosition') || 0;
    }

    // Save scroll position
    window.addEventListener('beforeunload', () => {
        if (allLobbies) {
            localStorage.setItem('allLobbiesScrollPosition', allLobbies.scrollTop);
        }
        if (userLobbies) {
            localStorage.setItem('userLobbiesScrollPosition', userLobbies.scrollTop);
        }
    });
}

// Password field toggle functionality
function setupPasswordFieldToggle() {
    const isPrivateCheckbox = document.getElementById('id_is_private');
    const passwordField = document.getElementById('passwordField');

    if (isPrivateCheckbox && passwordField) {
        isPrivateCheckbox.addEventListener('change', function() {
            passwordField.style.display = this.checked ? 'block' : 'none';
        });

        // Check on page load
        passwordField.style.display = isPrivateCheckbox.checked ? 'block' : 'none';
    }
}

// Show the modal with lobby id
function showJoinModal(lobbyId, isPrivate) {
    if (isPrivate) {
        document.getElementById("modal_lobby_id").value = lobbyId;
        document.getElementById("joinModal").style.display = "block";
    } else {
        // Submit the form directly for public lobbies
        submitJoinLobbyForm(lobbyId);
    }
}

// Close the modal
function closeJoinModal() {
    document.getElementById("joinModal").style.display = "none";
}

// Submit join lobby form
function submitJoinLobbyForm(lobbyId) {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = window.location.href;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    const lobbyIdInput = document.createElement('input');
    lobbyIdInput.type = 'hidden';
    lobbyIdInput.name = 'lobby_id';
    lobbyIdInput.value = lobbyId;
    form.appendChild(lobbyIdInput);

    const joinInput = document.createElement('input');
    joinInput.type = 'hidden';
    joinInput.name = 'join_lobby';
    joinInput.value = '1';
    form.appendChild(joinInput);

    document.body.appendChild(form);
    form.submit();
}

// Toggle filter menu
function toggleFilterMenu() {
    const filterMenu = document.getElementById("filterMenu");
    filterMenu.style.display = filterMenu.style.display === "block" ? "none" : "block";
}
