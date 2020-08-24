import { Component, OnInit } from '@angular/core';
import { Platform } from '@ionic/angular';
import { NFC, Ndef } from '@ionic-native/nfc/ngx';
import { Storage } from '@ionic/storage';
import { AlertController } from '@ionic/angular';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-cr-nfc',
  templateUrl: './cr-nfc.page.html',
  styleUrls: ['./cr-nfc.page.scss'],
})
export class CrNfcPage implements OnInit {
  url = '';
  OrgAPIURL2 = '';
  EMPLNO = '';
  DEPTNO = '';
  tagContent = '';
  DEVICE_NAME = this.route.snapshot.params.DEVICE_NAME;
  CK_LOCATION = this.route.snapshot.params.CK_LOCATION;
  myListener ;

  // tslint:disable-next-line:max-line-length
  constructor(private nfc: NFC, private ndef: Ndef, private storage: Storage,
              private plt: Platform, private alertController: AlertController, private router: Router,
              private route: ActivatedRoute ) {
      this.plt.ready().then(() => {
      console.log('PLT ready');
      this.cekNFC();
      });
      route.params.subscribe(val => {
        // put the code from `ngOnInit` here
        this.cekNFC();
      });

   }

  ngOnInit() {
    this.getParam();
  }

  private getParam(){
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
      this.storage.get('DEPTNO').then((val) => {
        console.log('DEPTNO val:', val);
        this.DEPTNO = val;
      });
    });
  }


  cekNFC() {
    this.nfc.enabled().then(() => {
      console.log('call NFC');
      this.listenToNdef();
    }).catch(err => {
      console.log('cekNFC err', err);
    });
  }

  listenToNdef() {
    console.log('listenToNdef start');
    this.myListener = this.nfc.addNdefListener().subscribe(data => {
      if (data && data.tag && data.tag.id) {
        if (data.tag.ndefMessage) {
            console.log('NFC Tag found');
            let payload = data.tag.ndefMessage[0].payload;
            this.tagContent = this.nfc.bytesToString(payload).substring(3);
            console.log('decoded tag id', this.nfc.bytesToHexString(data.tag.id));
            console.log('payload:', this.nfc.bytesToHexString(payload));
            console.log(this.tagContent);
            this.router.navigate(['/crdetail', {tag: this.tagContent, url: this.url, EMPLNO: this.EMPLNO, DEPTNO: this.DEPTNO}]);
            this.myListener.unsubscribe();
        } else {
          this.presentAlert('NFC感應','NFC感應失敗');
          console.log('NFC not found');
        }
      }
    }, (err) => { this.presentAlert('NFC感應','NFC感應失敗'); });
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
