document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab');
    const allCards = document.querySelectorAll('.card');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remueve clase "active" de todos
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Oculta todos los cards
            allCards.forEach(card => card.classList.add('hidden'));

            // Muestra solo los cards del tab seleccionado
            const category = tab.getAttribute('data-category');
            const matchingCards = document.querySelectorAll(`.card.${category}`);
            matchingCards.forEach(card => card.classList.remove('hidden'));
        });
    });
});
