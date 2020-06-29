import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
class DataService {
  // tslint:disable-next-line:variable-name
  private _sourceXSRFToken: string;
  // tslint:disable-next-line:variable-name
  private _sourceCookies: any;
  // tslint:disable-next-line:variable-name
  private _sourceBaseUrl: string;
  // tslint:disable-next-line:variable-name
  private _sourceUser: string;
  // tslint:disable-next-line:variable-name
  private _sourceCompanyId: number;
  // tslint:disable-next-line:variable-name
  private _targetXSRFToken: string;
  // tslint:disable-next-line:variable-name
  private _targetCookies: any;
  // tslint:disable-next-line:variable-name
  private _targetBaseUrl: string;
  // tslint:disable-next-line:variable-name
  private _targetUser: string;
  // tslint:disable-next-line:variable-name
  private _targetCompanyId: number;

  get targetCompanyId(): number {
    return this._targetCompanyId;
  }

  set targetCompanyId(value: number) {
    this._targetCompanyId = value;
  }

  get targetUser(): string {
    return this._targetUser;
  }

  set targetUser(value: string) {
    this._targetUser = value;
  }

  get targetBaseUrl(): string {
    return this._targetBaseUrl;
  }

  set targetBaseUrl(value: string) {
    this._targetBaseUrl = value;
  }

  get targetCookies(): any {
    return this._targetCookies;
  }

  set targetCookies(value: any) {
    this._targetCookies = value;
  }

  get targetXSRFToken(): string {
    return this._targetXSRFToken;
  }

  set targetXSRFToken(value: string) {
    this._targetXSRFToken = value;
  }

  get sourceCompanyId(): number {
    return this._sourceCompanyId;
  }

  set sourceCompanyId(value: number) {
    this._sourceCompanyId = value;
  }

  get sourceUser(): string {
    return this._sourceUser;
  }

  set sourceUser(value: string) {
    this._sourceUser = value;
  }

  get sourceBaseUrl(): string {
    return this._sourceBaseUrl;
  }

  set sourceBaseUrl(value: string) {
    this._sourceBaseUrl = value;
  }

  get sourceCookies(): any {
    return this._sourceCookies;
  }

  set sourceCookies(value: any) {
    this._sourceCookies = value;
  }

  get sourceXSRFToken(): string {
    return this._sourceXSRFToken;
  }

  set sourceXSRFToken(value: string) {
    this._sourceXSRFToken = value;
  }
}
