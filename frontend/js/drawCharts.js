/*
 Draw various charts on the page
 */
var d3 = require('d3');

function populateBars(chartSelector, data, shape) {
    // Initial version draws heavily from:
    //   https://bost.ocks.org/mike/bar/3/
    //   and d3 v4 update, https://bl.ocks.org/d3noob/bdf28027e0ce70bd132edc64f1dd7ea4

    // Options element for shape
    var height = shape.height;
    var width = shape.width;
    var margin = shape.margin;

    var x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var xAxis = d3.axisBottom()
        .scale(x)
        .tickFormat(function (d) {
            return d.getFullYear()
        });

    var yAxis = d3.axisLeft()
        .scale(y);

    var chart = d3.select(chartSelector)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    x.domain(data.map(function (d) {
        return d.date;
    }));

    y.domain([
        0,
        d3.max(data, function (d) {
            console.log(d);
            return d.count;
        }) + 1
    ]);

    chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    chart.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    var bars = chart.selectAll(".bars")
        .data(data)
        .enter()
        .append("g")
        .attr("class", "bars")
        .attr('nothing', function (d) {
            console.log(d)
        });

    bars.append("rect")
        .attr("class", "bar")
        .attr("x", function (d) {
            return x(d.date);
        })
        .attr("y", function (d) {
            return y(d.count);
        })
        .attr("height", function (d) {
            return height - y(d.count);
        })
        .attr("width", x.bandwidth());

    bars.append("text")
        .attr('class', 'label')
        .attr("x", function (d) {
            console.log('text');
            return x(d.date) + x.bandwidth() / 2;
        })
        .attr("y", function (d) {
            return y(d.count + 1);
        })
        .attr("dy", ".75em")
        .text(function (d) {
            return d.count;
        });
}

module.exports = {populateBars: populateBars};