/*
// script.js
document.querySelectorAll('.join-button').forEach(button => {
    button.addEventListener('click', function() {
        alert('Joining the lobby!');
    });
});

document.getElementById('createLobby').addEventListener('click', function() {
    alert('Creating a new lobby!');
});
*/
// Фейковые данные о квартире
const fakeProperty = {
    title: "Уютная квартира в центре города",
    price: "30000 руб/мес",
    rooms: "2 комнаты",
    metro_station: "Маяковская"
};

// Функция для отображения квартиры
function displayProperties(property) {
    const container = document.getElementById('properties');
    const div = document.createElement('div');
    div.className = 'property';
    div.innerHTML = `<h2>${property.title}</h2>
                     <p>Цена: ${property.price}</p>
                     <p>Комнаты: ${property.rooms}</p>
                     <p>Метро: ${property.metro_station}</p>`;
    container.appendChild(div);
}

// Событие для имитации загрузки данных при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    displayProperties(fakeProperty);
});

/*
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;
    const rooms = document.getElementById('rooms').value;
    fetch(`http://127.0.0.1:8000/search/?min_price=${minPrice}&max_price=${maxPrice}&rooms=${rooms}`)
        .then(response => response.json())
        .then(data => displayProperties(data))
        .catch(error => console.error('Ошибка:', error));
});

function displayProperties(properties) {
    const container = document.getElementById('properties');
    container.innerHTML = '';
    properties.forEach(property => {
        const div = document.createElement('div');
        div.className = 'property';
        div.innerHTML = `<h2>${property.title}</h2>
                         <p>Цена: ${property.price}</p>
                         <p>Комнаты: ${property.rooms}</p>
                         <p>Метро: ${property.metro_station}</p>`;
        container.appendChild(div);
    });
}
*/