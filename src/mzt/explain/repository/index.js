// A $( document ).ready() block.
$(document).ready(function () {
    $('#display-mode :checkbox').click(function () {
        var selector = '.mode-' + $(this).attr("id")
        $(selector).toggleClass('d-none');
    });
});