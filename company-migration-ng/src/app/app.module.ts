import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {ServerLoginComponent} from './modules/server-login/server-login.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AppRoutingModule} from './app-routing.module';
import {HttpClientModule} from '@angular/common/http';
import {HeaderComponent} from './components/header/header.component';
import {MatCardModule} from '@angular/material/card';
import {MatInputModule} from '@angular/material/input';
import {FormsModule} from '@angular/forms';
import {MatButtonModule} from '@angular/material/button';
import {HttpService} from './services/httpRequests.service';
import {ServerLoginService} from './services/server-login.service';
import {ToastrModule} from 'ngx-toastr';
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';
import {CreateCompanyComponent} from './modules/create-company/create-company.component';
import {CheckOptionsComponent} from './modules/check-options/check-options.component';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {CookieModule} from 'ngx-cookie';
import {MigrationService} from './services/migration.service';
import { VerifyDetailsComponent } from './modules/verify-details/verify-details.component';
import { MigrateComponent } from './modules/migrate/migrate.component';
import {MatIconModule} from '@angular/material/icon';
import {FontAwesomeModule} from '@fortawesome/angular-fontawesome';
import {NgxTimerModule} from "ngx-timer";

@NgModule({
  declarations: [
    AppComponent,
    ServerLoginComponent,
    HeaderComponent,
    CreateCompanyComponent,
    CheckOptionsComponent,
    VerifyDetailsComponent,
    MigrateComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    MatCardModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    ToastrModule.forRoot({
      timeOut: 500000,
      positionClass: 'toast-top-right'
    }),
    MatSnackBarModule,
    MatCheckboxModule,
    CookieModule.forRoot(),
    MatIconModule,
    FontAwesomeModule,
    NgxTimerModule
  ],
  providers: [
    HttpService,
    ServerLoginService,
    MigrationService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
