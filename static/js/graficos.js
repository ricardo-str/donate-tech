document.addEventListener('DOMContentLoaded', function () {
    // Cargar gráfico de dispositivos
    fetch("/get-device-stats")
        .then(response => response.json())
        .then(data => {
            const tipos = data.map(item => item.tipo);
            const totales = data.map(item => parseInt(item.total));

            Highcharts.chart('deviceChart', {
                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Distribución de Dispositivos por Tipo'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                        }
                    }
                },
                series: [{
                    name: 'Dispositivos',
                    colorByPoint: true,
                    data: tipos.map((tipo, index) => ({
                        name: tipo,
                        y: totales[index]
                    }))
                }]
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('deviceChart').innerHTML = 
                `<div class="error">Error al cargar el gráfico de dispositivos: ${error.message}</div>`;
        });

    // Cargar gráfico de contactos por comuna
    fetch("/get-contact-stats")
        .then(response => response.json())
        .then(data => {
            const comunas = data.map(item => item.comuna);
            const totales = data.map(item => parseInt(item.total));

            Highcharts.chart('contactChart', {
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
            document.getElementById('contactChart').innerHTML = 
                `<div class="error">Error al cargar el gráfico de contactos: ${error.message}</div>`;
        });
});