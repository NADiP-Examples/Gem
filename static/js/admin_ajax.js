$(function () {
});

function clear_errors() {
    $("#fill_form").find('li.error').remove()
}

function clear_form() {
    // Удаление формы редактирования
    $('#creation-form').html(' ');
}

function show_errors(errors) {
    // Отображаем ошибки формы
    clear_errors();
    for (var error_name in errors) {
        for (var error in errors[error_name]) {
            $('[name=' + error_name + ']', $("#fill_form")).closest('td').prepend('<li class="error">' + errors[error_name][error].message + '</li>');
        }
        $('[name=' + error_name + ']', $("#fill_form")).parent().addClass('error');
    }

}

function update_objects_list(new_html) {
    $('#objects_list').html(new_html)
}

function send_data(id, url_prefix) {
    // Запрос на создание/редактирование объекта
    var prefix = (id != undefined) ? id : '';
    var user_data = $("#fill_form").serializeArray();
    console.log('user_data = ', user_data);
    $.ajax({
        url: url_prefix + '/create/' + prefix,
        type: 'POST',
        data: user_data,
        dataType: 'json',
        success: function (response) {
            console.log("response = ", response);
            update_objects_list(response.html);
            clear_form();
        },
        error: function (response) {
            var errors = JSON.parse(response.responseJSON.errors);
            show_errors(errors);
        }
    });
}

function get_form(id, url_prefix) {
    // Запрос на получение формы редактирования
    var creation_form = $('#creation-form');
    $.ajax({
        url: url_prefix + '/get_form/' + id,
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            creation_form.html(response.html);
        },
        error: function (xhr, status, error) {
            console.log('error =', error)
        }
    });
}

function delete_object(id, url_prefix) {
    // Запрос на удаление объекта с id
    $.ajax({
        url: url_prefix + '/delete/' + id,
        type: 'DELETE',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function (response) {
            update_objects_list(response.html);
        },
        error: function (xhr, status, error) {
            console.log('error =', error)
        }
    });
}

// Функция взята тут: http://djbook.ru/rel1.7/ref/contrib/csrf.html
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// DEMO-function TEMPLATE
function demo_send_data(id) {
    $.ajax({
        url: '<адрес ajax-запроса>',
        type: 'GET/POST',
        dataType: 'json',
        // Функция, которая будет выполнена при успешном ответе
        success: function (response) {
            console.log("response = ", response);
        },
        // Функция, которая будет выполнена, при ошибке на сервере
        error: function (xhr, status, error) {
            console.log('error =', error)
        }
    });
}

// function recover_base_form(){
//     $('#user_modal').html(base_modal_html);
//     $form = $('#user_form');
// }