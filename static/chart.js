NIGHT_START = -6

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
}
function hours(x) {
    d = new Date(x.dateTime + 'Z');
    var o = d.getUTCDate() == (new Date(x.date)).getUTCDate() ? 0 : -24;
    return o + (
        d.getUTCHours() * 3600 +
        d.getUTCMinutes() * 60 +
        d.getUTCSeconds()
    ) / 3600;
}

var margin = {
    top: 20,
    left: 80,
    bottom: 80,
    right: 80
}
var WIDTH = document.body.clientWidth;
var HEIGHT = 1440 / 3 + margin.top + margin.bottom;

var sx = d3.scaleTime()
    .domain([new Date(2017, 0, 1), new Date(2018, 0, 1)])
    .range([0, WIDTH - margin.left - margin.right])
var sy = d3.scaleLinear()
    .domain([NIGHT_START, NIGHT_START + 24])
    .range([0, HEIGHT - margin.top - margin.bottom]);
var sh = d3.scaleLinear()
    .domain([0, 24])
    .range([0, HEIGHT - margin.top - margin.bottom]);

var BAR_W = sx(new Date(2017, 0, 2));

var ax = d3.axisBottom()
    .scale(sx)
    .tickSize(-(HEIGHT - margin.top - margin.bottom))
    .ticks(12);
var ay = d3.axisLeft()
    .scale(sy)
    .tickSize(-(WIDTH - margin.left - margin.right))
    .ticks(24)
    .tickFormat(function(d) {
      return ((d + 24) % 24).toLocaleString(undefined, {minimumIntegerDigits:2}) + 'h';
    });

var root = d3.select('#chart');
var svg = root.append('svg')
    .attr('width', WIDTH)
    .attr('height', HEIGHT);

var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

var gy = g.append('g')
    .call(ay);
var gx = g.append('g')
    .attr('transform', 'translate(0, ' + (HEIGHT - margin.top - margin.bottom) + ')')
    .call(ax);

gy.selectAll('g.tick line')
    .attr('stroke', '#505050')
    .attr('stroke-dasharray', function(d) {
        if (d % 3 == 0) {
            return '3,' + (BAR_W - 3);
        }
        return '0.5,' + (BAR_W - 0.5);
    });

gx.selectAll('g.tick line')
    .attr('stroke', '#505050')


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
// rects = rects.slice(0, 0);

var bars = g.selectAll('.bar').data(rects).enter();

bars.append('rect')
    .attr('class', 'bar')
    .attr('x', function(d) { return sx(date(d)); })
    .attr('y', function(d) { return sy(hours(d)); })
    .attr('height', function(d) { return sh(d.seconds / 3600); })
    .attr('width', BAR_W)
    .attr('fill', function(d) { return SLEEP_COLORS[d.level]; });
