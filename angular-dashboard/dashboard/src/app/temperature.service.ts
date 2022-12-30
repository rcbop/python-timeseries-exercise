import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';

import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, concat, interval, map, of, switchMap } from 'rxjs';
import { TemperatureDataPoint, RawTemperatureDataPoint } from './model';

@Injectable({
  providedIn: 'root'
})
export class TemperatureService {
  baseUrl: string = environment.baseUrl;

  constructor(private http: HttpClient) { }

  /**
   * Returns an observable that emits the raw data from the server
   *
   * @returns Observable<TemperatureRawDataPoint[]>
   */
  getData(startTimestamp?: Date, endTimestamp?: Date): Observable<RawTemperatureDataPoint[]> {
    let params = new HttpParams();
    if (startTimestamp) {
      params = params.set('timestamp[gte]', startTimestamp.toISOString());
    }
    if (endTimestamp) {
      params = params.set('timestamp[lte]', endTimestamp.toISOString());
    }
    if (!startTimestamp && !endTimestamp) {
      params = params.set('limit', '100');
    }
    return of(null).pipe(
      switchMap(() => this.http.get<RawTemperatureDataPoint[]>(`${this.baseUrl}/temperature/`, { params }))
    );
  }

  /**
   * Returns an observable that emits the parsed data from the server
   * and then emits the parsed data again after the specified interval.
   *
   * @returns Observable<TemperatureDataPoint[]>
   */
  getParsedDataWithUpdatingInterval(startTimestamp?: Date, endTimestamp?: Date, fetchInterval: number = 5000): Observable<TemperatureDataPoint[]> {
    return concat(this.getData(startTimestamp, endTimestamp), interval(fetchInterval).
      pipe(switchMap(() => this.getData(startTimestamp, endTimestamp)))).
      pipe(
        map((response) => {
          return response.map((item) => {
            return {
              id: item._id,
              timestamp: new Date(item.timestamp),
              temperature: item.temperature,
              sensor_area: item.metadata.sensor_area
            };
          });
        })
      );
  }
}
