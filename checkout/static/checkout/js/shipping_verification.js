// enable/disable checkout button and resume section
function deliveryIssue(change=false){
    // check if bag contains any item only deliverable to Ireland
    var euroShippingString = $(".euro-shipping").text()
    var onlyIeShipping = euroShippingString.includes("False")
    
    if (onlyIeShipping){
        var shippingCountry = $("select[name='country']").val();
        if (shippingCountry != 'IE'){
            $("#payment-section").addClass("d-none");
            $("#resume-section").addClass("d-none");
            // avoid realoading when country is changed
            if(change==false){
                var url ='/checkout/shipping_error';
                $.get(url);
            }
                       
        } else {
            $("#payment-section").removeClass("d-none");
            $("#resume-section").removeClass("d-none");
        };    
    }; 

}

// check with page loaded
$( document ).ready(deliveryIssue());

// only load page once
window.onload = function() {
    //considering there aren't any hashes in the urls already
    if(!window.location.hash) {
        //setting window location
        window.location = window.location + '#loaded';
        //using reload() method to reload web page
        window.location.reload();
    }
}
   
// check at changes 
$("select[name='country']").change( function (){
    deliveryIssue(change=true);
}   
);



