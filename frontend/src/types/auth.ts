// Authentication token response.
export interface LoginResponse {

  // JWT access token.
  access: string;

  // JWT refresh token.
  refresh: string;
}


// Register request payload.
export interface RegisterRequest {

  // User email.
  email: string;

  // Username.
  username: string;

  // Account password.
  password: string;
}