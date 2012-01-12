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
    title: {text:args.name, x:0,floating:true},
    legend: { enabled:false },
    series:[ {name:name,data:args.data} ],
    xAxis:{title:{text:null}},
    yAxis: {
        title: { text:null },
        startOnTick: false
    }
//    ,tooltip: {
//        formatter: function() {
//            return '<b>'+ this.series.name+ ':</b> <i>'+ this.y +'</i><br/>'+
//                Highcharts.dateFormat('%d-%m-%Y %H:%M', this.x);
//        }}
});

}