import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts';
import { TemperatureDataPoint } from '../model';
import { TemperatureService } from '../temperature.service';

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

  // TODO implement event emitter to update chart start and end date from the datepicker
  startDate?: Date = undefined;
  endDate?: Date = undefined;

  chart: any;
  data: TemperatureDataPoint[] = [];

  private options: any = {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: 'House Temperature Data',
      align: 'left'
    },
    subtitle: {
      text: document.ontouchstart === undefined ?
        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
      align: 'left'
    },
    tooltip: {
      formatter: () => {
        let index = this.chart.hoverPoint.index;
        let point = this.data[index-1]
        if (!point) {
          return 'No point found';
        }
        return `Sensor area: <b>${point.sensor_area}</b><br>Temperature: ${point.temperature}<br>Timestamp: ${point.temperature}`;
      }
    },
    legend: {
      enabled: false
    },
    credits: {
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
    this.updateChart();
  }

  updateChart() {
    this.timeseriesAPIService.getParsedDataWithUpdatingInterval(this.startDate, this.endDate).subscribe((data) => {
      this.data = data;

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

  constructor(private timeseriesAPIService: TemperatureService) {}
}
