document.addEventListener('DOMContentLoaded', function () {
    // Cargar gráfico de contactos por comuna
    fetch("/get-contact-stats")
        .then(response => response.json())
        .then(data => {
            const comunas = data.map(item => item.comuna);
            const totales = data.map(item => parseInt(item.total));

            Highcharts.chart('container', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Contactos por Comuna'
                },
                xAxis: {
                    categories: comunas,
                    title: {
                        text: 'Comuna'
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Cantidad de Contactos'
                    }
                },
                plotOptions: {
                    column: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                series: [{
                    name: 'Contactos',
                    data: totales,
                    color: '#4CAF50'
                }]
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('container').innerHTML = 
                `<div class="error">Error al cargar el gráfico de contactos: ${error.message}</div>`;
        });
});