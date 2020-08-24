import { TestBed } from '@angular/core/testing';

import { PickingapiService } from './pickingapi.service';

describe('PickingapiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: PickingapiService = TestBed.get(PickingapiService);
    expect(service).toBeTruthy();
  });
});
