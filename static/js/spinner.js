(function($){
    Number.prototype.pad = function() {
        return ('0' + this).slice(-2);
    }
    
    $.widget( "ui.durationspinner", $.ui.spinner, {
        options: {
            // seconds
            step: 1,
            page: 60,
            min: 0,
            max: 24*60*60-1,
        },

        _parse: function( value ) {
            if ( typeof value === "string" ) {
                var arr = value.split(':');
                var sum = 0;
                $.each(arr, function( index, val ) {
                    sum += parseFloat(val)*Math.pow(60, arr.length-index-1) || 0;
                    });
                return sum;
            }
            return value;
        },
        
        _format: function( value ) {
            var hours = Math.floor(value / (60 * 60));

            var divisor_for_minutes = value % (60 * 60);
            var minutes = Math.floor(divisor_for_minutes / 60);
        
            var divisor_for_seconds = divisor_for_minutes % 60;
            var seconds = Math.ceil(divisor_for_seconds);
            
            return hours.pad() + ":" + minutes.pad() + ":" + seconds.pad();
        }
    });

    $(function() {
        var spinner = $(".spinner").durationspinner();
    });
})(django.jQuery);