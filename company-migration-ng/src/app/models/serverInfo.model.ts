export interface Source {
  server: string;
  user: string;
}

export interface Target {
  server: string;
  user: string;
}

export interface ServerInfoModel {
  source: Source;
  target: Target;
}
