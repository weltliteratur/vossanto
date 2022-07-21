// set the dimensions and margins of the graph
const margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 2000 - margin.left - margin.right,
    height = 1500 - margin.top - margin.bottom;

// // append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`)

var slider = d3
    .sliderHorizontal()
    .min(1)
    .max(14)
    .step(1)
    .value(10)
    .width(600)
    .displayValue(true)
// .on('onchange', function (val) {
//     d3.select('#value').text(val);
// });

d3.select('#slider')
    .append('svg')
    .attr('width', 700)
    .attr('height', 150)
    .append('g')
    .attr('transform', 'translate(30,30)')
    .call(slider);

d3.select('#legend')
    .attr('width', 600)
    .attr('height', 150)
    .append('g')
    .attr('transform', 'translate(30,30)')

// color scheme
var color = d3.scaleOrdinal(d3.schemeCategory10);

// //Read the data
d3.csv("./data/kmeans_pca_tsne.csv").then(function (data) {

    // transform datatype of x and y coordinates to numeric
    data.forEach(function (d) {
        d.x = +d.x;
    });
    data.forEach(function (d) {
        d.y = +d.y;
    });

    // Add X axis
    var x = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d.x;
        }))
        .range([0, width]);

    // Add Y axis
    var y = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d.y;
        }))
        .range([height, 0]);
    // svg.append("g")
    //     .attr("transform", `translate($0,{width})`)
    //     .call(d3.axisLeft(y));

    var brush = d3.brush().extent([[0, 0], [width, height]]).on("end", brushended),
        idleTimeout,
        idleDelay = 350;


    x.domain(d3.extent(data, function (d) {
        return d.x;
    })).nice();
    y.domain(d3.extent(data, function (d) {
        return d.y;
    })).nice();


    var scattertext = svg.append("g")
        .attr("id", "scatterplot")
        .attr("my_dataviz-path", "url(#my_dataviz)");


    // "draw" labels
    var scatter = scattertext.selectAll(".dot")
        .data(data)
        .enter().append("text")
        .attr("class", "dot")
        .attr("x", function (d) {
            return x(d.x);
        })
        .attr("y", function (d) {
            return y(d.y);
        })
        .text(function (d) {
            return d.label;
        })
        .style("font", "5px times")
        .style("fill", function (d) {
            // console.log(d[9])
            return color(d[9])
        })


    var legend = d3.select("#legend")
    keys = Array.from({length: slider.value()}, (x, i) => i)
    legend.selectAll("mydots")
        .data(keys)
        .enter()
        .append("circle")
        .attr("cx", function (d, i) {
            return 30 + i * 38
        })
        .attr("cy", 100) // 100 is where the first dot appears. 25 is the distance between dots
        .attr("r", 7)
        .style("fill", function (d, i) {
            return color(i)
        })
        .on("click", function (d, i) {
            console.log(d)
            console.log(i)
            d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.4)")
            d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.4)")
            for (let t of d3.selectAll(".dot")) {
                // console.log(t.__data__[slider.value()] == i + 1, color(t.__data__[slider.value()]))
                color_p = color(t.__data__[slider.value()] )
                if (t.__data__[slider.value()] == i ) {
                    console.log("test")
                    t.style.fill = color_p
                }
                console.log(typeof color_p)
                //     console.log(slider.value() == i + 1)
                //     t.style.fill =  color_p
            }
        })

    // call brush on scattertext
    scattertext.append("g")
        .attr("class", "brush")
        .call(brush);


    function brushended(event, d) {
        var s = event.selection;
        if (s === null) {
            if (!idleTimeout) return idleTimeout = setTimeout(idled, idleDelay);
            x.domain(d3.extent(data, function (d) {
                return d.x;
            })).nice();
            y.domain(d3.extent(data, function (d) {
                return d.y;
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
            scattertext.selectAll("text")
                .attr("x", function (d) {
                    return x(d.x);
                })
                .attr("y", function (d) {
                    return y(d.y);
                }).style("font", "5px times");
        } else {
            scattertext.selectAll("text").transition(t)
                .attr("x", function (d) {
                    return x(d.x);
                })
                .attr("y", function (d) {
                    return y(d.y);
                })
                .style("font", "15px times");
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
            .attr("r", 7)
            .style("fill", function (d, i) {
                console.log(i)
                return color(i)
            })
            .on("click", function (d, i) {
                console.log(d)
                console.log(i)
                d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.4)")
                d3.selectAll(".dot").style("fill", "rgb(0,0,0,0.4)")
                for (let t of d3.selectAll(".dot")) {
                    // console.log(t.__data__[slider.value()] == i + 1, color(t.__data__[slider.value()]))
                    color_p = color(t.__data__[slider.value()])
                    if (t.__data__[slider.value()] == i) {
                        console.log("test")
                        t.style.fill = color_p
                    }
                    console.log(typeof color_p)
                    //     console.log(slider.value() == i + 1)
                    //     t.style.fill =  color_p
                }
            })
    });


})




