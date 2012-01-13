/**
 * Created by PyCharm.
 * User: bteam
 * Date: 11.01.12
 * Time: 13:05
 * To change this template use File | Settings | File Templates.
 */
time_response = function(args){
return new Highcharts.Chart({
    chart:{ renderTo:args.node || 'chart',
        defaultSeriesType:'line'},
    title: {text:null, x:0,floating:true},
    legend: { enabled:false },
    series:[ {name:name,data:args.step} ],
    xAxis:{title:{text:null},
        title: { text:null },
        startOnTick: false,
        minorTickInterval: 'auto',
        lineColor: '#000',
        lineWidth: 1,
        tickWidth: 1,
        tickColor: '#010'
    },
    yAxis: {
        title: { text:null },
        startOnTick: false,
        minorTickInterval: 'auto',
        lineColor: '#000',
        lineWidth: 1,
        tickWidth: 1,
        tickColor: '#000'
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -10,
        y: 100,
        borderWidth: 1
    }
    ,tooltip: {
        formatter: function() {
            return '<b>'+ this.series.name+ ':</b> <i>'+ this.y +'</i><br/>'

        }}
});

}