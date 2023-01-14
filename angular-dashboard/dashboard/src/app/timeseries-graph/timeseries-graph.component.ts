import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts';
import { TemperatureDataPoint } from '../model';
import { TemperatureService } from '../temperature.service';

declare var require: any;
let Boost = require('highcharts/modules/boost');
let noData = require('highcharts/modules/no-data-to-display');
let More = require('highcharts/highcharts-more');
let darkTheme = require('highcharts/themes/dark-unica');

darkTheme(Highcharts);
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
  allSeriesData: { [key: string]: TemperatureDataPoint[] } = {};

  formatTooltipForData = (data: TemperatureDataPoint): string => {
    let timestamp = new Date(data.timestamp).toISOString().slice(0, 19).replace('T', ' ');
    if (data.type === 'TEMPERATURE') {
      return `SensorID: ${data.sensor_uuid}</br>Sensor area: <b>${data.area}</b><br>Temperature: ${data.value}°C<br>Timestamp: ${timestamp}`;
    } else if (data.type === 'HUMIDITY') {
      return `SensorID: ${data.sensor_uuid}</br>Sensor area: <b>${data.area}</b><br>Humidity: ${data.value}%<br>Timestamp: ${timestamp}`;
    } else {
      return `SensorID: ${data.sensor_uuid}</br>Sensor area: <b>${data.area}</b><br>Reading: ${data.value}<br>Timestamp: ${timestamp}`;
    }
  }

  formatTooltip = () => {
    let point = this.chart.hoverPoint;
    if (!point) { return 'No point found'; }
    let key = point.series.name;
    let data = this.allSeriesData[key][point.index];
    if (!data) {
      return 'No point found';
    }
    return this.formatTooltipForData(data);

  }

  private options: any = {
    chart: {
      zoomType: 'x'
    },
    title: {
      text: 'House Sensors Data',
      align: 'left'
    },
    subtitle: {
      text: document.ontouchstart === undefined ?
        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
      align: 'left'
    },
    tooltip: {
      formatter: () => this.formatTooltip()
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
        text: 'Temperature (°C) / Humidity (%)'
      }
    },
    series: []
  }

  constructor(private timeseriesAPIService: TemperatureService) { }

  ngOnInit(): void {
    this.chart = Highcharts.chart('container', this.options);
    this.updateChart();
  }

  updateDataDictionary(data: { [key: string]: TemperatureDataPoint[] }): void {
    while(this.chart.series.length > 0)
      this.chart.series[0].remove(true);

    for (const key in data) {
      const seriesData = data[key].map((point) => [point.timestamp, point.value]);
      this.chart.addSeries({
        name: key,
        data: seriesData
      });
    }
    this.allSeriesData = data;
  }

  updateChartWithDateRange(startDate?: Date, endDate?: Date) {
    this.timeseriesAPIService.getParsedDataWithUpdatingIntervalGroupedBySensor(startDate, endDate).subscribe((data) => {
      this.updateDataDictionary(data);
    });
  }

  updateChart() {
    this.timeseriesAPIService.getParsedDataWithUpdatingIntervalGroupedBySensor().subscribe((data) => {
      this.updateDataDictionary(data);
    });
  }

}
