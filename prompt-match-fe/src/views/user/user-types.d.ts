interface UserBase {
  username: string
}

interface UserLoginForm extends UserBase {
  password: string
}

interface UserLoginedInfo extends UserBase {
  access_token: string;
  token_type: string;
  role: string;
  last_login_time: Date;
  create_time: Date;
  id: number;
}

export {
  UserLoginForm,
  UserLoginedInfo
}
