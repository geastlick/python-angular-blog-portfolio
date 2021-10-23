import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResponsivePaginatorComponent } from './responsive-paginator.component';

describe('ResponsivePaginatorComponent', () => {
  let component: ResponsivePaginatorComponent;
  let fixture: ComponentFixture<ResponsivePaginatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ResponsivePaginatorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ResponsivePaginatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
