let graphCanvas = document.getElementById('graphCanvas');
let graphInstance = null;

function loadGraph(graphType) {
    fetch(`/get_graph/${graphType}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            renderGraph(data.title, data.data);
        });
}

function renderGraph(title, data) {
    if (graphInstance) {
        graphInstance.destroy();
    }

    graphInstance = new Chart(graphCanvas, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr'],
            datasets: [{
                label: title,
                data: data,
                backgroundColor: 'rgba(183, 0, 0, 0.5)',
                borderColor: 'rgba(183, 0, 0, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}
