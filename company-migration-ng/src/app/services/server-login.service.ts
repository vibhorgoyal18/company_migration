import {Injectable} from '@angular/core';
import {HttpService} from './httpRequests.service';
import {ServerLoginRequestModel, ServerType} from '../models/serverLogin.model';
import {ToastrService} from 'ngx-toastr';
import {ApiResponseModel} from '../models/apiResponseModel';
import {ServerAuthResponseModel} from '../models/serverAuthResponse.model';
import {sha256} from 'js-sha256';
import {ServerInfoModel} from '../models/serverInfo.model';

@Injectable()
export class ServerLoginService {

  constructor(
    private httpService: HttpService,
    private toastrService: ToastrService
  ) {
  }

  login = (serverLoginData: ServerLoginRequestModel) => new Promise<ServerAuthResponseModel>((resolve, reject) => {
    serverLoginData.password = sha256.hex(serverLoginData.password);
    serverLoginData.type = serverLoginData.type === ServerType.source ? 'source' : 'target';
    this.httpService.post('api/auth-server',
      serverLoginData,
      null,
      {'Content-Type': 'application/json', Accept: 'application/json'}
    )
      .then((data: ApiResponseModel<ServerAuthResponseModel>) => {
        resolve(data.data);
      })
      .catch((error) => {
        reject(error);
      });
  });

  getServerInfo = () => new Promise<ServerInfoModel>(((resolve, reject) => {
    this.httpService.get('api/server-info',
      null,
      {'Content-Type': 'application/json', Accept: 'application/json'}).then(
      (data: ApiResponseModel<ServerInfoModel>) => {
        resolve(data.data);
      })
      .catch((error) => {
        reject(error);
      });
  }));
}
