import { Injectable } from '@angular/core';
import { InAppBrowser } from '@ionic-native/in-app-browser/ngx';
import { Storage } from '@ionic/storage';

@Injectable({
  providedIn: 'root'
})
export class GlobalParamService {

  OrgAPIURL = '';

  constructor(private iab: InAppBrowser, private storage: Storage) { }

  tran_shortURL(shortURL, storageName) {
    const browser = this.iab.create(shortURL, '_self', {location: 'no', hidden: 'yes'});
    browser.on('loadstop').subscribe( (event) => {
      console.log('tran_shortURL:', event.url);
      this.OrgAPIURL = event.url;
      this.storage.set(storageName, this.OrgAPIURL);
      browser.close();
    }, (err) => { console.log('短址轉換失敗'); } );
  }

}
