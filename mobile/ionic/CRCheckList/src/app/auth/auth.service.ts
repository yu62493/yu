import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { Observable, BehaviorSubject } from 'rxjs';

import { Storage } from '@ionic/storage';
import { User } from './user';
import { AuthResponse } from './auth-response';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private httpClient: HttpClient, private storage: Storage) { }

  AUTH_SERVER_ADDRESS = '';
  authSubject  = new BehaviorSubject(false);
  keyval = '';

  login(user: User, AUTH_SERVER_ADDRESS): Observable<AuthResponse> {
    return this.httpClient.post(`${AUTH_SERVER_ADDRESS}tinytest_emplno/?emplno=` + user.emplno + '&password=' + user.password , user).pipe(
      tap((res: AuthResponse) => {
        console.log(res);
        if (res.user) {
          this.storage.set('EMPLNO', res.user[0].emplno);
          this.storage.set('DEPTNO', res.user[0].deptno);
          this.authSubject.next(true);
        } else {
          this.storage.set('EMPLNO', '');
          this.storage.set('DEPTNO', '');
        }
      })
    );
  }


}
