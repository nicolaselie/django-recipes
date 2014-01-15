$(document).ready(function() {    
    $('#rating').raty({
        cancel: true,
        number: $('#rating').attr('data-number'),
        score: parseFloat($('#rating').attr('data-score').replace(',','.').replace(' ','')),
        path: $('#rating').attr('data-path'),
        click: function(score, evt) {
            if (score == null) {
                var url = $('#rating').attr('data-unrate-url');
            }
            else {
                var url = $('#rating').attr('data-rate-url');
                url = url.substr(0, url.length-2) + score + '/';
            }
            $.ajax({
                type: 'GET',
                url: url,
            });
        }
    });
});
