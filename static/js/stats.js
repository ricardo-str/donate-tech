document.addEventListener('DOMContentLoaded', function () {
    console.log('Script iniciado'); // Para debugging

    fetch("/get-stats-data")
        .then(response => {
            console.log('Respuesta recibida:', response); // Para debugging
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data); // Para debugging

            // Verifica que data sea un array y tenga elementos
            if (!Array.isArray(data) || data.length === 0) {
                throw new Error('No hay datos para mostrar');
            }

            // Procesa los datos
            const tipos = data.map(item => item.tipo);
            const totales = data.map(item => parseInt(item.total));

            console.log('Tipos:', tipos); // Para debugging
            console.log('Totales:', totales); // Para debugging

            // Configura y crea el gráfico
            Highcharts.chart('container', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Total de Dispositivos por Tipo'
                },
                xAxis: {
                    categories: tipos,
                    title: {
                        text: 'Tipo de Dispositivo'
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Cantidad de Dispositivos'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.x + '</b><br/>' +
                            'Cantidad: ' + this.y + ' dispositivos';
                    }
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true,
                            format: '{y}'
                        }
                    }
                },
                series: [{
                    name: 'Dispositivos',
                    data: totales,
                    color: '#4CAF50'
                }]
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('container').innerHTML = `
                <div style="color: red; padding: 20px; text-align: center;">
                    <h3>Error al cargar el gráfico</h3>
                    <p>${error.message}</p>
                </div>`;
        });
});