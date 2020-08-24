import { Component, OnInit } from '@angular/core';
import { CrapiService } from '../services/crapi.service';
import { formatDate } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router';
import { Camera, CameraOptions } from '@ionic-native/camera/ngx';

@Component({
  selector: 'app-crdetail',
  templateUrl: './crdetail.page.html',
  styleUrls: ['./crdetail.page.scss'],
})
export class CRDetailPage implements OnInit {

  tagContent = this.route.snapshot.params.tag;
  url = this.route.snapshot.params.url;
  emplno = this.route.snapshot.params.EMPLNO;
  deptno = this.route.snapshot.params.DEPTNO;
  webdata = '';
  ckdata = [];
  today = formatDate(new Date(), 'yyyyMMdd', 'en');
  time = formatDate(new Date(), 'HHmmss', 'en');
  tt = '';

  // tslint:disable-next-line:max-line-length
  tagArray = ['AP1-1401', 'AP1-1402', 'AP1-1403', 'AP1-1404', 'AP1-1405', 'AP1-1406', 'AP1-1407', 'AP1-1408', 'AP1-1409', 'AP1-1410', 'AP1-1411', 'AP1-1412'];
//  tagArray = ['AP1-140101', 'AP1-140201', 'AP1-140301', 'AP1-140401', 'AP1-140501', 'AP1-140601', 'AP1-140701', 'AP1-140801', 'AP1-140901', 'AP1-141001', 'AP1-141101', 'AP1-141201'];

  capturedSnapURL = [];
  base64Image = [];
  cameraOptions: CameraOptions = {
    quality: 20,
    destinationType: this.camera.DestinationType.DATA_URL,
    encodingType: this.camera.EncodingType.JPEG,
    mediaType: this.camera.MediaType.PICTURE
  }


// 由 cr-nfc router navigate過來 發現 ngOnInIt 不一定會有反應
  // 改由此處處理 正常運作中 2019/09/03 TinyYu
  constructor(private crapi: CrapiService, private route: ActivatedRoute, private router: Router, private camera: Camera) { 
    route.params.subscribe(val => {
      // put the code from `ngOnInit` here
      this.time = formatDate(new Date(), 'HHmmss', 'en');
      this.searchChanged();
    });
  }

  ngOnInit() {
    console.log('crdetail init');
//    this.searchChanged();
    console.log('crdetail url:', this.url);
    console.log('crdetail emplno:', this.emplno);
    console.log('crdetail deptno:', this.deptno);
  }

  searchChanged() {
    // Call our service function which returns an Observable
    console.log('hi api test start');
    console.log('tag id:', this.route.snapshot.params.tag);

    this.crapi.getDetails(this.tagContent, this.url, this.emplno, this.deptno).subscribe( result => {
      result.forEach( (myObject) => {
         console.log('device_code:', myObject.DEVICE_CODE);
         myObject.CK_DATE = this.today;
         myObject.CK_TIME = this.time;
         console.log('ABCDEFG TIME:', this.time);
         if (myObject.CK_RESULT === 'Y') {
           myObject.CK_RESULT = true;
         } else {
           myObject.CK_RESULT = false;
         }
      });
      this.ckdata = result;
      if (result.length === 0){
        this.tt = '沒有被授權的項目,請查明後進行';
      }

      console.log('this.ckdata:', this.ckdata);
    });
    console.log('api test end');
  }


  takeSnap(idx) {
    this.camera.getPicture(this.cameraOptions).then((imageData) => {
      // this.camera.DestinationType.FILE_URI gives file URI saved in local
      // this.camera.DestinationType.DATA_URL gives base64 URI
      this.base64Image[idx] = imageData;
      this.capturedSnapURL[idx] = 'data:image/jpeg;base64,' +  this.base64Image[idx];
    }, (err) => {
      console.log(err);
      // Handle error
    });
  }

  sendPostRequest(idx) {
    console.log('SEND POST CKDATA :', this.ckdata);
    this.webdata = Object.keys(this.ckdata[idx]).map(key => key + '=' + this.ckdata[idx][key]).join('&');
    console.log(Object.keys(this.ckdata[idx]));
    console.log('LOCATION_CODE=', this.ckdata[idx].LOCATION_CODE);
    this.crapi.postDetails(this.webdata);
    // 透過 encodeURIComponent 將 + 轉換 避免透過http 傳送時 被消失
    // 導致 base64 字串轉回時 圖片錯誤
    // By TinyYu 2020/02/13
    if (this.base64Image[idx] !== '') {
      // tslint:disable-next-line:max-line-length
      this.crapi.postImages('LOCATION_CODE=' + this.ckdata[idx].LOCATION_CODE + '&' + 'CK_DATE=' + this.ckdata[idx].CK_DATE + '&' + 'CK_TIME=' + this.ckdata[idx].CK_TIME + '&' + 'MAINT_USER=' + this.ckdata[idx].MAINT_USER + '&' +  'IMAGE01=' + encodeURIComponent(this.base64Image[idx]));
    }
//    this.router.navigate(['/cr-nfc', { DEVICE_NAME: this.ckdata[idx].DEVICE_NAME, CK_LOCATION: this.ckdata[idx].CK_LOCATION }]);
  }

}
