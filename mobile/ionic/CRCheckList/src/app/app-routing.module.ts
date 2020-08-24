import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'home', loadChildren: './home/home.module#HomePageModule' },
  { path: 'register', loadChildren: './auth/register/register.module#RegisterPageModule' },
  { path: 'login', loadChildren: './auth/login/login.module#LoginPageModule' },
  { path: 'cr-login', loadChildren: './CR/cr-login/cr-login.module#CrLoginPageModule' },
  { path: 'cr-nfc', loadChildren: './cr-nfc/cr-nfc.module#CrNfcPageModule' },
  { path: 'crdetail', loadChildren: './CR/crdetail/crdetail.module#CRDetailPageModule' },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
