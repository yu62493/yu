import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CRDetailPage } from './crdetail.page';

describe('CRDetailPage', () => {
  let component: CRDetailPage;
  let fixture: ComponentFixture<CRDetailPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CRDetailPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CRDetailPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
