$(document).ready(function() {
    function setSelfPickupAddress() {
        var selectedValue = $('#id_delivery_type').val();

        /*
        if (selectedValue == "SELF") {
            $('#div_id_delivery_address').hide();
        } else {
            $('#div_id_delivery_address').show();
        }
        */

        if (selectedValue == "SELF") {
            $("#id_delivery_address").val("ул. Куйбышева 26")
            $("#id_delivery_address").prop("readOnly", true);
        } else {
            $("#id_delivery_address").val("")
            $("#id_delivery_address").prop("readOnly", false);
        }
    }

    setSelfPickupAddress();

    $('#id_delivery_type').on('change', setSelfPickupAddress);
});
