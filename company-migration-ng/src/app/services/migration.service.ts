import {Injectable} from '@angular/core';
import {HttpService} from './httpRequests.service';
import {ServerLoginRequestModel, ServerType} from '../models/serverLogin.model';
import {ToastrService} from 'ngx-toastr';
import {ApiResponseModel} from '../models/apiResponseModel';
import {ServerAuthResponseModel} from '../models/serverAuthResponse.model';
import {sha256} from 'js-sha256';
import {MigrationOptionsModel} from '../models/migrationOptions.model';
import {Subject} from "rxjs";

@Injectable()
export class MigrationService {

  static migrationOptions: MigrationOptionsModel;
  public timerOption = new Subject<string>();

  constructor(private httpService: HttpService) {
  }

  getMigrationOptionsWithLabel() {
    if (MigrationService.migrationOptions) {
      const migrationOptionsKeys = Object.keys(MigrationService.migrationOptions);
      let migrationOptionsTrueKeys = [];
      for (const migrationOptionKey of migrationOptionsKeys) {
        const migrationOption = migrationOptionKey.replace('isChecked', '');
        let label = '';
        for (const char of migrationOption) {
          if (char.toUpperCase() === char) {
            label += ' ';
          }
          label += char;
        }
        migrationOptionsTrueKeys = [...migrationOptionsTrueKeys, {
          label,
          migrationOptionKey: migrationOption,
          isChecked: MigrationService.migrationOptions[migrationOptionKey]
        }];
      }
      return migrationOptionsTrueKeys;
    }
    return [];
  }

  reAuthServer = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/re-auth-server').then(
      data => resolve(),
      error => reject()
    );
  });

  migrateEnvVariables = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/env-variables').then(
      data => resolve(),
      error => reject()
    );
  });

  migrateUserTypes = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/user-types').then(
      data => resolve(),
      error => reject()
    );
  });

  migrateCompanySettings = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/company-settings').then(
      data => resolve(),
      error => reject()
    );
  });

  publishProcesses = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/publish-processes').then(
      data => resolve(),
      error => reject()
    );
  });

  updatePostHookUrl = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/update-post-url').then(
      data => resolve(),
      error => reject()
    );
  });

  addAndAssignBranchToAdmin = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/assign-default-hub').then(
      data => resolve(),
      error => reject()
    );
  });

  migrateDataStore = () => new Promise<ApiResponseModel<any>>((resolve, reject) => {
    this.httpService.get('api/migrate/datastore').then(
      data => resolve(),
      error => reject()
    );
  });
}
