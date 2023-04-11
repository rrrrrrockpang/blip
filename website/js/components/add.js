$(document).ready(function() {
    $("#contributeBtn").click(function(event) {
        event.stopPropagation();
        $("#contributeModal").css("display", "block");
    });

    $(".close").click(function() {
        $("#contributeModal").css("display", "none");
    }); 

    $(".option-button").click(function() {
        $("#contribute-option").val($(this).attr("data-option"));
    });

    $("#submit-button").click(function() {
        $("#contributeModal").css("display", "none");
        $("#alert").css("display", "block");
        setTimeout(() => $("#alert").css("opacity", "0"), 5000);
    });

    $(window).click(function(event) {
        if ($(event.target).is($("#contributeModal"))) {
            $("#contributeModal").css("display", "none");
        }
    });

});