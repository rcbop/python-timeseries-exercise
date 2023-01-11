import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { TemperatureService } from './temperature.service';

describe('TemperatureService', () => {
  let service: TemperatureService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [TemperatureService]
    });

    service = TestBed.inject(TemperatureService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch temperature data', () => {
    const mockTemperatureData = [
      {
        _id: '123',
        timestamp: '2022-01-01T00:00:00.000Z',
        value: 22,
        metadata: {
          area: 'kitchen',
          type: 'temperature',
          uuid: 'abc'
        }
      },
      {
        _id: '456',
        timestamp: '2022-01-01T01:00:00.000Z',
        value: 23,
        sensor_uuid: 'def',
        metadata: {
          area: 'bedroom',
          type: 'temperature',
          uuid: 'def'
        }
      }
    ];

    service.getData().subscribe((data) => {
      expect(data).toEqual(mockTemperatureData);
    });

    const req = httpMock.expectOne(`${service.baseUrl}/sensors/?limit=100`);
    expect(req.request.method).toEqual('GET');
    req.flush(mockTemperatureData);
  });
});
