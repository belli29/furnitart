
// check if the new shiping destination creates problems and recalculates shipping fees
$('select[name="country"]').change( function(){
    var delivery_problem = $('#delivery_problem').text();
    if ( delivery_problem == 'True' ){
        // colleting current delivery selection
        var getData = {
                'full_name': $('input[name="full_name"]').val(),
                'email': $('input[name="email"]').val(),
                'phone_number': $('input[name="phone_number"]').val(),
                'country': $('select[name="country"]').val(),
                'postcode': $('input[name="postcode"]').val(),
                'town_or_city': $('input[name="town_or_city"]').val(),
                'street_address1': $('input[name="street_address1"]').val(),
                'street_address2': $('input[name="street_address2"]').val(),
                'county': $('input[name="county"]').val(),
            };
        var parameters = $.param( getData );
        window.location.href = `/checkout/?${parameters}`
    }

    
})
