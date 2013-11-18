$( document ).ready(function() {
    $("table")
        .tablesorter({
            sortList: [[0,0]],
            selectorHeaders: "> thead th"
        })
        .bind('sortEnd', function (event) {
            var th = $(this).find("th");
            th.find(".fa-sort-desc").remove();
            th.find(".fa-sort-asc").remove();
            var sortDesc = '<span class="fa fa-sort-desc"></span>';
            var sortAsc = '<span class="fa fa-sort-asc"></span>';
            $(this).find(".tablesorter-headerDesc").children().append(sortDesc);
            $(this).find(".tablesorter-headerAsc").children().append(sortAsc);
        });

    $('.tip').tooltip();

    open_panel_count = 0;
    function update_toggle_button() {
        $('#expand-fail-btn').text((open_panel_count ? "Collapse" : "Expand") + " All")
    }
    update_toggle_button(); // Run once on page load to text #expand-fail-btn

    $('#expand-fail-btn').click(function() {
        $(open_panel_count ? '.in': '.collapse').collapse(open_panel_count ? 'hide' : 'show');
    });

    $('.collapse').on('shown.bs.collapse', function () {
        open_panel_count++;
        update_toggle_button();
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        open_panel_count--;
        update_toggle_button();
    });

    // bootstrap's radio buttons don't play nicely with jquery for some
    // reason. this gives all btn-groups the radio effect.
    $(".btn-group button").click(function() {
        $(this).addClass('active').siblings('.btn').not(this).removeClass('active');
    });

    $('#fail-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').show();
        $('.job_fail').show();
        $('#expand-fail-btn').prop('disabled', false);
    });

    $('#running-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').hide();
        $('.job_running').show();
        $('#expand-fail-btn').prop('disabled', true);
    });

    $('#pass-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').hide();
        $('.job_pass').show();
        $('#expand-fail-btn').prop('disabled', true);
    });

    $('#all-job-btn').click(function() {
        $('.job_fail_extra').show();
        $('.job').show();
        $('#expand-fail-btn').prop('disabled', false);
    });

});
