import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectionDetailComponent } from './projection-detail.component';

describe('ProjectionDetailComponent', () => {
  let component: ProjectionDetailComponent;
  let fixture: ComponentFixture<ProjectionDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectionDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectionDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
