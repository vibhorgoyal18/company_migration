export interface ServerLoginRequestModel {
  username: string;
  password: string;
  'base_url': string;
  type: any;
}

export enum ServerType {
  source, target
}
