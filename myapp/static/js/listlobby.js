document.addEventListener("DOMContentLoaded", function() {
    setupModalFunctionality();

    setupScrollPosition();

    setupPasswordFieldToggle();
});

function setupModalFunctionality() {
    const span = document.querySelector(".close");

   if (span) {
        span.onclick = () => closeAllModals();
    }

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
function setupScrollPosition() {
    const allLobbies = document.getElementById('allLobbies');
    const userLobbies = document.getElementById('userLobbies');

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

function setupPasswordFieldToggle() {
    const isPrivateCheckbox = document.getElementById('id_is_private');
    const passwordField = document.getElementById('passwordField');

    if (isPrivateCheckbox && passwordField) {
        isPrivateCheckbox.addEventListener('change', function() {
            passwordField.style.display = this.checked ? 'block' : 'none';
        });

        passwordField.style.display = isPrivateCheckbox.checked ? 'block' : 'none';
    }
}

function showJoinModal(lobbyId, isPrivate) {
    if (isPrivate) {
        document.getElementById("modal_lobby_id").value = lobbyId;
        document.getElementById("joinModal").style.display = "block";
    } else {
        submitJoinLobbyForm(lobbyId);
    }
}

function closeJoinModal() {
    document.getElementById("joinModal").style.display = "none";
}

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

function toggleFilterMenu() {
    const filterMenu = document.getElementById("filterMenu");
    filterMenu.style.display = filterMenu.style.display === "block" ? "none" : "block";
}
