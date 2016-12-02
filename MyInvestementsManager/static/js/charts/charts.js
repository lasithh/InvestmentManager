function drawPieChart(containerID, title, dataType, dataArray) {
	$('#' + containerID)
			.highcharts(
					{
						chart : {
							plotBackgroundColor : null,
							plotBorderWidth : null,
							plotShadow : false,
							type : 'pie'
						},
						title : {
							text : title
						},
						tooltip : {
							pointFormat : '{series.name}: <b>{point.percentage:.1f}%</b>'
						},
						plotOptions : {
							pie : {
								allowPointSelect : true,
								cursor : 'pointer',
								dataLabels : {
									enabled : true,
									format : '<b>{point.name}</b>: {point.percentage:.1f} %',
									style : {
										color : (Highcharts.theme && Highcharts.theme.contrastTextColor)
												|| 'black'
									}
								}
							}
						},
						series : [ {
							name : dataType,
							colorByPoint : true,
							data : dataArray
						} ]
					});
}




function drawBarChart(containerID, title, names, values){
	$(function () {
	    // Create the chart
	    $('#' + containerID).highcharts({
	        chart: {
	            type: 'column'
	        },
	        title: {
	            text: title
	        },
	        xAxis: {
	            categories: names
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: 'Sectors',
	            data: values
	        }]
	    });
	});
}
