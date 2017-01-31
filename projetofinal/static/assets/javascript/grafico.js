$(document).ready(function () {

        var coluna = {
            colors: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"],
            chart: {
                type: 'column',
                renderTo:'container'
            },
            title: {
                text: "Áreas Afetivas<br> "+paciente['paciente']
            },
            xAxis: {
                categories: [
                    'Afetivo-Relacional',
                    'Produtividade',
                    'Orgânico',
                    'Espiritual',
                    'Socio-Cultural',
                ],
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Valor'
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

        var chart = new Highcharts.Chart(coluna);
        for(var item in dados){
            chart.addSeries({
                name:item,
                data:dados[item]
            });
        }

        // split the data set into ohlc and volume

 var radar = {
            xAxis: [{
                categories: ['Adaptativo','Reativo', 'Criativo']
            }],
            chart: {
                zoomType: 'xy',
                renderTo: 'radar'
            },
            title: {
                text: 'Grau de Indiferenciação<br>'+ paciente['paciente']
            },
            yAxis: [{
                labels: {
                    style: {
                        color: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"]
                    }
                },
                title: {
                    text: 'Pontuação',
                    style: {
                        color: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"],
                    }
                }
            }],

            tooltip: {
                shared: true
            },

            series: []
}


        var chart2 = new Highcharts.Chart(radar);

        for(var item in dadosRadar){
            if (item[0] != "L"){
                chart2.addSeries({
                    type:'bubble',
                    name:item,
                    data:dadosRadar[item],
                    tooltip: {
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}:</td>' +
                        '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                    }
                });
                }
        }
        chart2.addSeries({
                name: 'Limites',
                type: 'errorbar',
                data: [[dadosRadar['Limite Inferior Adaptativo'],dadosRadar['Limite Superior Adaptativo']],
                [dadosRadar['Limite Inferior Reativo'],dadosRadar['Limite Superior Reativo']],
                [dadosRadar['Limite Inferior Criativo'],dadosRadar['Limite Superior Criativo']]],
                tooltip: {
                pointFormat:  '(Limites esperados: Inferior={point.low} Superior={point.high})<br/>'
                }

        });

    $("#selectAll").click(function() {
        $( this ).closest('form').find(':checkbox').prop( 'checked' , this.checked ? true : false );
    });

});

