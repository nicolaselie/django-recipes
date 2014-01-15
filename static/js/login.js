$(document).ready(function() {        
    $('#loginform').submit(function (event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $('#login-info').load(response.logout, function() {
                    $('#logout').click(logout);
                });
            },
        });
        return false;
    });
    
    function logout(event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: 'GET',
            url: $(this).attr('href'),
            success: function(response) {
                $('#login-info').load(response.login);
            },
        });
        return false;
    }
    
    $('#logout').click(logout);
});

