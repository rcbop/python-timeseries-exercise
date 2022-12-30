import { TestBed } from '@angular/core/testing';

import { TimeseriesApiService } from './timeseries-api.service';

describe('TimeseriesApiService', () => {
  let service: TimeseriesApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TimeseriesApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should have a getTemperatureData method', () => {
    expect(service.getTemperatureData).toBeTruthy();
  });

  it('should have a getTemperatureData method that returns an Observable', () => {
    expect(service.getTemperatureData().subscribe).toBeTruthy();
  });

  it('should have a getTemperatureData method that returns an Observable that emits an array of objects', () => {
    service.getTemperatureData().subscribe((data) => {
      expect(data).toBeTruthy();
      expect(data.length).toBeGreaterThan(0);
      expect(data[0]).toBeTruthy();
    });
  });
});
