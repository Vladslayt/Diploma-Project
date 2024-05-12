function addToSelected(flatId, flatLink, flatPrice) {
    const selectedList = document.getElementById('selectedList');
    const listItem = document.createElement('li');
    listItem.textContent = `${flatLink} - Цена: ${flatPrice}`;
    selectedList.appendChild(listItem);

    // Опционально: скрыть кнопку добавления после использования
    const addButton = document.querySelector(`#flat_${flatId} .add-button`);
    if (addButton) {
        addButton.disabled = true;
        addButton.textContent = 'Добавлено';
    }
}