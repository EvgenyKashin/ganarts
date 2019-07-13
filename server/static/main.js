document.addEventListener('DOMContentLoaded', e => {
    const yaButton = document.querySelector('.btn-success');
    yaButton.addEventListener('click', e => {
        gtag('event', 'yandex_donate_click', {
            'event_category': 'donate'
        });
    });

    const paypalButton = document.querySelector('.btn-info');
    paypalButton.addEventListener('click', e => {
        gtag('event', 'paypal_donate_click', {
            'event_category': 'donate'
        });
    });

    const cards = document.querySelectorAll('.card-body');
    cards.forEach(function (card, i, arr) {
        card.addEventListener('click', e => {
            let imgUrl = card.parentNode.href;
            gtag('event', 'img_click', {
                'event_category': 'downloads',
                'event_label': imgUrl
            });
        });
    });

});