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
        console.log('CSV Error!');
        return;
    }
    data = Object.assign(new Map(d3.csvParse(fileData, ({id, num}) => [id, +num])), {title: "Crime number:"});
    doGET('https://raw.githubusercontent.com/Lotunnnnny/Remote-Resources/master/London_Borough_Excluding_MHW.json', handleJSONFileData);
}

london = '';
function handleJSONFileData(fileData) {
    if (!fileData) {
        console.log('JSON Error!');
        return;
    }

    london = JSON.parse(fileData);

    color = d3.scaleQuantize([1, 10], d3.schemeBlues[9])

    geojson = topojson.feature(london, london.objects.London_Borough_Excluding_MHW);
    projection = d3.geoIdentity()
        .reflectY(true)
        .fitSize([550, 350],geojson);
    path = d3.geoPath().projection(projection);

    format = d => `${d}`

    boroughs = new Map(london.objects.London_Borough_Excluding_MHW.geometries.map(d => [d.id, d.name]))

    const svg = d3.select('body').append("svg")
        .attr("viewBox", [0, 0, 975, 610]);

    svg.append("g")
        .attr("transform", "translate(10,20)")
        .append(() => legend({color, title: data.title, width: 260}));

    svg.append("g")
        .selectAll("path")
        .data(geojson.features)
        .join("path")
        .attr("fill", d => color(data.get(d.id)))
        .attr("d", path)
        .attr("transform", "translate(0, 80)")
        .append("title")
        .text(d => `${boroughs.get(d.id)}
        ${format(data.get(d.id))}`);

    svg.append("path")
        .datum(topojson.mesh(london, london.objects.London_Borough_Excluding_MHW, (a, b) => a !== b))
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-linejoin", "round")
        .attr("transform", "translate(0, 80)")
        .attr("d", path);
}

// Do the request
doGET('https://raw.githubusercontent.com/Lotunnnnny/Remote-Resources/master/Other Crime', handleCSVFileData);