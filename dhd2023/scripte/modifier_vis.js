// set the dimensions and margins of the graph
const margin = {top: 40, right: 60, bottom: 80, left: 60};
const width = parseInt(d3.selectAll("#visualization_container").style("width")) - margin.left - margin.right;
const height = parseInt(d3.selectAll("#visualization_container").style("height")) - margin.top - margin.bottom;

// // append the svg object to the body of the page
const svg = d3.select("#visualization_container")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`)


var slider = d3
    .sliderHorizontal()
    .min(1)
    .max(15)
    .step(1)
    .value(9)
    .width(250)
    .displayValue(true)

d3.select('#slider')
    .append('svg')
    .attr('width', 300)
    // .attr('height', 150)
    .append('g')
    .attr('transform', 'translate(30,30)')
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
    var idleTimeout, idleDelay = 750;

    // add barchart
    var bar_infos = infos.total_count
    var bar_chart = d3.select("#bar_chart")
        .append("g")
        .attr("transform", "translate(" + 50 + "," + 0 + ")");


    var bar_x = d3.scaleBand()
        .range([0, 400])
        .domain(bar_infos["8"])
        .padding(0.2);

    var bar_y = d3.scaleLinear()
        .domain([0, Math.max.apply(null, bar_infos["8"])])
        .range([200, 0])
    var yAxis = bar_chart.append("g")
        .call(d3.axisLeft(bar_y));


    var scattertext = svg.append("g")
        .attr("id", "scatterplot")


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
            if (d.count < 5) {
                return "5px times"
            } else {
                return d.count + "px times"
            }
        })
        .style("fill", function (d) {
            return color(d[9])
        })

    scattertext.append("g")
        .attr("class", "brush")


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
                if (d.count < 5) {
                    return "5px times"
                } else {
                    return d.count + "px times"
                }
            })


        d3.select(".brush")
            .call(brush);

        update_slider(slider.value())

        function brushended(event, d) {
            var s = event.selection;
            d3.selectAll(".dot")
                .attr('transform', event.transform);
            if (s === null) {
                if (!idleTimeout) return idleTimeout = setTimeout(idled, idleDelay);
                x.domain(d3.extent(data, function (d) {
                    return d[reduction + "_x"];
                })).nice();
                y.domain(d3.extent(data, function (d) {
                    return d[reduction + "_y"];
                })).nice();
            } else {
                x.domain([s[0][0], s[1][0]].map(x.invert, x));
                y.domain([s[1][1], s[0][1]].map(y.invert, y));
                d3.select(".brush").call(brush.move, null);
            }
            zoom(s);
        }

        brush.on("end", brushended);

        function idled() {
            idleTimeout = null;
        }

        // zooms in when brushed
        function zoom(s) {
            if (s == null) {
                d3.selectAll(".dot").transition().duration(1500)
                    .attr("x", function (d) {
                        return x(d[reduction + "_x"]);
                    })
                    .attr("y", function (d) {
                        return y(d[reduction + "_y"]);
                    })
                    .style("font", function (d) {
                        if (d.count < 5) {
                            return "5px times"
                        } else {
                            return d.count + "px times"
                        }
                    });
            } else {
                // change text size depended on the chosen brush
                var brush_size = Math.abs(s[1][0] - s[0][0]) * Math.abs(s[1][1] - s[0][1])
                var alpha = Math.sqrt((2000 * 1000) / brush_size)
                scattertext.selectAll("text").transition().duration(1500)
                    .attr("x", function (d) {
                        return x(d[reduction + "_x"]);
                    })
                    .attr("y", function (d) {
                        return y(d[reduction + "_y"]);
                    })
                    .style("font", function (d) {
                        if (d.count < 5) {
                            return alpha * 5 + "px times"
                        } else {
                            return alpha * d.count + "px times"
                        }
                    })
            }
        }
    }

    // Function that change a color
    function changeColor(value) {
        scattertext.selectAll(".dot")
            .data(data).style("fill", function (d) {
            return color(d[value])
        });
    }


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
            .attr("transform", "translate(0," + 200 + ")")
            .call(d3.axisBottom(bar_x).tickSize(0))
            .selectAll("text")
            .style("font", "0 px")


        var bars = bar_chart.selectAll(".bar")
            .data(bar_infos[(val - 1).toString()])


        bars
            .enter()
            .append("rect")
            .attr("class", "bar")
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
                return 200 - bar_y(d)
            })
            .attr("fill", function (d, i) {
                return color(i)
            })

        d3.selectAll(".bar").on("click", function (d, i) {
            i = parseInt(d3.select(this).attr("x") / (400 / slider.value()))
            d3.selectAll(".bar")
                .style("opacity", 0.2);
            d3.select(this)
                .style("opacity", 1.0);
            // "update" coords of phrases
            d3.selectAll(".dot")
                .data(data)
                .style("fill", "rgb(0,0,0,0.1)")
            console.log(i)
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
                .style("font", "10px times");
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
    }

    console.log("red", reduction)
}

// call function
Promise.all([d3.csv('./data/data.csv'), d3.json('./data/infos.json')]).then(([data, infos]) => {
    visualize(data, infos, "pca_tsne")
})



