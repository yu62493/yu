import { TestBed } from '@angular/core/testing';

import { GlobalParamService } from './global-param.service';

describe('GlobalParamService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: GlobalParamService = TestBed.get(GlobalParamService);
    expect(service).toBeTruthy();
  });
});
