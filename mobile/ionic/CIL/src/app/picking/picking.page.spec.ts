import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { PickingPage } from './picking.page';

describe('PickingPage', () => {
  let component: PickingPage;
  let fixture: ComponentFixture<PickingPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PickingPage ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(PickingPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
