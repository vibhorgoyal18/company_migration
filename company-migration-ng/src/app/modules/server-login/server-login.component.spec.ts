import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServerLoginComponent } from './server-login.component';

describe('ServerLoginComponent', () => {
  let component: ServerLoginComponent;
  let fixture: ComponentFixture<ServerLoginComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServerLoginComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServerLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
