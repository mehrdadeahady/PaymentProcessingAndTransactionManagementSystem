// Shared HTTP client.
import api from "../api/axios";

// Authentication types.
import type {

  LoginResponse,

  RegisterRequest

} from "../types/auth";


/**
 * Authentication service.
 *
 * Responsibilities:
 *
 * - Login
 * - Register
 * - Logout
 * - Token storage
 *
 * Keeps authentication logic
 * out of React pages.
 */
class AuthService {

  /**
   * Login user.
   */
  async login(

    email: string,

    password: string

  ): Promise<LoginResponse> {

    // Request JWT tokens.
    const response =
      await api.post(

        "/api/token/",

        {
          email,
          password
        }
      );

    // Store tokens.
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

  /**
   * Register account.
   */
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

  /**
   * Logout user.
   */
  logout(): void {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "refresh_token"
    );
  }

  /**
   * Check authentication state.
   */
  isAuthenticated(): boolean {

    return Boolean(
      localStorage.getItem(
        "access_token"
      )
    );
  }

  /**
   * Get access token.
   */
  getAccessToken():
  string | null {

    return localStorage.getItem(
      "access_token"
    );
  }

  /**
   * Get refresh token.
   */
  getRefreshToken():
  string | null {

    return localStorage.getItem(
      "refresh_token"
    );
  }
}


// Singleton instance.
const authService =
  new AuthService();

export default authService;