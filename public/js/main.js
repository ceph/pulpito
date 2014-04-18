function set_paddles_address(address) {
    window.paddles_address = address;
}

function set_filters(filters) {
    window.filters = filters;
}

function table_sortend_callback(event) {
    var th = $(this).find("th");
    th.find(".fa-sort-desc").remove();
    th.find(".fa-sort-asc").remove();
    var sortDesc = '<span class="fa fa-sort-desc"></span>';
    var sortAsc = '<span class="fa fa-sort-asc"></span>';
    $(this).find(".tablesorter-headerDesc").children().append(sortDesc);
    $(this).find(".tablesorter-headerAsc").children().append(sortAsc);
}

function navigate_with_modal(url) {
    $('#processing-modal').modal();
    window.location.href = url;
}

function filter(name, value) {
    if (name == '') {
        var new_url = '/';
    } else {
        var new_url = '/?' + name + '=' + value;
    };
    navigate_with_modal(new_url);
};

function stack_filter(name, value) {
    /* Given a filter name and value, combine it with existing filters and
     * navigate the that query's page. */
    filters = window.filters;
    filters[name] = value;
    var query_str = jQuery.param(filters);
    var new_url = '/?' + query_str;
    navigate_with_modal(new_url);
};

function unstack_filter(name) {
    /* The opposite of stack_filter: removes the given filter, then rebuilds
     * the query and navigates to that page */
    var filters = window.filters;
    delete filters[name];
    if (filters == {}) {
        var new_url = '/';
    } else {
        var query_str = jQuery.param(filters);
        var new_url = '/?' + query_str;
    };
    $('#processing-modal').modal();
    window.location.href = new_url;
}


function set_machine_types() {
    $.getJSON(window.paddles_address + '/runs/machine_type/', function(machine_types) {
        populate_machine_type_menus(machine_types);
    });
}

function populate_machine_type_menus(machine_types) {
    var run_filter_list = $('#menu-machine-type').parent().find('ul');
    if (run_filter_list.children().length == 0) {
        var items = [];
        $.each(machine_types, function(i) {
            var machine_type = machine_types[i];
            var item = "<li><a onclick='stack_filter(&quot;machine_type&quot;, &quot;" + machine_type + "&quot;)' data-toggle='modal' data-target='#processing-modal' href='#'>" + machine_type + "</a></li>";
            items.push(item);
        });
        run_filter_list.append(items);
    }

    var node_stats_list = $('#menu-node-stats').parent().find('ul');
    if (node_stats_list.children().length == 1) {
        var items = [];
        $.each(machine_types, function(i) {
            var machine_type = machine_types[i];
            var item = "<li><a onclick='navigate_with_modal(&quot;/stats/nodes?machine_type=" +machine_type +"&quot;)' href='#'>" + machine_type + "</a></li>"
            items.push(item);
        });
        node_stats_list.append(items);
    }
}

function set_suites() {
    $.getJSON(paddles_address + '/runs/suite/', function(suite_names) {
        populate_suite_menus(suite_names);
    });
}

function populate_suite_menus(suite_names) {
    var suite_list = $('#menu-suites').parent().find('ul');
    if (suite_list.children().length == 0) {
            var items = [];
            $.each(suite_names, function(i) {
                var suite = suite_names[i];
                var item = "<li><a onclick='stack_filter(&quot;suite&quot;, &quot;" + suite + "&quot;)' data-toggle='modal' data-target='#processing-modal' href='#'>" + suite + "</a></li>";
                items.push(item);
            });
            suite_list.append(items);
    }
}

$( document ).ready(function() {
    $("table")
        .tablesorter({
            selectorHeaders: "> thead th"
        })
        .bind('sortEnd', table_sortend_callback);

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

    $('#queued-job-btn').click(function() {
        $('.job').hide();
        $('.job_queued_extra').show();
        $('.job_queued').show();
        $('#expand-queued-btn').prop('disabled', true);
    });

    $('#fail-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').show();
        $('.job_fail').show();
        $('#expand-fail-btn').prop('disabled', false);
    });

    $('#dead-job-btn').click(function() {
        $('.job').hide();
        $('.job_dead_extra').show();
        $('.job_dead').show();
        $('#expand-dead-btn').prop('disabled', true);
    });

    $('#running-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').hide();
        $('.job_running').show();
        $('#expand-fail-btn').prop('disabled', true);
    });

    $('#unknown-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').hide();
        $('.job_unknown').show();
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

    $('#search-dates').datepicker({ format: 'yyyy-mm-dd' });
    $('#search-dates').on('changeDate', function(ev) {
        date = new Date(ev.date);
        date_str = date.toISOString().split("T")[0]
        stack_filter('date', date_str);
    });

    $('#search-branches').typeahead({
        name: 'branches',
        prefetch: paddles_address + '/runs/branch/',
        ttl: 30000,
    });

    $('#search-branches').keypress(function(e) {
        // Enter pressed?
        if(e.which == 10 || e.which == 13) {
            branch = $(this).prop('value');
            stack_filter('branch', branch);
        }
    });

    set_machine_types();
    set_suites();
})
