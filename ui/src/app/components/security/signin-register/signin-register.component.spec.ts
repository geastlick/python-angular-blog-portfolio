import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SigninRegisterComponent } from './signin-register.component';

describe('SigninRegisterComponent', () => {
  let component: SigninRegisterComponent;
  let fixture: ComponentFixture<SigninRegisterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SigninRegisterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SigninRegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
