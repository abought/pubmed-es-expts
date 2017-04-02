/*
 Define premade charts
 */
'use strict';

var d3 = require('d3');

// Three conventions and patterns used for these charts:
//   1. Margin convention: https://bl.ocks.org/mbostock/3019563
//   2. Reusable charts technique: https://bost.ocks.org/mike/chart/
//   3. Update pattern: https://bl.ocks.org/mbostock/3808218


function yearBarChart() {
    var margin = {top: 20, right: 30, bottom: 30, left: 40};
    var width = 960;
    var height = 300;

    var xScale = d3.scaleBand()
        .range([0, width])
        .padding(0.1);

    var yScale = d3.scaleLinear()
        .range([height, 0]);

    var xAxis = d3.axisBottom()
        .scale(xScale)
        .tickFormat(function (d) {
            return d.getFullYear()
        });

    var yAxis = d3.axisLeft()
        .scale(yScale);

    var update = function (data) {
        // TODO: handle binding to the selection associated with this chart?
        xScale.domain(data.map(function (d) {
            return d.date;
        }));

        yScale.domain([
            0,
            d3.max(data, function (d) {
                return d.count;
            }) + 1
        ]);
        return instance;
    };

    function instance(selection, data) {
        // TODO: Find a good blending of the update + reusable conventions
        // On first usage, create skeleton chart: use margin convention
        var chart = selection
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        update(data);

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
            .attr("class", "bars");

        bars.append("rect")
            .attr("class", "bar")
            .attr("x", function (d) {
                return xScale(d.date);
            })
            .attr("y", function (d) {
                return yScale(d.count);
            })
            .attr("height", function (d) {
                return height - yScale(d.count);
            })
            .attr("width", xScale.bandwidth());

        bars.append("text")
            .attr('class', 'label')
            .attr("x", function (d) {
                return xScale(d.date) + xScale.bandwidth() / 2;
            })
            .attr("y", function (d) {
                return yScale(d.count + 1);
            })
            .attr("dy", ".75em")
            .text(function (d) {
                return d.count;
            });
    }

    instance.width = function (value) {
        if (!arguments.length) return width;
        width = value;
        return instance;
    };
    instance.height = function (value) {
        if (!arguments.length) return height;
        height = value;
        return instance;
    };
    instance.margin = function (value) {
        if (!arguments.length) return margin;
        margin = value;
        return instance;
    };
    instance.update = update;

    return instance;
}

module.exports = {
    yearBarChart: yearBarChart
};