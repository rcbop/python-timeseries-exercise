
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { Observable } from "rxjs";
import { TemperatureDataPoint } from "../model";
import { TemperatureService } from "../temperature.service";
import { TimeseriesGraphComponent } from "./timeseries-graph.component";
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

class MockTemperatureService {
  getParsedDataWithUpdatingIntervalGroupedBySensor(startDate?: Date, endDate?: Date, fetchInterval?: number): Observable<{ [key: string]: TemperatureDataPoint[] }> {
    return new Observable<{ [key: string]: TemperatureDataPoint[] }>(observer => {
      observer.next(mockParsedTemperatureData);
    });
  }
}

describe('TimeseriesGraphComponent', () => {

  let component: TimeseriesGraphComponent;
  let fixture: ComponentFixture<TimeseriesGraphComponent>;
  let temperatureService: TemperatureService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TimeseriesGraphComponent],
      providers: [
        { provide: TemperatureService, useClass: MockTemperatureService }
      ]
    })
      .compileComponents();
    fixture = TestBed.createComponent(TimeseriesGraphComponent);
    component = fixture.componentInstance;
    temperatureService = TestBed.inject(TemperatureService);

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call getParsedDataWithUpdatingIntervalGroupedBySensor', () => {
    spyOn(temperatureService, 'getParsedDataWithUpdatingIntervalGroupedBySensor').and.callThrough();
    component.ngOnInit();
    expect(temperatureService.getParsedDataWithUpdatingIntervalGroupedBySensor).toHaveBeenCalled();
  });
});
