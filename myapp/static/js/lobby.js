/*
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.addForm').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Add form submitted');
            let formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.text())
              .then(data => {
                  console.log('Add form response received');
                  document.body.innerHTML = data;
              })
              .catch(error => console.error('Error:', error));
        });
    });

    document.querySelectorAll('.removeForm').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Remove form submitted');
            let formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.text())
              .then(data => {
                  console.log('Remove form response received');
                  document.body.innerHTML = data;
              })
              .catch(error => console.error('Error:', error));
        });
    });

    const filterForm = document.querySelector('#filterForm');
    if (filterForm) {
        filterForm.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Filter form submitted');
            let formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.text())
              .then(data => {
                  console.log('Filter form response received');
                  document.body.innerHTML = data;
              })
              .catch(error => console.error('Error:', error));
        });
    }
});
*/
