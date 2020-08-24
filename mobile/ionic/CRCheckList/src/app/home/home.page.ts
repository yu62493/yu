import { Component } from '@angular/core';
import { GlobalParamService } from '../auth/global-param.service';
import { Storage } from '@ionic/storage';

import * as data from '../data.json';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  constructor(private ApiURL: GlobalParamService, private storage: Storage) {}

  GlobalParam: any = (data as any).default;

  userid = '';
  WEBshortURL = '';

  // tslint:disable-next-line:use-life-cycle-interface
  ngOnInit() {
    this.WEBshortURL = this.GlobalParam[0].WEBshortURL;
    console.log('webshorturl:', this.WEBshortURL);
    this.ApiURL.tran_shortURL(this.WEBshortURL, 'OrgAPIURL2');
  }

  ionViewWillEnter(){
    this.LoginUSER();
  }
  private LoginUSER(){
    this.storage.ready().then(() => {
      this.storage.get('EMPLNO').then((val) => {
        this.userid = val;
        console.log('user id : ', this.userid);
      });
    });
  }

}
