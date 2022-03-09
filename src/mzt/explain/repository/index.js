var state = {
    save: function () {
        localStorage.formData = JSON.stringify({
            output: $('#output-format input:checked').attr('id'),
            dplans: $('#display-plan input:checked').map(function () {
                return $(this).attr('id');
            }).get(),
            opened: $('button[aria-expanded=true]').map(function () {
                return $(this).attr('aria-controls');
            }).get(),
        });
    },
    load: function () {
        if (localStorage.formData != undefined) {
            var data = JSON.parse(localStorage.formData);
            $('input#' + data.output).click();
            $('#display-plan input').each(function () {
                if (data.dplans.includes($(this).attr('id'))) {
                    $(this).click();
                };
            });
            $('button').each(function () {
                if (data.opened.includes($(this).attr('aria-controls'))) {
                    $($(this).attr('data-target')).collapse('show');
                };
            })
        }
    }
}

$(document).ready(function () {
    // display box change handler
    $('#display-plan input:checkbox').click(function () {
        var selector = '.mode-' + $(this).attr("id")
        $(selector).toggleClass('d-none');
    });

    // output format change handler
    $('#output-format input:radio').change(function () {
        var format = $(this).filter(':checked').val();
        $('img.plan').attr('src', function (i, src) {
            return src.replace(/\.[^/.]+$/, format);
        });
    });

    // clipboard buttons handler
    $('button.clipboard').click(function () {
        navigator.clipboard.writeText($(this).data('content'));
    });

    // save state to local storage when data is changed
    $('input').click(function () {
        state.save();
    });
    $('.collapse').on('shown.bs.collapse hidden.bs.collapse', function () {
        state.save();
    })

    // restore state from local storage when page is loaded
    state.load();
});