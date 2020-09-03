// enable/disable checkout button and resume section if bag contais items not deliverable to the shipping destination
$( document ).ready(function() {
    var euroShippingString = $(".euro-shipping").text()
    var onlyIeShipping = euroShippingString.includes("False")  
    if (onlyIeShipping){
        var ieDelivery = $(".ie-delivery").text();
        if (ieDelivery == "False"){
            $("#delivery-table-row").html('<td class="d-none d-sm-block"></td><td class="text-left text-sm-center"><strong>Delivery not possible to EU:<p>Choose a delivery address in Ireland at next step or edit your bag.</p></strong></td>');
            $("#grand-total-table-row").addClass('d-none');
        }else {
            $("#grand-total-table-row").removeClass('d-none');
        }; 
    }; 
});


