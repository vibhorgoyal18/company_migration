import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {Router} from '@angular/router';
import {ToastrService} from 'ngx-toastr';


@Injectable()
export class HttpService {

  constructor(private httpClient: HttpClient,
              private router: Router,
              private toastrService: ToastrService
  ) {
  }

  private httpHeader(): any {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        return {
          Accept: '*/*',
        };
      } else {
        return {
          Accept: '*/*'
        };
      }
    } catch (err) {
      console.error(err);
    }
  }

  get = (uri: string, params = {}, headers?: any) => new Promise((resolve, reject) => {
    this.httpClient.get(environment.apiBaseURL + uri, {
      headers: {...this.httpHeader(), ...headers},
      params,
    }).subscribe(
      (response: any) => {
        resolve(response);
      },
      error => {
        reject(error);
      });
  });

  post = (uri: string, body: any, params = {}, headers?: any) => new Promise((resolve, reject) => {
    this.httpClient.post(environment.apiBaseURL + uri, body, {
      headers: {...this.httpHeader(), ...headers},
      params,
    }).subscribe(
      (response: HttpResponse<any>) => {
        resolve(response);
      },
      error => {
        reject(error);
      }
    );
  });
}
