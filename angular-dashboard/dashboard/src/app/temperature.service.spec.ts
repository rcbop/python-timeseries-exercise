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

    const req = httpMock.expectOne(`${service.baseUrl}/sensors/?limit=500`);
    expect(req.request.method).toEqual('GET');
    req.flush(mockTemperatureData);
  });

  it('should parseDataPoint', () => {
    const mockRawTemperatureDataPoint = {
      _id: '123',
      timestamp: '2022-01-01T00:00:00.000Z',
      value: 22,
      metadata: {
        area: 'kitchen',
        type: 'temperature',
        uuid: 'abc'
      }
    };

    const mockTemperatureDataPoint = {
      id: '123',
      timestamp: new Date('2022-01-01T00:00:00.000Z'),
      value: 22,
      area: 'kitchen',
      type: 'temperature',
      sensor_uuid: 'abc'
    };

    const result = service.parseDataPoint(mockRawTemperatureDataPoint);
    expect(result).toEqual(mockTemperatureDataPoint);
  });

  it('should getParsedDataWithUpdatingInterval', () => {
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

    const mockParsedTemperatureData = [
      {
        id: '123',
        timestamp: new Date('2022-01-01T00:00:00.000Z'),
        value: 22,
        area: 'kitchen',
        type: 'temperature',
        sensor_uuid: 'abc'
      },
      {
        id: '456',
        timestamp: new Date('2022-01-01T01:00:00.000Z'),
        value: 23,
        area: 'bedroom',
        type: 'temperature',
        sensor_uuid: 'def'
      }
    ];

    service.getParsedDataWithUpdatingInterval().subscribe((data) => {
      expect(data).toEqual(mockParsedTemperatureData);
    });

    const req = httpMock.expectOne(`${service.baseUrl}/sensors/?limit=500`);
    expect(req.request.method).toEqual('GET');
    req.flush(mockTemperatureData);
  });

  it('it should getParsedDataWithUpdatingIntervalGroupedBySensor', () => {
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

    const mockParsedTemperatureData = {
      abc: [
        {
          id: '123',
          timestamp: new Date('2022-01-01T00:00:00.000Z'),
          value: 22,
          area: 'kitchen',
          type: 'temperature',
          sensor_uuid: 'abc'
        },
      ],
      def: [
        {
          id: '456',
          timestamp: new Date('2022-01-01T01:00:00.000Z'),
          value: 23,
          area: 'bedroom',
          type: 'temperature',
          sensor_uuid: 'def'
        },
      ]
    };

    service.getParsedDataWithUpdatingIntervalGroupedBySensor().subscribe((data) => {
      expect(data).toEqual(mockParsedTemperatureData);
    });

    const req = httpMock.expectOne(`${service.baseUrl}/sensors/?limit=500`);
    expect(req.request.method).toEqual('GET');
    req.flush(mockTemperatureData);
  });
});
