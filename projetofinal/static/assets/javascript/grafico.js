$(document).ready(function () {
        debugger
        var ctx = document.getElementById("container").getContext('2d');
//        var coluna = {
//            colors: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"],
//            type: 'column',
//            title: {
//                text: "Áreas Afetivas<br> "+paciente['paciente']
//            },
//            xAxis: {
//                categories: [
//                    'Afetivo-Relacional',
//                    'Produtividade',
//                    'Orgânico',
//                    'Espiritual',
//                    'Socio-Cultural',
//                ],
//                crosshair: true
//            },
//            yAxis: {
//                min: 0,
//                title: {
//                    text: 'Valor'
//                }
//            },
//            tooltip: {
//                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
//                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}:</td>' +
//                    '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
//                footerFormat: '</table>',
//                shared: true,
//                useHTML: true
//            },
//            plotOptions: {
//                column: {
//                    pointPadding: 0.2,
//                    borderWidth: 0
//                }
//            },
//            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
//            datasets: [{
//                label: '# of Votes',
//                data: [12, 19, 3, 5, 2, 3],
//                backgroundColor: [
//                    'rgba(255, 99, 132, 0.2)',
//                    'rgba(54, 162, 235, 0.2)',
//                    'rgba(255, 206, 86, 0.2)',
//                    'rgba(75, 192, 192, 0.2)',
//                    'rgba(153, 102, 255, 0.2)',
//                    'rgba(255, 159, 64, 0.2)'
//                ]
//            }]
//        }
        var coluna = {
            type: 'bar',
            data: {
                labels: ["Afetivo Relacional", "Produtividade", "Organico", "Espiritual", "Socio-Cultural"],
                datasets: [{
                    label: 'Areas Afetivas - '+ paciente['paciente'],
                    data: dados['dados'],
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
        }
        var chart = new Chart(ctx,container);
//        for(var item in dados){
//            chart.addSeries({
//                labels:item,
//                data:dados[item]
//            });
//        }

        // split the data set into ohlc and volume
     var ctx2 = document.getElementById("radar").getContext('2d');
//     var radar = {
//                xAxis: [{
//                    categories: ['Adaptativo','Reativo', 'Criativo'],
//                    crosshair: true
//                }],
//                chart: {
//                    renderTo: 'radar',
//                    zoomType:'none',
//                    pinchType:'none'
//                },
//                title: {
//                    text: 'Grau de Indiferenciação<br>'+ paciente['paciente']
//                },
//                yAxis: [{
//                    labels: {
//                        style: {
//                            color: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"]
//                        }
//                    },
//                    min: 0,
//                    title: {
//                        text: 'Pontuação',
//                        style: {
//                            color: ["#7cb5ec","#f7a35c","#ff095c","#FFDAB9","#FF0000","#AB82FF","#ADFF2F","#FF69B4"],
//                        }
//                    }
//                }],
//                plotOptions: {
//                    column: {
//                        pointPadding: 0.2,
//                        borderWidth: 0
//                    }
//                },
//                series: []
//     }
     var radar = {
            type: 'radar',
            data: {
                labels: ["Adaptativo", "Reativo", "Criativo"],
                datasets: [{
                    label: 'Grau de Indiferenciação - '+ paciente['paciente'],
                    data: [1,2,3],
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',

                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                }
            }
     }
     var chart_radar = new Chart(ctx2,radar);

//        var chart2 = new Highcharts.Chart(radar);
//
//        for(var item in dadosRadar){
//            if (item[0] != "L"){
//                chart2.addSeries({
//                    type:'bubble',
//                    name:item,
//                    data:dadosRadar[item],
//                    tooltip: {
//                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}:</td>' +
//                        '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
//                        footerFormat: '</table>',
//                        shared: true,
//                        useHTML: true
//                    }
//                });
//                }
//        }
//        chart2.addSeries({
//                name: 'Limites',
//                type: 'errorbar',
//                data: [[dadosRadar['Limite Inferior Adaptativo'],dadosRadar['Limite Superior Adaptativo']],
//                [dadosRadar['Limite Inferior Reativo'],dadosRadar['Limite Superior Reativo']],
//                [dadosRadar['Limite Inferior Criativo'],dadosRadar['Limite Superior Criativo']]],
//                tooltip: {
//                    pointFormat:  '(Limites esperados: Inferior={point.low} Superior={point.high})<br/>',
//                    footerFormat: '</table>',
//                    shared: true,
//                    useHTML: true
//                }
//
//        });
//
    $("#selectAll").click(function() {
        $( this ).closest('form').find(':checkbox').prop( 'checked' , this.checked ? true : false );
    });

});

