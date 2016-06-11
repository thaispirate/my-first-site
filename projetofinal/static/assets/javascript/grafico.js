    $(document).ready(function () {
        var options = {
            colors: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"],
            chart: {
                type: 'column',
                renderTo:'container'
            },
            title: {
                text: "Áreas Afetivas ("+paciente['paciente']+")"
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
                    text: 'nota'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}:</td>' +
                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
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
