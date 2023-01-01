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

  startDate?: Date;
  endDate?: Date;

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

  onDatePickerUpdateEvent(event: { startDate: Date, endDate: Date }) {
    console.log('Received update event:', event);
    this.startDate = event.startDate;
    this.endDate = event.endDate;
    this.updateChart();
  }

  updateData(data: TemperatureDataPoint[]) {
    this.data = data;
    this.chart.series[0].setData(this.data.map((point) => [point.timestamp, point.temperature]));
  }

  updateChart() {
    this.timeseriesAPIService.getParsedDataWithUpdatingInterval(this.startDate, this.endDate).subscribe((data) => {
      this.updateData(data);
    });
  }

  constructor(private timeseriesAPIService: TemperatureService) {}
}
