import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FollowingBlogsComponent } from './following-blogs.component';

describe('FollowingBlogsComponent', () => {
  let component: FollowingBlogsComponent;
  let fixture: ComponentFixture<FollowingBlogsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FollowingBlogsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FollowingBlogsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
