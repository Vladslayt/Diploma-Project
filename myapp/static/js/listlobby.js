// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Моковые данные, имитирующие ответ сервера
    const mockLobbies = [
        { id: 1, name: 'Lobby 1', price: 150.00 },
        { id: 2, name: 'Lobby 2', price: 250.00 },
        { id: 3, name: 'Lobby 3', price: 350.00 }
    ];

    // Получаем элемент, куда будем помещать список лобби
    const lobbyList = document.getElementById('lobbyList');

    // Очистим список перед добавлением новых элементов
    lobbyList.innerHTML = '';

    // Создаем и добавляем элементы в список
    mockLobbies.forEach(lobby => {
        const lobbyItem = document.createElement('div');
        lobbyItem.className = 'lobby-item';
        lobbyItem.innerHTML = `<span class="lobby-name">${lobby.name} - ${lobby.price.toFixed(2)} руб.</span>
                                <button class="join-button">войти</button>`;
        lobbyList.appendChild(lobbyItem);
    });

    // Добавляем обработчики событий для кнопок "войти"
    document.querySelectorAll('.join-button').forEach(button => {
        button.addEventListener('click', function() {
            alert('Присоединение к лобби!');
        });
    });

    // Обработчик событий для кнопки создания лобби
    document.getElementById('createLobby').addEventListener('click', function() {
        alert('Создание нового лобби!');
    });
});


/*
document.addEventListener('DOMContentLoaded', function() {
fetch('http://localhost:8000/lobbies/')
    .then(response => response.json())
    .then(data => {
        const lobbyList = document.querySelector('.lobby-list');
        lobbyList.innerHTML = ''; // Очищаем список перед добавлением новых элементов
        data.forEach(lobby => {
            const lobbyItem = document.createElement('div');
            lobbyItem.className = 'lobby-item';
            lobbyItem.innerHTML = `<span class="lobby-name">${lobby.name} - ${lobby.price} руб.</span>
                                <button class="join-button">войти</button>`;
            lobbyList.appendChild(lobbyItem);
        });
    })
    .catch(error => console.error('Error loading the lobbies:', error));
});

document.querySelectorAll('.join-button').forEach(button => {
    button.addEventListener('click', function () {
        alert('Joining the lobby!');
    });
});

document.getElementById('createLobby').addEventListener('click', function () {
    alert('Creating a new lobby!');
});*/







