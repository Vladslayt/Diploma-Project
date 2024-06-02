document.addEventListener("DOMContentLoaded", function() {
    const isPrivateCheckbox = document.getElementById('id_is_private');
    const passwordField = document.getElementById('passwordField');
    const passwordInput = document.getElementById('id_password');

    if (isPrivateCheckbox && passwordField) {
        isPrivateCheckbox.addEventListener('change', function() {
            if (this.checked) {
                passwordField.style.display = 'block';
            } else {
                passwordInput.value = '';
                passwordField.style.display = 'none';
            }
        });

        passwordField.style.display = isPrivateCheckbox.checked ? 'block' : 'none';
    }
});
