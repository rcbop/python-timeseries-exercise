import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormField, MatFormFieldModule } from '@angular/material/form-field';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { NgxMaterialTimepickerModule, NgxTimepickerFieldComponent } from 'ngx-material-timepicker';
import { DatepickerComponent } from './datepicker.component';

xdescribe('DatepickerComponent', () => {
  let component: DatepickerComponent;
  let fixture: ComponentFixture<DatepickerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        MatDatepickerModule,
        MatNativeDateModule,
        MatFormFieldModule,
        FormsModule,
        NoopAnimationsModule,
        NgxMaterialTimepickerModule
      ],
      declarations: [
        DatepickerComponent,
        MatFormField,
        NgxTimepickerFieldComponent
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DatepickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
