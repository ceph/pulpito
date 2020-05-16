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
    var new_url = window.location.pathname + '?' + query_str;
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
    $.getJSON('/_paddles/machine_types/', function(machine_types) {
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

    function populate_nodes_menu(menu_list, page) {
        if (menu_list.children().length == 1) {
            var items = [];
            $.each(machine_types, function(i) {
                var machine_type = machine_types[i];
                var item = "<li><a onclick='navigate_with_modal(&quot;" + page + "?machine_type=" + machine_type +"&quot;)' href='#'>" + machine_type + "</a></li>"
                items.push(item);
            });
            menu_list.append(items);
        }
    }
    var nodes_list = $('#menu-nodes').parent().find('ul');
    populate_nodes_menu(nodes_list, '/nodes/');
    var node_stats_jobs_list = $('#menu-node-stats-jobs').parent().find('ul');
    populate_nodes_menu(node_stats_jobs_list, '/stats/nodes/jobs');
    var node_stats_locks_list = $('#menu-node-stats-locks').parent().find('ul');
    populate_nodes_menu(node_stats_locks_list, '/stats/nodes/locks');
}

function set_suites() {
    $.getJSON('/_paddles/suites/', function(suite_names) {
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

    $('table').stickyTableHeaders();
    $('.tip').tooltip();

    open_panel_count = 0;
    function update_toggle_button() {
        $('#expand-fail-btn').text((open_panel_count ? "Collapse" : "Expand") + " All")
    }
    update_toggle_button(); // Run once on page load to text #expand-fail-btn
    open_desc_count = 0;
    function update_description_button() {
        $('#expand-desc-btn').text((open_desc_count ? "Hide" : "Show") + " Description")
    }
    update_description_button(); // Run once on page load to text #expand-desc-btn

    $('#expand-fail-btn').click(function() {
        var open_rows = $("tr.job:visible").next("tr.job_fail_extra");
        if (open_panel_count) {
            open_rows.find('.in').collapse('hide');
        } else {
            open_rows.find('.collapse').collapse('show');
        }
    });

    function show_hide_desc() {
        var show_columns = ["Description"];
        var hide_columns = [
                "Posted",
                "Started",
                "Updated",
                "Runtime",
                "In Waiting",
                "OS Type",
                "OS Version",
                "Teuthology Branch",
                "Machine",
        ];
        show_columns.forEach( function(item) {
            var i = $('#run-job-table').find("th:contains('" + item + "')").index() + 1
            if (open_desc_count) {
                $('td:nth-child(' + i  + '),th:nth-child(' + i + ')').show();
            } else {
                $('td:nth-child(' + i  + '),th:nth-child(' + i + ')').hide();
            }
        });
        hide_columns.forEach( function(item) {
            var i = $('#run-job-table').find("th:contains('" + item + "')").index() + 1
            if (!open_desc_count) {
                $('td:nth-child(' + i  + '),th:nth-child(' + i + ')').show();
            } else {
                $('td:nth-child(' + i  + '),th:nth-child(' + i + ')').hide();
            }
        });
        update_description_button();
        open_desc_count = (open_desc_count + 1) % 2;
    }
    show_hide_desc();

    $('#expand-desc-btn').click(function () {
        show_hide_desc();
    });

    $('.collapse').not(".panel-collapse").on('shown.bs.collapse', function () {
        open_panel_count++;
        update_toggle_button();
    });

    $('.collapse').not(".panel-collapse").on('hidden.bs.collapse', function () {
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
        $('.job_fail_extra').hide();
        $('.job_queued').show();
        $('#expand-queued-btn').prop('disabled', true);
    });

    $('#fail-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').show();
        $('.job_fail').show();
        $('#expand-fail-btn').prop('disabled', false);
        var fail_jobs_failures = $(".job_fail").next(".job_fail_extra").length
        if (open_panel_count && fail_jobs_failures) {
            $("tr.job:visible").next("tr.job_fail_extra").find(".collapse").collapse("show");
            $("tr.job:hidden").next("tr.job_fail_extra").find(".in").collapse("hide");
        }
    });

    $('#dead-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').show();
        $('.job_dead').show();
        $('#expand-fail-btn').prop('disabled', false);
        var dead_jobs_failures = $(".job_dead").next(".job_fail_extra").length
        if (open_panel_count && dead_jobs_failures) {
            $("tr.job:visible").next("tr.job_fail_extra").find(".collapse").collapse("show");
            $("tr.job:hidden").next("tr.job_fail_extra").find(".in").collapse("hide");
        }
        else {
            $('.job_fail_extra').hide();
        }
    });

    $('#running-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').hide();
        $('.job_running').show();
        $('#expand-fail-btn').prop('disabled', true);
    });

    $('#waiting-job-btn').click(function() {
        $('.job').hide();
        $('.job_fail_extra').hide();
        $('.job_waiting').show();
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
        if (open_panel_count) {
            $("tr.job:visible").next("tr.job_fail_extra").find(".collapse").collapse("show");
        }
    });

    $('#search-dates').datepicker({ format: 'yyyy-mm-dd' });
    $('#search-dates').on('changeDate', function(ev) {
        date = new Date(ev.date);
        date_str = date.toISOString().split("T")[0]
        stack_filter('date', date_str);
    });

    $('#search-branches').typeahead({
        name: 'branches',
        prefetch: '/_paddles/branches/',
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
