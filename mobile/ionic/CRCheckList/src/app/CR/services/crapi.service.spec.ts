import { TestBed } from '@angular/core/testing';

import { CrapiService } from './crapi.service';

describe('CrapiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CrapiService = TestBed.get(CrapiService);
    expect(service).toBeTruthy();
  });
});
