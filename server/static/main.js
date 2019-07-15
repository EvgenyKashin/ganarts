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

    const twitterButton = document.querySelector('li:nth-child(1)');
    twitterButton.addEventListener('click', e => {
        gtag('event', 'twitter_like_click', {
            'event_category': 'likes'
        });
    });

    const fbButton = document.querySelector('li:nth-child(2)');
    fbButton.addEventListener('click', e => {
        gtag('event', 'fb_like_click', {
            'event_category': 'likes'
        });
    });

    const githubButton = document.querySelector('li:nth-child(3)');
    githubButton.addEventListener('click', e => {
        gtag('event', 'github_like_click', {
            'event_category': 'likes'
        });
    });

    const donateNavigationButton = document.querySelector('li:nth-child(4)');
    donateNavigationButton.addEventListener('click', e => {
        gtag('event', 'donate_navigation_click', {
            'event_category': 'donate'
        });
    });

    const moreInfoButton = document.querySelector('.navbar-toggler');
    moreInfoButton.addEventListener('click', e => {
        gtag('event', 'more_info_click', {
            'event_category': 'info'
        });
    });

    const styleganButton = document.querySelector('.text-muted a:nth-child(1)');
    styleganButton.addEventListener('click', e => {
        gtag('event', 'stylegan_click', {
            'event_category': 'info'
        });
    });

    const superResButton = document.querySelector('.text-muted a:nth-child(2)');
    superResButton.addEventListener('click', e => {
        gtag('event', 'super_res_click', {
            'event_category': 'info'
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