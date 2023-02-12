import { Component, EventEmitter, Output } from '@angular/core';


@Component({
  selector: 'app-datepicker',
  templateUrl: './datepicker.component.html',
  styleUrls: ['./datepicker.component.less']
})
export class DatepickerComponent {
  startDate?: Date;
  endDate?: Date;
  startTimeValue?: Date;
  endTimeValue?: Date;

  @Output() updateChartEvent = new EventEmitter<{startDate?: Date, endDate?: Date}>();

  onSelect() {
    console.log('onSelect DateTime');
    if (!this.startDate || !this.endDate) {
      return;
    }
    let startDate = new Date(this.startDate);
    if (this.startTimeValue) {
      console.log("setting start time", this.startTimeValue)
      let time = new Date("1970-01-01 " + this.startTimeValue);
      startDate.setHours(time.getHours(), time.getMinutes());
    }
    let endDate = new Date(this.endDate);
    if (this.endTimeValue) {
      console.log("setting end time", this.endTimeValue)
      let time = new Date("1970-01-01 " + this.endTimeValue);
      endDate.setHours(time.getHours(), time.getMinutes());
    }
    console.log("emitting", startDate, endDate);
    this.updateChartEvent.emit({ startDate: this.startDate, endDate: this.endDate });
  }
}
