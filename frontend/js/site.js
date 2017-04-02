'use strict';

var d3 = require('d3');
var esQuery = require('./es_query');
var drawCharts = require('./drawCharts');


// Draw the base chart
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;


var histogramData = esQuery.getYearCounts();
var yearChart = drawCharts.yearBarChart();

histogramData.then(function (data) {
    var selection = d3.select('#yearHisto');
    selection.call(yearChart, data);
// }).then(function (bars) {
//     bars.on('click', function (d) {
//         var res = esQuery.getTermsForYear(d.date).then(function(res) {
//             console.log('Significant terms are?', res)
//         });
//     });
});


