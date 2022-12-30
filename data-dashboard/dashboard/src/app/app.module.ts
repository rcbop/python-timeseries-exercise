import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TimeseriesGraphComponent } from './timeseries-graph/timeseries-graph.component';
import { TimeseriesApiService } from './timeseries-api.service';
import { HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [
    AppComponent,
    TimeseriesGraphComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    TimeseriesApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
