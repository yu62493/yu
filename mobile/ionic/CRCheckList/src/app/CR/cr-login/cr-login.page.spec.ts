import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrLoginPage } from './cr-login.page';

describe('CrLoginPage', () => {
  let component: CrLoginPage;
  let fixture: ComponentFixture<CrLoginPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrLoginPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrLoginPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
