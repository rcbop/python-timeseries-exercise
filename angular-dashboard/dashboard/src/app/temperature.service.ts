import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';

import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, concat, interval, map, of, switchMap } from 'rxjs';
import { RawTemperatureDataPoint, TemperatureDataPoint } from './model';

@Injectable({
  providedIn: 'root'
})
export class TemperatureService {
  baseUrl: string = environment.baseUrl;

  constructor(private http: HttpClient) { }

  /**
   * Parses the raw data from the server into the format that the
   * dashboard expects.
   *
   * @param item RawTemperatureDataPoint
   * @returns TemperatureDataPoint
   * @example
   * {
   *  "id": "5e7f9b9b9b9b9b9b9b9b9b9b",
   * "value": 23.5,
   * "timestamp": "2020-03-25T12:00:00.000Z",
   * "sensor_uuid": "5e7f9b9b9b9b9b9b9b9b9b9b",
   * "area": "kitchen",
   * "type": "temperature"
   * }
   * */
  private parseDataPoint(item: RawTemperatureDataPoint): TemperatureDataPoint {
    return {
      id: item._id,
      timestamp: new Date(item.timestamp),
      value: item.value,
      area: item.metadata.area,
      type: item.metadata.type,
      sensor_uuid: item.metadata.uuid
    };
  }

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
      switchMap(() => this.http.get<RawTemperatureDataPoint[]>(`${this.baseUrl}/sensors/`, { params }))
    );
  }

  /**
   * Returns an observable that emits the parsed data from the server
   * and then emits the parsed data again after the specified interval.
   *
   * @returns Observable<TemperatureDataPoint[]>
   */
  getParsedDataWithUpdatingInterval(startTimestamp?: Date, endTimestamp?: Date, fetchInterval: number = 5000): Observable<TemperatureDataPoint[]> {
    return concat(
      this.getData(startTimestamp, endTimestamp),
      interval(fetchInterval).
        pipe(switchMap(() => this.getData(startTimestamp, endTimestamp)))).
      pipe(
        map((response) => {
          return response.map((item) => this.parseDataPoint(item));
        }),
      );
  }

  /**
   * Returns an observable that emits the parsed data from the server
   * and then emits the parsed data again after the specified interval.
   * The data is grouped by sensor.
   *
   * @returns Observable<{ [key: string]: TemperatureDataPoint[] }>
   * @example
   * {
   *  "5e7f9b9b9b9b9b9b9b9b9b9b": [
   *    {
   *     "id": "5e7f9b9b9b9b9b9b9b9b9b9b",
   *     "value": 23.5,
   *     "timestamp": "2020-03-25T12:00:00.000Z",
   *     "sensor_uuid": "5e7f9b9b9b9b9b9b9b9b9b9b",
   *     "area": "kitchen",
   *     "type": "temperature"
   *    }
   *  ]
   * }
   * */
  getParsedDataWithUpdatingIntervalGroupedBySensor(startTimestamp?: Date, endTimestamp?: Date, fetchInterval: number = 5000): Observable<{ [key: string]: TemperatureDataPoint[] }> {
    return this.getParsedDataWithUpdatingInterval(startTimestamp, endTimestamp, fetchInterval).pipe(
      map((data) => {
        const result: { [key: string]: TemperatureDataPoint[] } = {};
        data.forEach((item) => {
          if (!result[item.sensor_uuid]) {
            result[item.sensor_uuid] = [];
          }
          result[item.sensor_uuid].push(item);
        });
        return result;
      })
    );
  }
}
