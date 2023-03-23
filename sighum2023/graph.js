// based on https://bl.ocks.org/mapio/53fed7d84cd1812d6a6639ed7aa83868

const margin = {top: 20, right: 25, bottom: 60, left: 25},
    width = d3.select("#visualization_container").node().clientWidth - margin.left - margin.right,
    height = d3.select("#visualization_container").node().clientHeight - margin.top - margin.bottom;

let color = d3.scaleOrdinal(d3.schemeCategory10);


Promise.all([
    d3.json("data/graph.json"),
    d3.json("data/node_infos.json"),
    d3.json("data/paths.json"),
    d3.json("data/image_urls.json")
]).then(([graph, node_infos, paths, image_urls]) => {

    let text_container = d3.select(".sentences");


    const x = d3.scaleLinear()
        .domain([d3.min(graph.nodes, function (d) {
            return d.x;
        }), d3.max(graph.nodes, function (d) {
            return d.x;
        })])
        .range([0, width])
        .nice();

    const y = d3.scaleLinear()
        .domain([d3.min(graph.nodes, function (d) {
            return d.y;
        }), d3.max(graph.nodes, function (d) {
            return d.y;
        })])
        .range([0, height])
        .nice();

    let label = {
        'nodes': [],
        'links': []
    };
    let edges = [];

    graph.links.forEach(function (d, i) {

        edges.push(d.source.toString() + "-" + d.target.toString())
    })


    graph.nodes.forEach(function (d, i) {
        label.nodes.push({node: d});
        label.nodes.push({node: d});
        label.links.push({
            source: i * 2,
            target: i * 2 + 1
        });
    });


    let adjlist = [];
    let adjlist2 = [];

    graph.links.forEach(function (d) {
        adjlist[d.source.index + "-" + d.target.index] = true;
        adjlist[d.target.index + "-" + d.source.index] = true;
    });

    function neigh(a, b) {
        return a == b || adjlist[a + "-" + b];
    }

    graph.links.forEach(function (d) {
        adjlist2[d.source.id + "-" + d.target.id] = true;
        adjlist2[d.target.id + "-" + d.source.id] = true;
    });

    function neigh2(a, b) {
        return a == b || adjlist2[a + "-" + b];
    }

    var svg = d3.select("#visualization_container")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)


    let container = svg.append("g")

    svg.append('defs').append('marker')
        .attr("id", 'arrowhead')
        .attr('refX', 73)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 4)
        .attr('markerHeight', 4)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke', 'none');


    // svg.call(
    //     d3.zoom()
    //         .scaleExtent([.1, 8])
    //         .on("zoom", function () {
    //             container.attr("transform", d3.event.transform);
    //         })
    // );

    const zoom = d3.zoom()
        .scaleExtent([.1, 10])
        .on("zoom", function () {
            container.attr("transform", d3.event.transform);
        });

    svg.call(zoom);

