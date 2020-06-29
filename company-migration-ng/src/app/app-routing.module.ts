import {ModuleWithProviders} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {ServerLoginComponent} from './modules/server-login/server-login.component';
import {CreateCompanyComponent} from './modules/create-company/create-company.component';
import {CheckOptionsComponent} from './modules/check-options/check-options.component';
import {VerifyDetailsComponent} from './modules/verify-details/verify-details.component';
import {MigrateComponent} from './modules/migrate/migrate.component';

const routes: Routes = [
  {
    path: 'server-auth',
    component: ServerLoginComponent
  },
  {
    path: 'check-options',
    component: CheckOptionsComponent
  },
  {
    path: 'create-company',
    component: CreateCompanyComponent
  },
  {
    path: 'verify-details',
    component: VerifyDetailsComponent
  },
  {
    path: 'migrate',
    component: MigrateComponent
  },
  {
    path: '**',
    pathMatch: 'full',
    redirectTo: 'server-auth'
  }
];

export const AppRoutingModule: ModuleWithProviders = RouterModule.forRoot(routes, {useHash: true});
