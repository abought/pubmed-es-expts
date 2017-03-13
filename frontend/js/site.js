var d3 = require('d3');
var esQuery = require('./es_query');
var drawCharts = require('./drawCharts');


// Draw the base chart
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

esQuery.getYearCounts().then(function(data) {
    return drawCharts.populateBars('.chart', data, {
        width:width,
        height:height,
        margin: margin
    })
});