// Add zoom in and zoom out event listeners
    d3.select("#zoom_in").on("click", function () {
        zoom.scaleBy(svg.transition().duration(750), 1.3);
    });

    d3.select("#zoom_out").on("click", function () {
        zoom.scaleBy(svg.transition().duration(750), 1 / 1.3);
    });

    const link = container.append("g").attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter()
        .append("line")
        .attr("x1", function (d) {
            return x(graph.nodes[d.source]["x"])
        })
        .attr("x2", function (d) {
            return x(graph.nodes[d.target]["x"])
        })
        .attr("y1", function (d) {
            return y(graph.nodes[d.source]["y"])
        })
        .attr("y2", function (d) {
            return y(graph.nodes[d.target]["y"])
        })
        .attr("stroke", "#aaa")
        .attr("stroke-width", "0.5px")
    // .attr('marker-end', 'url(#arrowhead)');

    const node = container.append("g").attr("class", "nodes")
        .selectAll("g")
        .data(graph.nodes)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return x(d.x);
        })
        .attr("cy", function (d) {
            return y(d.y);
        })
        .attr("id", function (d) {
            return d.id
        })
        .attr("r", function (d) {
            return d.size / 3 + 1
        })
        .style("stroke", "#aaa")
        .style("fill", "white")
        .style("stroke-width", "0.5px")
        .style("cursor", "pointer")


    node.on("click", focus)


    const labelNode = container.append("g").attr("class", "labelNodes")
        .selectAll("g")
        .data(label.nodes)
        .enter()
        .append("text")
        .attr("x", function (d) {
            return x(d.node.x) + 1.5;
        })
        .attr("y", function (d) {
            return y(d.node.y) - 0.5;
        })
        .html(function (d, i) {
            return i % 2 == 0 ? "" : node_infos[d.node.id]["label"];
        })
        .style("fill", "#aaa")
        .style("font-family", "Roboto")
        .style("font-size", function (d) {
            return Math.max(d.node.size, 3).toString() + "px"
        })
        .style("cursor", "pointer")

    labelNode.on("click", function (d) {
        return focus(d.node)
    });
    //
    node.on("click", focus);


    svg.on("click", function () {
        // Check if the event target is the SVG container itself
        if (d3.event.target === this) {
            unfocus();
        }
    });

    let firstClicked = false;
    let highlightNodeInfos = [];

    text_container.select("#source-button")
        .on("click", function () {
            if (firstClicked) {
                html_text = generateSrcHtml(highlightNodeInfos[0], highlightNodeInfos[1], highlightNodeInfos[2])
                d3.select("#text").html(html_text);
            } else {
                d3.select("#text").text("Please click on a node in the graph first.");
            }
            console.log(this)
            d3.select(this).style("background-color", "#800000")
                .style("color", "white");
            d3.select("#target-button").style("background-color", "lightgrey")
                .style("color", "black");
        });

    text_container.select("#target-button")
        .on("click", function () {
            if (firstClicked) {
                html_text = generateTrgHtml(highlightNodeInfos[0], highlightNodeInfos[1], highlightNodeInfos[2])
                d3.select("#text").html(html_text);
            } else {
                d3.select("#text").text("Please click on a node in the graph first.");
            }
            d3.select(this).style("background-color", "#808000")
                .style("color", "white");
            d3.select("#source-button").style("background-color", "lightgrey")
                .style("color", "black");
        });


    function unfocus() {
        node.style("stroke", "#aaa")
            .style("fill", "white")
            .style("stroke-width", "0.5px")
            .style("opacity", 1);
        labelNode
            .style("fill", "#aaa")
            .style("font-size", function (d) {
                return Math.max(d.node.size, 3).toString() + "px"
            })
            .style("opacity", function (o, i) {
                return i % 2 == 0 ? 0 : 1;
            });
        link.style("opacity", "1")
            .style("stroke", "#aaa")
            .style("stroke-width", "0.5px");
        d3.select("#text").text("");
        d3.select("#label").text("");
        d3.select("#image_container").text("");
        d3.select("#target-button").style("background-color", "lightgrey")
            .style("color", "black");
        d3.select("#source-button").style("background-color", "lightgrey")
            .style("color", "black");
    }

    function focus(d) {
        d3.select("#text").text("");
        var node_id = d.id
        var node_name = node_infos[node_id]["label"]
        var node_index = d.index;
        var connected = paths[node_index]
        firstClicked = true;
        highlightNodeInfos = [node_id, node_name, node_infos[node_id]]
        updateNodeStyle(node, node_id, connected);
        updateLabelNodeStyle(node_index, connected);
        updateLinkStyle(node_index, connected, edges)

        d3.select("#target-button").style("background-color", "lightgrey")
            .style("color", "black");
        d3.select("#source-button").style("background-color", "lightgrey")
            .style("color", "black");
        d3.select("#label").html(
            `<h2><a href=https://www.wikidata.org/wiki/${node_id}>${node_name}</a></h2>`
        )
        // wikidata image by url
        let image = "";
        let meta = "";
        if (image_urls.hasOwnProperty(node_id)) {
            image += "<a href='https://commons.wikimedia.org/wiki/File:" + image_urls[node_id]["sourceImId"] + "'>" +
                "<img src='https://upload.wikimedia.org/wikipedia/commons/" + image_urls[node_id]["sourceImThumb"] + "'/></a><br>";
            meta += "<a href='https://commons.wikimedia.org/wiki/File:" + image_urls[node_id]["sourceImId"] + "'>Wikimedia Commons</a>";

            meta += ", license: " + image_urls[node_id]["permissions"]
            d3.select("#image_container")
                .html(image + meta);
        } else {
            d3.select("#image_container")
                .html("No image available.");
        }
    }


    function updateNodeStyle(node, node_id, connected) {
        node.style("stroke", function (o) {
            if (o.id == node_id) {
                return "#f58231";
            } else if (connected[0].includes(o.index) && connected[1].includes(o.index)) {
                return "#703cd8";
            } else if (connected[0].includes(o.index)) {
                return "#EC5552";
            } else if (connected[1].includes(o.index)) {
                return "#069869";
            } else {
                return "#555";
            }
        });

        node.style("opacity", function (o) {
            if ((o.id == node_id) || (connected[0].includes(o.index) || connected[1].includes(o.index))) {
                return 0.6;
            } else {
                return 0.3;
            }
        });
    }

    function updateLabelNodeStyle(node_index, connected) {
        labelNode.style("fill", function (o) {
            if (o.node.index == node_index) {
                return "#f58231";
            } else if (connected[0].includes(o.node.index) && connected[1].includes(o.node.index)) {
                return "#9763db";
            } else if (connected[0].includes(o.node.index)) {
                return "#f36e64";
            } else if (connected[1].includes(o.node.index)) {
                return "#069869";
            } else {
                return "#555";
            }
        })
            .style("opacity", function (o, i) {
                if ((o.node.index == node_index) || (connected[0].includes(o.node.index) || connected[1].includes(o.node.index))) {
                    return i % 2 == 0 ? 0 : 1;
                } else {
                    return i % 2 == 0 ? 0 : 0.2;
                }
            })
            .style("font-size", function (o, i) {
                if ((o.node.index == node_index) || (connected[0].includes(o.node.index) || connected[1].includes(o.node.index))) {
                    return i % 2 == 0 ? 0 : 1.2 * Math.max(o.node.size, 3).toString() + "px";
                } else {
                    return i % 2 == 0 ? 0 : 1 * Math.max(o.node.size, 3).toString() + "px";
                }
            })
        // return 1.5 * Math.max(d.node.size, 3).toString() + "px"
        // })
    }

    function updateLinkStyle(node_index, connected, edges) {
        link.style("opacity", function (o) {
            if ((o.source == node_index || o.target == node_index) ||
                ((connected[0].includes(o.source) && connected[0].includes(o.target))
                    || (connected[1].includes(o.source) && connected[1].includes(o.target)))) {
                return 1;
            } else {
                return 0.3;
            }
        })
        link.style("stroke", function (o) {
                //neighbors
                if (((edges.includes(o.source.toString() + "-" + o.target.toString()) && edges.includes(o.target.toString() + "-" + o.source.toString()))
                        && (o.target == node_index || o.source == node_index))
                    ||
                    //non-neighbors
                    ((edges.includes(o.source.toString() + "-" + o.target.toString()) && edges.includes(o.target.toString() + "-" + o.source.toString()))
                        && (connected[0].includes(o.target) || connected[1].includes(o.target))
                        && (connected[0].includes(o.source) || connected[1].includes(o.source))
                    )) {
                    return "#9763db";
                } else if ((connected[0].includes(o.source) && connected[0].includes(o.target))
                    || (o.target == node_index)) {
                    return "#f36e64";
                } else if ((connected[1].includes(o.source) && connected[1].includes(o.target))
                    || (o.source == node_index)) {
                    return "#069869";
                } else {
                    return "#555";
                }
            }
        )
            .style("stroke-width", function (o) {
                if ((o.source == node_index || o.target == node_index) ||
                    ((connected[0].includes(o.source) && connected[0].includes(o.target))
                        || (connected[1].includes(o.source) && connected[1].includes(o.target)))) {
                    return 1.2;
                } else {
                    return 1;
                }
            })
            .style("opacity", 0.2)
    }

    function generateSrcHtml(node_id, node_name, node_infos) {

        const listItems = node_infos["VA_src_sents"].map(d => {
            const [prefix, modifier, suffix] = d[0].split("/");
            let sent = `${prefix}<em>${modifier}</em>${suffix}`;
            if (sent.includes("|")) {
                const [prefix, target, suffix] = sent.split("|");
                sent = `${prefix}<a class='trg-link' href='https://www.wikidata.org/wiki/${d[3]}'>${target}</a>${suffix}`;
            }
            const [prefix2, emphasis, suffix2] = sent.split("*");
            sent = `<li>${prefix2}<a class='current-link' href='https://www.wikidata.org/wiki/${node_id}'>${emphasis}</a>${suffix2}
      (<a href='http://query.nytimes.com/gst/fullpage.html?res=${d[1]}'>NYT ${d[2]}</a>)</li>`;
            return sent;
        });
        return `
    
    <ul>
      ${listItems.join("")}
    </ul>
  `;
    }

    function generateTrgHtml(node_id, node_name, node_infos) {
        const listItems = node_infos["VA_trg_sents"].map(d => {
            const [prefix, modifier, suffix] = d[0].split("/");
            let sent = `${prefix}<em>${modifier}</em>${suffix}`;
            if (sent.includes("|")) {
                const [prefix, target, suffix] = sent.split("|");
                sent = `${prefix}<a class='current-link' href='https://www.wikidata.org/wiki/${node_id}'>${target}</a>${suffix}`;
            }
            const [prefix2, emphasis, suffix2] = sent.split("*");
            sent = `<li>${prefix2}<a class='src-link' href='https://www.wikidata.org/wiki/${d[3]}'>${emphasis}</a>${suffix2}
      (<a href='http://query.nytimes.com/gst/fullpage.html?res=${d[1]}'>NYT ${d[2]}</a>)</li>`;
            return sent;
        });
        return `
    <ul>
      ${listItems.join("")}
    </ul>
  `;
    }

})
;
