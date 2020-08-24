import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { formatDate } from '@angular/common';
import { AlertController } from '@ionic/angular';

@Injectable({
  providedIn: 'root'
})
export class CrapiService {

  constructor(private http: HttpClient, private alertController: AlertController) { }

  today = formatDate(new Date(), 'yyyyMMdd', 'en');
  url = '';

  getDetails(tagContent, arg_url, emplno, deptno): Observable<any> {
    this.url = arg_url;
    console.log('getDetails deptno:', deptno)
    // tslint:disable-next-line:max-line-length
    return this.http.get(`${this.url}OracleAPI_MECH003M/?location_code=` + tagContent + `&ck_date=` + this.today + `&emplno=` + emplno + `&deptno=` + deptno );
  }

  postDetails(data) {
    // 特別備註 Django 中,只針對 application/x-www-form-urlencoded body 內容會有反應,其他都不會
    // 此問題困擾足足一天 紀錄於 2019/08/12 By TinyYu
    let headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    let options = {
      headers
    };

    console.log('POST DETAIL DATA:', data);
    console.log('post start');
    this.http.post(`${this.url}OracleAPI_POSTMECH003M/`, data, options).subscribe( res => {
       console.log(res);
       console.log(res[0]);
       this.presentAlert('點檢確認', '點檢確認成功');
    }, (err) => { this.presentAlert('資料寫入錯誤', '資料無法寫入.(請洽 資訊 喻士正 8226)'); });
  }


  postImages(data) {
    let headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });
    let options = {
      headers
    };

    console.log('image01=', data);
    this.http.post(`${this.url}OracleAPI_POSTIMAGES/`, data, options).subscribe( res => {
    }, (err) => { this.presentAlert('圖片上傳', '圖片上傳失敗(請洽 資訊 喻士正 8226)'); });
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
