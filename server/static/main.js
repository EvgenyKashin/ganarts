document.addEventListener('DOMContentLoaded', e => {
    const cards = document.querySelectorAll('.card-body');
    cards.forEach(function (card, i, arr) {
        card.addEventListener('click', e => {
            window.location.href = 'images/image_' + i + '.png'
        });

        // card.addEventListener('onmouseover', e => {
        //     imgs = card.querySelectorAll("img");
        //     imgs[0].style.display = 'none';
        //     imgs[1].style.display = 'block';
        // });
        //
        // card.addEventListener('onmouseout', e => {
        //     imgs = card.querySelectorAll("img");
        //     imgs[0].style.display = 'block';
        //     imgs[1].style.display = 'none';
        // });
    });

    // const imgs = document.querySelectorAll('img');
    // imgs.forEach(function (img, i, arr) {
    //     img.addEventListener('onmouseover', e => {
    //         img.src = 'images/image_0_small.png'
    //     });
    //
    //     img.addEventListener('onmouseout', e => {
    //         img.src = 't_shirt/image_0.png'
    //     });
    // });
});