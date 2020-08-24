import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrNfcPage } from './cr-nfc.page';

describe('CrNfcPage', () => {
  let component: CrNfcPage;
  let fixture: ComponentFixture<CrNfcPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrNfcPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrNfcPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
