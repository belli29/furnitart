// check if bag contains any item only deliverable to Ireland
var euroShippingString = $(".euro-shipping").text()
var onlyIeShipping = euroShippingString.includes("False")
// save original value of the table 
var standardTable = $("tbody").html()
// enable/disable checkout button and informs user of a delivery issue
function deliveryIssue(){
    if (onlyIeShipping){
        var shippingCountry = $("select[name='country']").val();
        if (shippingCountry != 'IE'){
            $("#payment-section").addClass("d-none");
            $("tbody").html ("<h4>Some items in your bag cannot be delivered to your shipping destination. Go back to you bag and delete them or change your shipping address</h4>");
        } else {
            $("#payment-section").removeClass("d-none");
            $("tbody").html(standardTable);
        };    
    }; 

}
// check with page loaded
$( document ).ready(deliveryIssue());
// check at changes 
$("select[name='country']").change( function (){
 deliveryIssue()
}   
);



