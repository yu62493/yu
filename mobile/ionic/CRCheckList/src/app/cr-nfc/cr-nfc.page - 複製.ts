import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { Platform } from '@ionic/angular';
import { NFC, Ndef } from '@ionic-native/nfc/ngx';
import { InAppBrowser } from '@ionic-native/in-app-browser/ngx';
import { Storage } from '@ionic/storage';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';


@Component({
  selector: 'app-cr-nfc',
  templateUrl: './cr-nfc.page.html',
  styleUrls: ['./cr-nfc.page.scss'],
})
export class CrNfcPage implements OnInit {
  granted: boolean;
  denied: boolean;
  scanned: boolean;
  tagId: string;

  subscriptions: Array<Subscription> = new Array<Subscription>();
  ndefMsg: string;

  // tslint:disable-next-line:max-line-length
  constructor(private nfc: NFC, private ndef: Ndef, private iab: InAppBrowser, private storage: Storage,
              private plt: Platform, private alertController: AlertController, private router: Router ) {
      this.plt.ready().then(() => {
      console.log('PLT ready');
      this.cekNFC();
    });
   }

  OrgAPIURL2 = '';
  url = '';
  EMPLNO = '';
  ngOnInit() {
    this.test();
  }

  private test(){
    this.storage.ready().then(() => {
      this.storage.get('OrgAPIURL').then((val) => {
        console.log('OrgAPIURL val:', val);
        this.url = val;
      });
      this.storage.get('OrgAPIURL2').then((val) => {
        console.log('OrgAPIURL2 val:', val);
        this.OrgAPIURL2 = val;
      });
      this.storage.get('EMPLNO').then((val) => {
        console.log('EMPLNO val:', val);
        this.EMPLNO = val;
      });
    });
  }


  cekNFC() {
    this.nfc.enabled().then(() => {
      console.log('call NFC')
      this.addListenNFC();
    }).catch(err => {
    });
  }

  addListenNFC() {
    console.log('addListenNFC start');
    this.nfc.addNdefListener().subscribe(data => {
      if (data && data.tag && data.tag.id) {
          if (data.tag.ndefMessage) {
              let payload = data.tag.ndefMessage[0].payload;
              let tagContent = this.nfc.bytesToString(payload).substring(3);
              console.log('payload:', payload);
              console.log('tagcontent:', tagContent);
          }
      }
    });

  }

  listenToNdef() {
    console.log('按下 listenToNdef');
    this.presentAlert('NFC感應','請靠近NFC tag 進行感應');
    this.nfc.addNdefListener().subscribe(data => {
      if (data && data.tag && data.tag.id) {
        if (data.tag.ndefMessage) {
            console.log('NFC Tag found');
            let payload = data.tag.ndefMessage[0].payload;
            let tagContent = this.nfc.bytesToString(payload).substring(3);
            console.log(tagContent);
            // tslint:disable-next-line:max-line-length
//            this.launch('https://lihi.cc/drKF5', tagContent, '_self');
            this.router.navigate(['/crdetail', {tag: tagContent, url: this.url, emplno: this.EMPLNO}]);
//            this.router.navigateByUrl('crdetail');

        } else {
          this.presentAlert('NFC感應','NFC感應失敗');
          console.log('NFC not found');
        }
      }
    });
  }

  public launch(url, tag_content, opentype) {
    this.plt.ready().then(() => {
      if (this.OrgAPIURL2 === '') {
        this.OrgAPIURL2 = url;
      }
      // tslint:disable-next-line:max-line-length
      this.OrgAPIURL2 = this.OrgAPIURL2.replace('MECH/MECH000M', 'MECH/MECH003M_CK') + '?lc_code=' + tag_content + '&user_id=' + this.EMPLNO ;
      // tslint:disable-next-line: max-line-length
      // this.OrgAPIURL2 = this.OrgAPIURL2.replace('MECH/MECH000M', 'MECH/MECH003M') + '?m_device_code=AP1-1401&m_device_name=1.%E5%99%B4%E7%A0%82%E6%A9%9F' ;
      console.log('lauch url:', this.OrgAPIURL2);
      const browser = this.iab.create(this.OrgAPIURL2, opentype, {location: 'no'});
      browser.show();

    });

  }

  async presentAlert(arg_header: string, arg_message: string) {
    const alert = await this.alertController.create({
      header: 'Alert',
      subHeader: arg_header,
      message: arg_message ,
      buttons: ['OK']
    });
    await alert.present();
  }

}
