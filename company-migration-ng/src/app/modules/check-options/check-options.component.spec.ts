import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckOptionsComponent } from './check-options.component';

describe('CheckOptionsComponent', () => {
  let component: CheckOptionsComponent;
  let fixture: ComponentFixture<CheckOptionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CheckOptionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CheckOptionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
