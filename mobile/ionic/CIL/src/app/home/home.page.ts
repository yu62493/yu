import { Component } from '@angular/core';
import { Storage } from '@ionic/storage';
import { GlobalParamService } from '../global-param.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  constructor(private ApiURL: GlobalParamService, private storage: Storage) {}

  WEBshortURL = 'https://lihi.cc/ZPvoX';

  // tslint:disable-next-line:use-lifecycle-interface
  ngOnInit() {
//    this.ApiURL.tran_shortURL(this.WEBshortURL, 'OrgAPIURL');
  }

}
