// payment options UI 
$('.payment-option').click(function () { 
    $(this).addClass("text-color-pr");
    var other_methods = $(this).closest('.row').find('.payment-option').not(this);
    $(other_methods).removeClass("text-color-pr");
});
// Paypal payment
$('#paypal-payment').click(function () { 
    $(".paypal-total").removeClass("d-none"); // display discounted total
    $(".checkout-total").css("text-decoration", "line-through");// total barred 
    $("#paypal_p").removeClass("d-none");// display paypal payment info
    $("#card-element,#card-errors").addClass("d-none");// remove Stripe cc field 
});
// Stripe payment
$('#stripe-payment').click(function () { 
    $(".paypal-total").addClass("d-none");// hide discounted total
    $(".checkout-total").css("text-decoration", "none");// total unbarred 
    $("#card-element").removeClass("d-none");// display Stripe cc field 
    $("#paypal_p").addClass("d-none");// remove paypal payment info
});