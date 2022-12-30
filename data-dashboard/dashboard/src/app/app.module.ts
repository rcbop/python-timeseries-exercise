import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TemperatureService } from './temperature.service';
import { TimeseriesGraphComponent } from './timeseries-graph/timeseries-graph.component';
import { DatepickerComponent } from './datepicker/datepicker.component';


@NgModule({
  declarations: [
    AppComponent,
    TimeseriesGraphComponent,
    DatepickerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    MatNativeDateModule,
    BrowserAnimationsModule
  ],
  providers: [
    TemperatureService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
