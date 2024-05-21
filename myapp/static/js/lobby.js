document.addEventListener('DOMContentLoaded', function() {
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
