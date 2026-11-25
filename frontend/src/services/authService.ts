// Shared API client.
import api from "../api/axios";

// Auth types.
import type {

  LoginResponse,

  RegisterRequest

} from "../types/auth";


class AuthService {

  async login(

    email: string,

    password: string

  ): Promise<LoginResponse> {

    const response =
      await api.post(

        "/api/accounts/login/",

        {
          email,
          password
        }
      );

    localStorage.setItem(

      "access_token",

      response.data.access
    );

    localStorage.setItem(

      "refresh_token",

      response.data.refresh
    );

    return response.data;
  }

  async register(

    payload: RegisterRequest

  ) {

    const response =
      await api.post(

        "/api/accounts/register/",

        payload
      );

    return response.data;
  }

  logout(): void {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "refresh_token"
    );
  }

  isAuthenticated(): boolean {

    return Boolean(
      localStorage.getItem(
        "access_token"
      )
    );
  }

  getAccessToken():

  string | null {

    return localStorage.getItem(
      "access_token"
    );
  }

  getRefreshToken():

  string | null {

    return localStorage.getItem(
      "refresh_token"
    );
  }
}

const authService =
  new AuthService();

export default authService;