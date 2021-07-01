const stripe = Stripe('pk_test_51IzN5FBE7MCF29mgI6oaJq8joNPAy8IWbDOgVSHOHgjXFD5DdNELwQoIlOrVoSVsi6e8cVowNgWvJP7PPxKJ1tY200yyd6FetQ')

var elem = document.getElementById('submit');

clientsecret = elem.getAttribute('data-secret');

var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        lineHeight: '2.4',
        fontSize: '16px',
    }
};

const card = elements.create("card", {style: style})
card.mount("#card-element");

card.on('change', function (event) {
    var displayError = document.getElementById('card-errors')
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert')
    }
})