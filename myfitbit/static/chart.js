
DAY_WIDTH = 5

function make_chart(selector, outer_width, outer_height, day_start_hour, range) {
    var margin = {
        top:    40,
        left:   20,
        bottom: 20,
        right:  20,
    };

    var width = outer_width - margin.left - margin.right;
    var height = outer_height - margin.top - margin.right;

    var sx = d3.scaleTime()
        .domain([range.start, range.end])
        .range([0, width])
    var sy = d3.scaleLinear()
        .domain([day_start_hour, day_start_hour + 24])
        .nice(d3.timeMonth)
        .range([0, height]);

    _one_day = new Date(range.start);
    _one_day.setUTCDate(_one_day.getUTCDate() + 1);
    var day_width = sx(_one_day);

    var ax = d3.axisBottom()
        .scale(sx)
        .tickSize(-height)
        .ticks(12);
    var ay = d3.axisLeft()
        .scale(sy)
        .tickSize(-width)
        .ticks(24)
        .tickFormat(function(d) {
          return ((d + 24) % 24).toLocaleString(undefined, {minimumIntegerDigits:2}) + 'h';
        });

    var root = d3.select(selector);
    var svg = root.append('svg')
        .attr('width', outer_width)
        .attr('height', outer_height);

    var g = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    var gy = g.append('g')
        .call(ay);
    var gx = g.append('g')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(ax);

    gy.selectAll('g.tick line')
        .attr('stroke', '#505050')
        .attr('stroke-dasharray', function(d) {
            if (d % 3 == 0) {
                return '3,' + (day_width - 3);
            }
            return '0.5,' + (day_width - 0.5);
        });

    gx.selectAll('g.tick line')
        .attr('stroke', '#505050')

    return {
        root, svg, g,
        margin, width, height,
        sx, sy, ax, ay,
        day_start_hour, day_width
    };
}

function sleep_chart(sleep, range) {

    var chart = make_chart(
        '#sleep',
        range.count * DAY_WIDTH,
        (1440 / 3 + 20 + 20),
        -6,
        range
    );

    SLEEP_COLORS = {
        'deep':     '#0000f0',
        'light':    '#8080f0',
        'wake':     '#f00000',
        'awake':    '#f00000',
        'rem':      '#00f000',
        'asleep':   '#008080',
        'restless': '#800000'
    };

    function date(x) {
        return new Date(x.date);
    };

    function hours(x) {
        d = new Date(x.dateTime + 'Z');
        var o = d.getUTCDate() == (new Date(x.date)).getUTCDate() ? 0 : -24;
        return o + (
            d.getUTCHours() * 3600 +
            d.getUTCMinutes() * 60 +
            d.getUTCSeconds()
        ) / 3600;
    };

    var legend = ['light', 'deep', 'rem', 'awake', 'asleep'];
    legend.forEach(function(k, i) {
        var x = chart.g.append('g').attr('class', 'legend');
        x.append('rect')
            .attr('fill', SLEEP_COLORS[k])
            .attr('height', 10)
            .attr('width', 10)
            .attr('x', 30 + 80 * i)
            .attr('y', -15);
        x.append('text')
            .attr('x', 45 + 80 * i)
            .attr('y', -5)
            .text(k);
    });

    var rects = [];
    for (var i=0; i<sleep.length; i++) {
        var s = sleep[i];
        for (var j=0; j<s.levels.data.length; j++) {
            var r = s.levels.data[j];
            r.date = s.dateOfSleep;
            rects.push(r);
        }
        for (var j=0; j<s.levels.data.length; j++) {
            var r = s.levels.data[j];
            r.date = s.dateOfSleep;
            rects.push(r);
        }
    }

    var bars = chart.g.selectAll('.bar').data(rects).enter();

    bars.append('rect')
        .attr('class', 'bar')
        .attr('x', function(d) { return chart.sx(date(d)); })
        .attr('y', function(d) { return chart.sy(hours(d)); })
        .attr('height', function(d) { return chart.sy((d.seconds / 3600) + chart.day_start_hour); })
        .attr('width', chart.day_width)
        .attr('fill', function(d) { return SLEEP_COLORS[d.level]; });

}

function heartrate_chart(heartrate, range) {

    var chart = make_chart(
        '#heartrate',
        range.count * DAY_WIDTH,
        1440 / 2,
        0,
        range
    )

    var color = d3.scaleSequential(d3.interpolateViridis)
        .domain([0, 1]);

    var percentile = {};
    all_data = [];
    for (var i=0; i<heartrate.length; i++) {
        all_data = all_data.concat(heartrate[i].minutes);
    }
    all_data.sort(function(a, b) { return a - b; });
    for (var i=0; i<all_data.length; i++) {
        if (all_data[i] != null) { break; }
    }
    all_data.splice(0, i);
    for (var k=0; k<300; k++) {
        var s = 0;
        var e = all_data.length;
        while (s < e) {
            var m = Math.floor((s + e) / 2);
            if (all_data[m] >= k) { e = m; }
            if (all_data[m] < k) { s = m + 1; }
        }
        percentile[k] = s / all_data.length;
    }

    var legend = chart.g.append('g')
        .attr('class', 'legend hr')
        .attr('transform', 'translate(20, -15)');
    legend_width = 401;
    for (var i=0; i<legend_width; i++) {
        var k = all_data[Math.floor(all_data.length * i / legend_width)];
        legend.append('rect')
            .attr('x', i)
            .attr('y', 0)
            .attr('height', 5)
            .attr('width', 2)
            .attr('fill', color(percentile[k]));
        if (i % 50 == 0) {
            legend.append('text')
                .attr('x', i - 5)
                .attr('y', -5)
                .text(k);
        }

    }
    all_data.splice(0, 0);

    for (var i=0; i<heartrate.length; i++) {
        var hr = heartrate[i];
        var d = new Date(hr.date);
        var x = chart.sx(d);
        var h = chart.sy(1 / 60 - chart.day_start_hour) + 1;
        for (var j=0; j<hr.minutes.length; j++) {
            var v = hr.minutes[j];
            if (v === null) { continue; }
            chart.g.append('rect')
                .attr('x', x)
                .attr('y', chart.sy(j / 60))
                .attr('width', chart.day_width)
                .attr('height', h)
                .attr('fill', color(percentile[hr.minutes[j]]));
        }
    }
}

function get_extents(data) {

    var sleep_start = new Date(data.sleep[0].dateOfSleep);
    var sleep_end = new Date(data.sleep[data.sleep.length - 1].dateOfSleep);
    var hr_start = new Date(data.heartrate[0].date);
    var hr_end = new Date(data.heartrate[data.heartrate.length - 1].date);

    var start = Math.min(sleep_start, hr_start);
    var end = Math.max(sleep_end, hr_end);
    var count = Math.ceil((end - start) / (24*60*60*1000));
    return {
        start,
        end,
        count
    }
}

var range = get_extents(data);

sleep_chart(data.sleep, range);
heartrate_chart(data.heartrate, range);
