import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxMaterialTimepickerModule } from 'ngx-material-timepicker';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DatepickerComponent } from './datepicker/datepicker.component';
import { TemperatureService } from './temperature.service';
import { TimeseriesGraphComponent } from './timeseries-graph/timeseries-graph.component';


@NgModule({
  declarations: [
    AppComponent,
    TimeseriesGraphComponent,
    DatepickerComponent
  ],
  imports: [
    BrowserModule,
    NgxMaterialTimepickerModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    MatNativeDateModule,
    ReactiveFormsModule,
    BrowserAnimationsModule
  ],
  providers: [
    TemperatureService
  ],
  bootstrap: [AppComponent],
  exports: [MatFormFieldModule, MatInputModule]
})
export class AppModule { }
