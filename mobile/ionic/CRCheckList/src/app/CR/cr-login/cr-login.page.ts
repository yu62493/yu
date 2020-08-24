import { Component, OnInit } from '@angular/core';
import { InAppBrowser } from '@ionic-native/in-app-browser/ngx';
import { Platform } from '@ionic/angular';
import { Storage } from '@ionic/storage';

@Component({
  selector: 'app-cr-login',
  templateUrl: './cr-login.page.html',
  styleUrls: ['./cr-login.page.scss'],
})
export class CrLoginPage implements OnInit {

  constructor(private iab: InAppBrowser, private plt: Platform, private storage: Storage) { }

  OrgAPIURL2 = '';
  userid = '';

  ngOnInit() {
    this.getParam();
  }

  private getParam(){
    this.storage.ready().then(() => {
      this.storage.get('EMPLNO').then((val) => {
        this.userid = val;
        console.log('user id : ', this.userid);
      });
      this.storage.get('OrgAPIURL2').then((val) => {
        this.OrgAPIURL2 = val;
        console.log('OrgAPIURL2 : ', this.OrgAPIURL2);
      });
    });

  }

  public launch(url, uid, opentype) {
    this.plt.ready().then(() => {
      if (this.OrgAPIURL2 === '') {
        this.OrgAPIURL2 = url;
      }
      this.OrgAPIURL2 = this.OrgAPIURL2.replace('MECH/MECH000M', 'MECH/MECH001M') + '?user_id=' + uid;
      console.log('lauch url:', this.OrgAPIURL2);
      const browser = this.iab.create(this.OrgAPIURL2, opentype, {location: 'no'});
      browser.show();

    });

  }

}
