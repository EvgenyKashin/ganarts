document.addEventListener('DOMContentLoaded', e => {
    const cards = document.querySelectorAll('.card-body');
    cards.forEach(function (card, i, arr) {
        card.addEventListener('click', e => {
            window.location.href = 'images/image_' + i + '.png'
        });
    });
});