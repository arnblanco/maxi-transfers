export interface UserToken {
  access_token: string;
  refresh_token: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserRegister {
  first_name: string;
  last_name: string;
  email: string;
  username: string;
  password: string;
}
