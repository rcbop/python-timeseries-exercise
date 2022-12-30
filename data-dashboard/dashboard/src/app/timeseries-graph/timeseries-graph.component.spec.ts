import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeseriesGraphComponent } from './timeseries-graph.component';

xdescribe('TimeseriesGraphComponent', () => {
  let component: TimeseriesGraphComponent;
  let fixture: ComponentFixture<TimeseriesGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TimeseriesGraphComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TimeseriesGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
