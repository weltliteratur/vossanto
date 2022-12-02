// set the dimensions and margins of the graph
const margin = {top: 10, right: 30, bottom: 30, left: 60}, width = 2000 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;

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
    .width(600)
    .displayValue(true)


// .on('onchange', function (val) {
//     d3.select('#value').text(val);
// });

var buttonNames = ["pca", "pca_tsne", "tsne", "umap", "ivis"]

buttons = d3.select("#reduction_container")
    .selectAll("input")
    .data(buttonNames)
    .enter()
    .append("input")
    .attr("type", "button")
    .attr("class", "button")
    .attr("value", function (d) {
        return d;
    })


d3.select('#slider')
    .append('svg')
    .attr('width', 700)
    // .attr('height', 150)
    .append('g')
    .attr('transform', 'translate(30,30)')
    .call(slider);

d3.select('#legend')
    .attr('width', 600)
    // .attr('height', 150)
    .append('g')
    .attr('transform', 'translate(30,30)')

// color scheme
var color = d3.scaleOrdinal(d3.schemeCategory10);


function visualize(data, infos, reduction) {
    // transform datatype of x and y coordinates to numeric
    data.forEach(function (d) {
        d[reduction + "_x"] = +d[reduction + "_x"];
    });
    data.forEach(function (d) {
        d[reduction + "_y"] = +d[reduction + "_y"];
    });

    // Add X axis
    var x = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d[reduction + "_x"];
        }))
        .range([0, width]);

    // Add Y axis
    var y = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d[reduction + "_y"];
        }))
        .range([height, 0]);

    var brush = d3.brush().extent([[0, 0], [width, height]]).on("end", brushended), idleTimeout, idleDelay = 350;


    x.domain(d3.extent(data, function (d) {
        return d[reduction + "_x"];
    })).nice();
    y.domain(d3.extent(data, function (d) {
        return d[reduction + "_y"];
    })).nice();


    var scattertext = svg.append("g")
        .attr("id", "scatterplot")
        .attr("visualization_container-path", "url(#visualization_container)");


    // "draw" labels
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
        // .style("font", "5px times")
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

    bar_infos = infos.total_count
    var bar_chart = d3.select("#bar_chart")
        // .append("svg")
        // .attr("width", 600)
        // .attr("height", 400)
        .append("g")
        .attr("transform",
            "translate(" + 50 + "," + 0 + ")");

    var bar_x = d3.scaleBand()
        .range([0, 400])
        .domain(bar_infos["8"])
        .padding(0.2);
    var xAxis = bar_chart.append("g")
        .attr("transform", "translate(0," + 200 + ")")
        .call(d3.axisBottom(bar_x).tickSize(0))
        .selectAll("text")
        .style("font", "0 px")


    // Add Y axis
    var bar_y = d3.scaleLinear()
        .domain([0, Math.max.apply(null, bar_infos["8"])])
        .range([200, 0])


    var yAxis = bar_chart.append("g")
        .call(d3.axisLeft(bar_y));
