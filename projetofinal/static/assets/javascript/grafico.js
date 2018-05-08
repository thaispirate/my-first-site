$(document).ready(function () {
    if (show_radar != 1){
        var ctx = document.getElementById("container")
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
        var chart = new Chart(ctx,coluna);
    }

    if (show_radar == 1) {
        var ctx2 = document.getElementById("radar")
        var radar = {
                type: 'radar',
                data: {
                    labels: ["Adaptativo", "Reativo", "Criativo"],
                    datasets: [{
                        label: paciente['paciente'],
                        data: dadosRadar['paciente'],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.2)',

                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1
                    },{
                        label: 'Limite Superior',
                        data: dadosRadar['limite superior'],
                        backgroundColor: [
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    },{
                        label: 'Limite Inferior',
                        data: dadosRadar['limite inferior'],
                        backgroundColor: [
                            'rgba(153, 102, 255, 0.2)'
                        ],
                        borderColor: [
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
        var chart_radar = new Chart(ctx2,radar)
     }

    $("#selectAll").click(function() {
        $( this ).closest('form').find(':checkbox').prop( 'checked' , this.checked ? true : false );
    });

});

