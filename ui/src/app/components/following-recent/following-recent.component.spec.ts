import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FollowingRecentComponent } from './following-recent.component';

describe('FollowingRecentComponent', () => {
  let component: FollowingRecentComponent;
  let fixture: ComponentFixture<FollowingRecentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FollowingRecentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FollowingRecentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
