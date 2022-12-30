import { Component } from '@angular/core';

@Component({
  selector: 'app-datepicker',
  templateUrl: './datepicker.component.html',
  styleUrls: ['./datepicker.component.less']
})
export class DatepickerComponent {
  updateChart() {
    console.log('updateChart');
  }
}