//
// Bars


    var bars = bar_chart.selectAll("rect")
        .data(bar_infos["8"])

    bars
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function (d) {
            return bar_x(d);
        })
        .attr("y", function (d) {
            return bar_y(d);
        })
        .attr("width", bar_x.bandwidth())
        .attr("height", function (d) {
            return 200 - bar_y(d);
        })
        .attr("fill", function (d, i) {
            return color(i)
        })

    bars.exit().remove()


    var legend = d3.select("#legend")

    keys = Array.from({length: slider.value()}, (x, i) => i)
    legend.selectAll("mydots")
        .data(keys)
        .enter()
        .append("circle")
        .attr("cx", function (d, i) {
            return 30 + i * 38
        })
        .attr("cy", 100) // 100 is where the first dot appears.
        .attr("r", 15)
        .style("fill", function (d, i) {
            return color(i)
        })

        .on("click", function (d, i) {
            d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.1)")
            for (let t of d3.selectAll(".dot")) {
                slider_value = Math.round(slider.value())
                color_p = color(t.__data__[slider_value])
                if (t.__data__[slider_value] == i) {
                    t.style.fill = color_p
                }
            }
        })

    // call brush on scattertext
    scattertext.append("g")
        .attr("class", "brush")
        .call(brush);


    function brushended(event, d) {
        var s = event.selection;

        scattertext.selectAll("text")
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
            scattertext.select(".brush").call(brush.move, null);
        }
        zoom(s);
    }

    function idled() {
        idleTimeout = null;
    }

    function zoom(s) {


        var t = scattertext.transition().duration(750);
        if (s == null) {
            scattertext.selectAll("text").transition(t)
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
            scattertext.selectAll("text").transition(t)
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

    // Function that change a color
    function changeColor(value) {
        scattertext.selectAll(".dot")
            .data(data).style("fill", function (d) {
            return color(d[value])
        });
    }


    // change color when changing slider
    slider.on('onchange', function (val, d) {

        bar_x
            .domain(bar_infos[(val-1).toString()])
            .padding(0.2)
        ;

        bar_chart.append("g")
            .attr("transform", "translate(0," + 200 + ")")
            .call(d3.axisBottom(bar_x).tickSize(0))
            .selectAll("text")
            .style("font", "0 px")
        // .attr("transform", "translate(-10,0)rotate(-45)")
        // .style("text-anchor", "end");
//
// Add Y axis
        bar_y
            .domain([0, Math.max.apply(null, bar_infos[(val-1).toString()])])
        yAxis
            .transition().duration(750)
            .call(d3.axisLeft(bar_y));

// Bars


        var bars = bar_chart.selectAll("rect")
            .data(bar_infos[(val-1).toString()])

        bars
            .enter()
            .append("rect")
            .merge(bars)
            .transition() // and apply changes to all of them
            .duration(750)
            .attr("class", "bar")
            .attr("x", function (d) {
                return bar_x(d);
            })
            .attr("y", function (d) {
                return bar_y(d);
            })
            .attr("width", bar_x.bandwidth())
            .attr("height", function (d) {
                return 200 - bar_y(d);
            })
            .attr("fill", function (d, i) {
                return color(i)
            })

        bars.exit().remove()

        // d3.select('#value').text(val);
        changeColor(val)
        legend.selectAll("circle").remove();
        legend.selectAll("mydots")
            .data(Array.from({length: val}, (x, i) => i))
            .enter()
            .append("circle")
            .attr("cx", function (d, i) {
                return 30 + i * 35
            })
            .attr("cy", 100) // 100 is where the first dot appears. 25 is the distance between dots
            .attr("r", 15)
            .style("fill", function (d, i) {
                return color(i)
            })
            //todo: eigentlich wäre es cooler, auf den barchart zu klicken bzw beides?
            .on("click", function (d, i) {
                d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.1)")
                for (let t of d3.selectAll(".dot")) {

                    color_p = color(t.__data__[slider.value()])
                    if (t.__data__[slider.value()] == i) {
                        t.style.fill = color_p
                    }
                }
            })

    });

    clicked = buttons.on("click", function () {
        buttons.style("background", "#e7e7e7");
        d3.select(this).style("background", "#B2D8D8");
        reduction_name = this.value// console.log(this.value)
        // todo:mit transition().duration(1000) o.ä. punkte verschieben lassen, sieht halt cooler aus.
        //  bräcuhte aber eine andere architektur: update coordinates instead of drawing new
        svg.selectAll("*").remove()
        bar_chart.selectAll("*").remove()
        Promise.all([
            d3.csv('../data/data.csv'),
            d3.json('../data/infos.json')
        ]).then(([data, infos]) => {
                visualize(data, infos, "pca_tsne")
            }
        )
        // d3.csv("./data/data.csv").then(function (data) {
        //     visualize(data, reduction_name)
        // })
    })

}

Promise.all([
    d3.csv('../data/data.csv'),
    d3.json('../data/infos.json')
]).then(([data, infos]) => {
        visualize(data, infos, "pca_tsne")
    }
)
// d3.csv("./data/data.csv").then(function (data) {
//     visualize(data, "pca_tsne")
// })




