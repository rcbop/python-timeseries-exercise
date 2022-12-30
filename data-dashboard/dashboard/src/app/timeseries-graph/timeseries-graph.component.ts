import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts';
import { TimeseriesApiService } from '../timeseries-api.service';

declare var require: any;
let Boost = require('highcharts/modules/boost');
let noData = require('highcharts/modules/no-data-to-display');
let More = require('highcharts/highcharts-more');

Boost(Highcharts);
noData(Highcharts);
More(Highcharts);
noData(Highcharts);

@Component({
  selector: 'app-timeseries-graph',
  templateUrl: './timeseries-graph.component.html',
  styleUrls: ['./timeseries-graph.component.less']
})
export class TimeseriesGraphComponent implements OnInit {
  Highcharts = Highcharts;
  chart: any;
  private options: any = {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: 'Sample Data',
      align: 'left'
    },
    subtitle: {
      text: document.ontouchstart === undefined ?
        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
      align: 'left'
    },
    legend: {
      enabled: false
    },
    xAxis: {
      type: 'datetime',
      title: {
        text: 'Time'
      }
    },
    yAxis: {
      type: 'linear',
      title: {
        text: 'Temperature (°C)'
      }
    },
    series: [{
      name: 'Temperature Sensors',
      type: 'line',
      data: []
    }]
  }

  ngOnInit(): void {
    this.chart = Highcharts.chart('container', this.options);
    this.timeseriesAPIService.getTemperatureData().subscribe((data) => {
      console.log(data);
      // convert TemperatureDataPoint to Highcharts DataPoints [x, y]
      let convertedChartData = data.map((item) => {
        return [item.timestamp.getTime(), item.temperature];
      });
      this.chart.update(
        {
          series: [{
            data: convertedChartData
          }]
        },
      )
    });
  }

  constructor(private timeseriesAPIService: TimeseriesApiService) {
  }
}
