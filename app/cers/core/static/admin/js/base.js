function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {
        $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});
function initializeSelects() {
    $('#subsidiary-context').select2({
        theme: 'admin-autocomplete',
        width: '20px',
    });
    // $('select:not(#subsidiary-context, .actions-wrap select, .field-permissions select)').not('select[class*="admin-autocomplete"]').not('[name*=__prefix__]').select2({
    //     theme: 'admin-autocomplete',
    //     minimumResultsForSearch: 6,
    //     width: '100%',
    // });

}

$('body').on('change', '#subsidiary-context', function () {

    $.ajax({
        url: '/set_subsidiary_context/',
        method: 'post',
        data: {
            'path': window.location.pathname,
            'subsidiary_context': $(this).val(),
        },
        success: function (html) {
            window.location.href = window.location.pathname;
            newPage = $(html);
            title = newPage.find('#branding h2').text();
            if ($('#dashboard-grid').length) {
                $('#page-wrapper').replaceWith($(html).find('#page-wrapper'));
            } else {
                $('.messagelist').remove();
                $('#changelist-wrap').css('align-self', 'initial');
                $('#change-list-extra-wrap').replaceWith($(html).find('#change-list-extra-wrap'));
                $('#changelist-form').replaceWith($(html).find('#changelist-form'));
                $('#top-toolbar').replaceWith($(html).find('#top-toolbar'));
                $('#total-fields').replaceWith($(html).find('#total-fields'));
                $('#changelist-filter').replaceWith($(html).find('#changelist-filter'));
            }
            initializeSelects();
        }
    });
})

$(document).ready(function () {
    initializeSelects();
});
