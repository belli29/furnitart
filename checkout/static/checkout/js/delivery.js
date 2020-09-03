// enable/disable checkout button and resume section if bag contais items not deliverable to the shipping destination
$( document ).ready(function() {
    var euroShippingString = $(".euro-shipping").text()
    var onlyIeShipping = euroShippingString.includes("False")  
    if (onlyIeShipping){
        var shippingCountry = $("select[name='country']").val();
        if (shippingCountry != 'IE'){
            $("#payment-section").addClass("d-none");
            $("#resume-section").addClass("d-none");
            var url = "checkout/delivery_issue";
            $.get(url);
            }else {
            $("#payment-section").removeClass("d-none");
            $("#resume-section").removeClass("d-none");
        }; 
    }; 
});

// check if the new shiping desitnation creates problems and recalculates shipping fees
$('select[name="country"]').change( function(){
    // define if there are items in bag only deliverable to Ireland
    var euroShippingString = $(".euro-shipping").text()
    var onlyIeShipping = euroShippingString.includes("False")
    // if previous was true and delivery coutry is not Ireland , amend DOM accordingly
    if (onlyIeShipping){
        var shippingCountry = $("select[name='country']").val();
        if (shippingCountry != 'IE'){
            $("#payment-section").addClass("d-none");
            $("#resume-section").addClass("d-none");
            var deliveryIssue = true;
            }else {
            $("#payment-section").removeClass("d-none");
            $("#resume-section").removeClass("d-none");
        }; 
    };
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
    var parameters = $.param( getData )
    if (deliveryIssue){
        var parameters = parameters +"&delivery_issue=true"
    };
    window.location.href = `/checkout/?${parameters}`; 
    if (deliveryIssue){
        var parameters = parameters +"&delivery_issue=true"
    }; 
})
