export interface Cookies {
  aUTH_TYPE: string;
  fAREYE_CMP_ID: string;
  fAREYE_EMP_CODE: string;
  jSESSIONID: string;
  'xSRF-TOKEN': string;
  'remember-me': string;
}

export interface ServerAuthResponseModel {
  statusCode: number;
  cookies: Cookies;
  user: string;
  body?: any;
}
