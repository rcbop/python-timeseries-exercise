import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { interval, switchMap, map, Observable } from 'rxjs';
import { TemperatureRawDataPoint, TemperatureDataPoint } from './model';

@Injectable({
  providedIn: 'root'
})
export class TimeseriesApiService {

  private fetchInterval: number = 5000;

  constructor(private http: HttpClient) {}

  getTemperatureData(): Observable<TemperatureDataPoint[]> {
    // Fetch data from the API every 5 seconds
    return interval(this.fetchInterval).pipe(
      // Switch to a new observable each time the interval emits
      switchMap(() => this.http.get<TemperatureRawDataPoint[]>('http://localhost:8000/temperature/')),
      map((response) => {
        // Parse the raw data into the TemperatureDataPoint interface
        return response.map((item) => {
          return {
            id: item._id,
            timestamp: new Date(item.timestamp),
            temperature: item.temperature,
            metadata: item.metadata
          };
        });
      })
    );
  }
}
