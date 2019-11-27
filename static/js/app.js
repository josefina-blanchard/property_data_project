
async function makePlot(){
    const defaultURL = `/zipcode/78515`;
    let data = await d3.json(defaultURL);
    data = [data];
    const layout = { margin: { t: 30, b: 100 } };
    Plotly.plot("bar", data, layout);
}

function updatePlotly(newdata) {
    Plotly.restyle("bar", "x", [newdata.x]);
    Plotly.restyle("bar", "y", [newdata.y]);
}

// Get new data whenever the dropdown selection changes
async function getData(zipCodeValue) {
    let data = await d3.json(`zipcode/${zipCodeValue}`);
    updatePlotly(data);
}

makePlot();