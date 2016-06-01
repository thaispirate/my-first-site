    $(document).ready(function () {
        var options = {
            colors: ["#7cb5ec", "#f7a35c"],
            chart: {
                type: 'column',
                renderTo:'container'
            },
            title: {
                text: 'Areas Afetivas'
            },
            xAxis: {
                categories: [
                    'Afetivo-Relacional',
                    'Produtividade',
                    'Orgânico',
                    'Socio-Cultural',
                    'Espiritual',
                ],
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'taxa (%)'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series:[]
            }

        var chart = new Highcharts.Chart(options);
        for(var item in dados){
            chart.addSeries({
                name:item,
                data:dados[item]
            });
        }

     });