//comments
function bindPostCommentHandler() {
    $('#form-comment').off();
    $('.delete-comment').off();
    
    $('#form-comment').submit(function() { 
        var data = $('#form-comment').serialize() + '&post=Send';
        var url = $('#form-comment').attr('action');
    
        $.ajax({
            type: 'POST',
            data: data,
            url: url,
            cache: false,
            dataType: 'html',
            success: function(html, textStatus) {
                $('#comment-modal').modal('hide');
                $('#comment-list').append(html);
                bindPostCommentHandler();
                alertify.success('Comment successfuly added.');
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alertify.error('Your comment was unable to be posted at this time. We apologise for the inconvenience.');
            }
        });
        return false;
    });
    
    $('.delete-comment').click(function(event) {
        var $this = $(this);
        event.preventDefault();
        alertify.set({ buttonFocus: "cancel" });
        alertify.confirm('This comment will be permanently deleted. Are you sure?', function(e) {
            if (e) {
                $.ajax({
                    type: 'POST',
                    url: $this.attr('href'),
                    cache: false,
                    success: function(json, textStatus) {
                        alertify.success('Comment successfuly deleted.');
                        $this.parent().parent().remove();
                    },
                    error: function(json, textStatus) {
                        alertify.error('Failed to delete comment.');
                    }
                });
            }
        });
        return false;
    });
}

//rating
function bindPostRatingHandler() {    
    $('#rating').raty({
        cancel: true,
        number: $('#rating').attr('data-number'),
        score: function() {
            var score = $('#rating').attr('data-score');
            if (score != 'None') {
                return parseFloat(score.replace(',','.').replace(' ',''));
            }
            else {
                return 0;
            }
        },
        path: $('#rating').attr('data-path'),
        click: function(score, event) {
            if (score == null) {
                var url = $('#rating').attr('data-unrate-url');
            }
            else {
                var url = $('#rating').attr('data-rate-url');
                url = url.substr(0, url.length-2) + score + '/';
            }
            $.ajax({
                type: 'POST',
                url: url,
                success: function(json) {
                    if (score == null) {
                        alertify.success('Rating successfuly unset.');
                        $('#rating').attr('data-score', json.average_score);
                        bindPostRatingHandler();
                    }
                    else {
                        $('#rating').attr('data-score', json.average_score);
                        bindPostRatingHandler();
                        alertify.success('Rating successfuly set to ' + score + '.');
                    }
                },
                error: function(json) {
                    if (score == null) {
                        alertify.error('Failed to unset rating.');
                    }
                    else {
                        alertify.error('Failed to set rating.');
                    }
                },
            });
        },
        readOnly: function() {
            if ( typeof $(this).attr('data-readonly') === 'undefined') {
                return true;
            }
            else {
                return $(this).attr('data-readonly') == "true";
            }
        }
    });
}

function bindPostLoginHandler() {
    function login(event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: $(this).attr('action'),
            success: function(json) {
                alertify.success('Logged in.');
                $('#login-modal').modal('hide');
                $('#navbar-user').html(json.navbar_user);
                $('.delete-comment[data-author="'+ json.user + '"]').removeClass('hide');
                $('#comment-form').html(json.comment_form);
                $('#form-comment textarea').markdown();
                bindPostCommentHandler();
                $('#rating').raty('readOnly', false);
                $('#logout').click(logout);
            },
            error: function(json) {
                alertify.error('Failed to log in.');
            },
        });
        return false;   
    }
    
    function logout(event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: 'POST',
            url: $(this).attr('href'),
            success: function(json) {
                alertify.success('Logged out.');
                $('#navbar-user').html(json.navbar_user);
                $('#comment-form').empty();
                $('.delete-comment').addClass('hide');
                $('#rating').raty('readOnly', true);
            },
            error: function(json) {
                alertify.error('Failed to log out.');
            },
        });
        return false;
    }
    
    $('.form-signin').submit(login);
    if ( $('#logout').length > 0 ) {
        $('#logout').click(logout);
    }
}

$(document).ready(function() {
    //tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    //comments
    if ( $('#form-comment').length > 0 ) {
        bindPostCommentHandler();
    }
    
    //rating
    if ( $('#rating').length > 0 ) {
        bindPostRatingHandler();
    }

    $('#rating img').tooltip();

    //login
    bindPostLoginHandler();
    
    //csrf protection
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        }
    });
});