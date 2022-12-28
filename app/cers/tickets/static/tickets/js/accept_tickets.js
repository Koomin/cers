function acceptTicket() {
    $('#accept_ticket').on('click', function (e) {
            $.ajax({
                url: '/accept_ticket/',
                method: 'post',
                data: {
                    'pk': $('#accept_ticket').attr('data-id'),
                    'csrfmiddlewaretoken': window.CSRF_TOKEN,
                },
            });
        }
    )
}


$('body').ready(function () {
    acceptTicket();
});