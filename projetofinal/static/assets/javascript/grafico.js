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
                    'Socio-Cultural',
                    'Espiritual',
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
        var radar = {
            chart: {
                polar: true,
                type: 'line',
                renderTo:'radar'
            },

            title: {
                text: "Grau de Indiferenciação<br>"+paciente['paciente'],
            },

            pane: {
                size: '80%'
            },

            xAxis: {
                categories: ['Adaptativo', 'Reativo', 'Criativo'],
                tickmarkPlacement: 'on',
                lineWidth: 0
            },

            yAxis: {
                gridLineInterpolation: 'polygon',
                lineWidth: 0,
                min: 0
            },

            tooltip: {
                shared: true,
                pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
            },


            series:[]

            }

        var chart2 = new Highcharts.Chart(radar);
        for(var item in dadosRadar){
            chart2.addSeries({
                name:item,
                data:dadosRadar[item],
                pointPlacement: 'on'
            });
        }


    $("#selectAll").click(function() {
        $( this ).closest('form').find(':checkbox').prop( 'checked' , this.checked ? true : false );
    });

});
