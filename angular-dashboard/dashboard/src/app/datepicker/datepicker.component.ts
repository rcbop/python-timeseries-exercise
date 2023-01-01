import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-datepicker',
  templateUrl: './datepicker.component.html',
  styleUrls: ['./datepicker.component.less']
})
export class DatepickerComponent {
  startDate?: Date;
  endDate?: Date;
  @Output() updateChartEvent = new EventEmitter<{startDate?: Date, endDate?: Date}>();

  updateChart() {
    console.log('updateChart');
    this.updateChartEvent.emit({ startDate: this.startDate, endDate: this.endDate });
  }
}
