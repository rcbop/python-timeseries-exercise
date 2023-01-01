import { Component, ViewChild } from '@angular/core';
import { TimeseriesGraphComponent } from './timeseries-graph/timeseries-graph.component';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  title = 'Timeseries Dashboard';
  @ViewChild('timeseriesGraph', { static: true }) timeseriesGraph?: TimeseriesGraphComponent
}
