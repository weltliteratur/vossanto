// set the dimensions and margins of the graph
const margin = {top: 40, right: 60, bottom: 80, left: 60};
const width = parseInt(d3.selectAll("#visualization_container").style("width")) - margin.left - margin.right;
const height = parseInt(d3.selectAll("#visualization_container").style("height")) - margin.top - margin.bottom;

const barMargin = {top: 20, right: 20, bottom: 30, left: 50};
const barWidth = parseInt(d3.selectAll("#bar_chart").style("width")) - barMargin.left - barMargin.right;
const barHeight = parseInt(d3.selectAll("#bar_chart").style("height")) - barMargin.top - barMargin.bottom;

// // append the svg object to the body of the page
const svg = d3.select("#visualization_container")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`)




var sliderWidthFactor = 0.8;
var sliderWidth = barWidth * sliderWidthFactor;

var slider = d3
    .sliderHorizontal()
    .min(1)
    .max(15)
    .step(1)
    .value(9)
    .width(sliderWidth)
    .displayValue(true);

var sliderGroup = d3.select('#slider')
    .append('svg')
    .attr('width', sliderWidth + barMargin.left + barMargin.right + 30)
    .append('g')
    .attr('transform', 'translate(' + (barMargin.left + 10) + ',30)')
    .call(slider);


// reduction choices
var buttonNames = ["pca_tsne", "pca", "tsne", "umap", "ivis"]

// reduction dropdown
// add the options to the selections
selections = d3.select("#selectButton")
    .selectAll('input')
    .data(buttonNames)
    .enter()
    .append('option')
    .text(function (d) {
        return d;
    }) // text showed in the menu
    .attr("value", function (d) {
        return d;
    }) // corresponding value returned by the button


// color scheme
var color = d3.scaleOrdinal(d3.schemeCategory10);

function visualize(data, infos, reduction) {

    // X axis
    var x = d3.scaleLinear()
        .range([0, width])
    // Y axis
    var y = d3.scaleLinear()
        .range([height, 0])

    // Using brush
    var brush = d3.brush().extent([[0, 0], [width, height]])
    var zoomBehavior = d3.zoom()
        .scaleExtent([0.5, 20]) // Allow zooming between 0.5x and 20x
        .on("zoom", zoomed);


    var idleTimeout, idleDelay = 750;

    // add barchart
    var bar_infos = infos.total_count
// Update the bar_chart SVG attributes
    var bar_chart = d3.select("#bar_chart")
        .append("svg")
        .attr("width", barWidth + barMargin.left + barMargin.right)
        .attr("height", barHeight + barMargin.top + barMargin.bottom)
        .append("g")
        .attr("transform", "translate(" + barMargin.left + "," + barMargin.top + ")");


// Add this after the bar_chart variable
    var selectedBarIndex = null;


    var bar_x = d3.scaleBand()
        .range([0, barWidth])
        .domain(bar_infos["8"])
        .padding(0.2);

    var bar_y = d3.scaleLinear()
        .domain([0, Math.max.apply(null, bar_infos["8"])])
        .range([barHeight, 0])
    var yAxis = bar_chart.append("g")
        .call(d3.axisLeft(bar_y));


    var scattertext = svg.append("g")
        .attr("id", "scatterplot")

// Add this after the scattertext variable
    var chartArea = svg.append("rect")
        .attr("class", "chart-area")
        .attr("width", width)
        .attr("height", height)
        .attr("fill", "transparent");

    // draw plot
    scattertext.selectAll(".dot")
        .data(data)
        .enter().append("text")
        .attr("class", "dot")
        .attr("x", function (d) {
            return x(d[reduction + "_x"]);
        })
        .attr("y", function (d) {
            return y(d[reduction + "_y"]);
        })
        .attr("size", function (d) {
            return d.count;
        })
        .text(function (d) {
            return d.label;
        })

        .style("font", function (d) {
            if (d.count < 3) {
                return "3px times"
            } else {
                return d.count + "px times"
            }
        })
        .style("fill", function (d) {
            return color(d[9])
        })


    // update plot depended on reduction algorithm
    update_reduction(reduction, 25)

    //update plot
    function update_reduction(reduction, k) {

        // update domains
        x.domain(d3.extent(data, function (d) {
            return d[reduction + "_x"];
        })).nice()

        y.domain(d3.extent(data, function (d) {
            return d[reduction + "_y"];
        })).nice()

        // "update" coords of phrases
        d3.selectAll(".dot")
            .data(data)
            .transition().duration(2000)
            .attr("x", function (d) {
                return x(d[reduction + "_x"]);
            })
            .attr("y", function (d) {
                return y(d[reduction + "_y"]);
            })
            .attr("size", function (d) {
                return d.count;
            })
            .text(function (d) {
                return d.label;
            })
            // .style("font", "5px times")
            .style("font", function (d) {
                if (d.count < 3) {
                    return "3px times"
                } else {
                    return d.count + "px times"
                }
            })


        d3.select(".brush")
            .call(brush);

        update_slider(slider.value())


    }

    // Function that change a color
    function changeColor(value) {
        scattertext.selectAll(".dot")
            .data(data).style("fill", function (d) {
            return color(d[value])
        });
    }

    function zoomed(event) {
        var transform = event.transform;
        scattertext.attr("transform", transform);
        scattertext.selectAll(".dot")
            .style("font", function (d) {
                var k = event.transform.k;
                var customScalingFactor = 0.01; // Adjust this value to control the text zoom speed
                if (d.count < 3) {
                    return (3 * (1 + customScalingFactor * (k - 1))) + "px times";
                } else {
                    return (d.count * (1 + customScalingFactor * (k - 1))) + "px times";
                }
            });
    }


    chartArea.call(zoomBehavior);



    // update when changing slider
    slider.on('onchange', update_slider)

    // updates colors, bar chart
    function update_slider(val) {
        changeColor(val)

        bar_x
            .domain(bar_infos[(val - 1).toString()])
            .padding(0.2);
        bar_y
            .domain([0, Math.max.apply(null, bar_infos[(val - 1).toString()])])
        yAxis
            .transition().duration(750)
            .call(d3.axisLeft(bar_y));

        bar_chart.append("g")
            .attr("transform", "translate(0," + barHeight + ")")
            .call(d3.axisBottom(bar_x).tickSize(0))
            .selectAll("text")
            .style("font", "0 px");

        var bars = bar_chart.selectAll(".bar")
            .data(bar_infos[(val - 1).toString()])


        bars
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("data-index", function (d, i) {
                return i;
            })
            .merge(bars)
            .transition()
            .duration(750)
            .attr("x", function (d, i) {
                return bar_x(d)
            })
            .attr("y", function (d) {
                return bar_y(d)
            })
            .attr("width", bar_x.bandwidth())
            .attr("height", function (d) {
                return barHeight - bar_y(d)
            })
            .attr("fill", function (d, i) {
                return color(i)
            })

        d3.selectAll(".bar").on("click", function (event, d) {
            var i = parseInt(d3.select(this).attr("data-index"));
            console.log(d)
            if (selectedBarIndex === i) { // If the clicked bar is already selected, deselect it
                d3.selectAll(".bar").style("opacity", 1.0);
                d3.selectAll(".dot").style("fill", function (d) {
                    return color(d[slider.value()]);
                });
                selectedBarIndex = null;
            } else { // If the clicked bar is not selected, select it
                selectedBarIndex = i;
                d3.selectAll(".bar").style("opacity", 0.2);
                d3.select(this).style("opacity", 1.0);
                d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.1)");
                d3.selectAll(".dot").filter(function (d) {
                    return d[slider.value()] === selectedBarIndex;
                }).style("fill", function (d) {
                    return color(d[slider.value()]);
                });
            }
            for (let t of d3.selectAll(".dot")) {

                color_p = color(t.__data__[slider.value()])
                // console.log(color_p)
                if (t.__data__[slider.value()] == i) {
                    t.style.fill = color_p
                }
            }

            var topic_infos = infos["topics"]
            html_text = "<ul>"

            for (let j = 0; j < topic_infos[slider.value() - 1][i].length - 5; j++) {
                html_text += "<li>" + topic_infos[slider.value() - 1][i][j]
            }

            d3.select("#topics")
                .html(html_text)
                .style("font", "20px times");
            // })
        });

        console.log("t", d3.selectAll(".bar"))
        bars.exit().remove()
    }


    selections.on("click", clickbutton)

    function clickbutton() {
        selections.style("background", "#e7e7e7");
        d3.select(this).style("background", "#B2D8D8");
        reduction_name = this.value// console.log(this.value)
        // bar_chart.selectAll("*").remove()
        update_reduction(reduction_name, 50)

        // Reset the opacity of all bars
        d3.selectAll(".bar").style("opacity", 1.0);

        // Reset the selectedBarIndex
        selectedBarIndex = null;

        // Reset the colors of the dots
        d3.selectAll(".dot").style("fill", function (d) {
            return color(d[slider.value()]);
        });
    }

}

// call function
Promise.all([d3.csv('./data/data.csv'), d3.json('./data/infos.json')]).then(([data, infos]) => {
    visualize(data, infos, "pca_tsne")

})



