function doGET(path, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                callback(xhr.responseText);
            } else {
                callback(null);
            }
        }
    };
    xhr.open("GET", path);
    xhr.send();
}

data = '';
function handleCSVFileData(fileData) {
    if (!fileData) {
        console.log('Error!');
        return;
    }
    data = Object.assign(new Map(d3.csvParse(fileData, ({id, rate}) => [id, +rate])), {title: "Unemployment rate (%)"});
    doGET('https://raw.githubusercontent.com/Lotunnnnny/Remote-Resources/master/counties-albers-10m.json', handleJSONFileData);
}

us = '';
function handleJSONFileData(fileData) {
    if (!fileData) {
        console.log('Error!');
        return;
    }

    us = JSON.parse(fileData);

    color = d3.scaleQuantize([1, 10], d3.schemeBlues[9])

    path = d3.geoPath()

    format = d => `${d}%`

    states = new Map(us.objects.states.geometries.map(d => [d.id, d.properties]))

    const svg = d3.select('body').append("svg")
        .attr("viewBox", [0, 0, 975, 610]);

    svg.append("g")
        .attr("transform", "translate(610,20)")
        .append(() => legend({color, title: data.title, width: 260}));

    svg.append("g")
        .selectAll("path")
        .data(topojson.feature(us, us.objects.counties).features)
        .join("path")
        .attr("fill", d => color(data.get(d.id)))
        .attr("d", path)
        .append("title")
        .text(d => `${d.properties.name}, ${states.get(d.id.slice(0, 2)).name}
        ${format(data.get(d.id))}`);

    svg.append("path")
        .datum(topojson.mesh(us, us.objects.states, (a, b) => a !== b))
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-linejoin", "round")
        .attr("d", path);
}

// Do the request
doGET('https://raw.githubusercontent.com/Lotunnnnny/Remote-Resources/master/unemployment-x.csv', handleCSVFileData);
