$(document).ready(function () {
    $('#display-mode :checkbox').click(function () {
        var selector = '.mode-' + $(this).attr("id")
        $(selector).toggleClass('d-none');
    });
    $('#output-format :radio[name="output-format"]').change(function () {
        var format = $(this).filter(':checked').val();
        $('img.plan').attr('src', function (i, src) {
            return src.replace(/\.[^/.]+$/, format);
        });
    });
});