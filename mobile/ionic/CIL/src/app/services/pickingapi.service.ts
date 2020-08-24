import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { formatDate } from '@angular/common';
import { AlertController } from '@ionic/angular';
import { ToastController } from '@ionic/angular';

@Injectable({
  providedIn: 'root'
})
export class PickingapiService {

  // tslint:disable-next-line:max-line-length
  constructor(private http: HttpClient, private alertController: AlertController, public toastController: ToastController) { }
  url = '';

  // tslint:disable-next-line:variable-name
  async presentToast( arg_str: string ) {
    const toast = await this.toastController.create({
      message: arg_str,
      duration: 2000,
      position: 'top',
      color: 'danger'
    });
    toast.present();
  }

  postDetails(arg_url , data) {
    let headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    let options = {
      headers
    };

    this.url = arg_url;
    console.log('POST DETAIL DATA:', data);
    this.http.post(`${this.url}RestCILAPI_POSTCILA030M/`, data, options).subscribe( res => {
        console.log(res);
        this.presentToast('更新成功');
        },
        (err) => { console.log('post err', err); this.presentToast('更新失敗:' + err.message);
    });
  }

}
