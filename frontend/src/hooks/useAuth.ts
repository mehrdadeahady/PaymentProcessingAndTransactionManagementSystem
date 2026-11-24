// React context utilities.
import {

  useContext,

  useState

} from "react";

// Auth context.
import {

  AuthContext

} from "../context/AuthContext";

// Auth service.
import authService from
  "../services/authService";


/**
 * Authentication hook.
 *
 * Responsibilities:
 *
 * - Login
 * - Logout
 * - Auth state
 * - Loading state
 *
 * Components should use
 * this hook instead of
 * talking directly to
 * AuthContext.
 */
export const useAuth = () => {

  // Load auth context.
  const context =
    useContext(
      AuthContext
    );

  // Request state.
  const [loading,
    setLoading
  ] = useState(false);

  /**
   * Login user.
   */
  const login = async (

    email: string,

    password: string

  ) => {

    try {

      setLoading(true);

      // Authenticate.
      const result =
        await authService.login(

          email,

          password
        );

      // Update context.
      context.loginUser(
        result.access
      );

      return result;

    } finally {

      setLoading(false);
    }
  };

  /**
   * Logout user.
   */
  const logout = () => {

    authService.logout();

    context.logoutUser();
  };

  return {

    token:
      context.token,

    isAuthenticated:
      context.isAuthenticated,

    loading,

    login,

    logout,
  };
};