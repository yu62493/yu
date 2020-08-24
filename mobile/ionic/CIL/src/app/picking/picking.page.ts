import { Component, OnInit } from '@angular/core';
import { BarcodeScanner } from '@ionic-native/barcode-scanner/ngx';
import { formatDate } from '@angular/common';
import { PickingapiService } from '../services/pickingapi.service';
import { Storage } from '@ionic/storage';
import { CILData } from './CIL';

@Component({
  selector: 'app-picking',
  templateUrl: './picking.page.html',
  styleUrls: ['./picking.page.scss'],
})
export class PickingPage implements OnInit {

  MTL_NO: string;
  QRCodeText: string;
  TAKE_QTY: number;
  webdata = '';
  today = formatDate(new Date(), 'yyyyMMdd', 'en');
  time = formatDate(new Date(), 'HHmmss', 'en');
  url = '';

  constructor(private barcodeScanner: BarcodeScanner, private pickingapi: PickingapiService, private storage: Storage) { }

  ngOnInit() {
    this.getURL();
    this.TAKE_QTY = 1;
  }

  QRScan() {
    this.barcodeScanner.scan().then(barcodeData => {
      // success. barcodeData is the data returned by scanner
      console.log(barcodeData);
      this.QRCodeText = barcodeData.text.replace(/"/g , ' ');
      this.QRCodeText = this.QRCodeText.replace(/'/g , '"');
//      this.QRCodeText = barcodeData.text;
      const QRContent: CILData = JSON.parse(this.QRCodeText);
      console.log(QRContent);
      console.log('MTL_NO', QRContent.MATERIAL_ID);
      this.MTL_NO = QRContent.MATERIAL_ID;

    }).catch(err => {
      // error
      console.log(err);
    });
  }

  private getURL(){
    this.storage.ready().then(() => {
      this.storage.get('OrgAPIURL').then((val) => {
        console.log('OrgAPIURL val:', val);
        this.url = val;
      });
    });
  }

  sendPostRequest() {
    console.log('QRContent:', this.QRCodeText);
    // tslint:disable-next-line:max-line-length
    this.webdata = 'TAKE_DATE=' + this.today + '&TAKE_TIME=' + this.time + '&MTL_NO=' + this.MTL_NO + '&TAKE_QTY=' + this.TAKE_QTY + '&WORK_NO1=' + '&REMARK=' + this.QRCodeText ;
    this.pickingapi.postDetails(this.url, this.webdata);
  }


}
