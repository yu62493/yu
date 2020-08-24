import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { Storage } from '@ionic/storage';
import { AuthService } from '../auth.service';
import { GlobalParamService } from '../global-param.service';

// tsconfig.json 要先設定  "resolveJsonModule": true,
import * as data from '../../data.json';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  // tslint:disable-next-line:max-line-length
  constructor(private ApiURL: GlobalParamService, private authService: AuthService,
              private router: Router, private alertController: AlertController, private storage: Storage) { }

  GlobalParam: any = (data as any).default;

  OrgAPIURL = '';
  APPshortURL = '';

  ngOnInit() {
    this.APPshortURL = this.GlobalParam[0].shotURL;
    this.ApiURL.tran_shortURL(this.APPshortURL, 'OrgAPIURL');
    this.get_URL();
  }

  login(form){
    this.authService.login(form.value, this.OrgAPIURL).subscribe((res) => {
      this.router.navigateByUrl('home');
    }, (err) => { this.presentAlert(err); });
  }

  async sleep(time : number): Promise<void> {
    return new Promise<void>((res, rej) => {
        setTimeout(res, time);
    });
  }

  async get_URL() {
    await this.sleep(2000);
    this.storage.ready().then(() => {
      this.storage.get('OrgAPIURL').then((val) => {
        console.log('OrgAPIURL val:', val);
        this.OrgAPIURL = val;
      } );
    });
  }

  async presentAlert( argdes: string) {
    const alert = await this.alertController.create({
      header: 'Alert',
      subHeader: '認證錯誤',
      message: argdes + '帳號或密碼錯誤.(或洽 資訊 喻士正 8226)',
      buttons: ['OK']
    });
    await alert.present();
  }

}
