// React context helpers.
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


export const useAuth = () => {

  const context =
    useContext(
      AuthContext
    );

  const [loading,
    setLoading
  ] = useState(false);

  if (!context) {

    throw new Error(
      "useAuth must be used within AuthProvider"
    );
  }

  const login = async (

    email: string,

    password: string

  ) => {

    try {

      setLoading(true);

      const result =
        await authService.login(

          email,

          password
        );

      context.loginUser(
        result.access
      );

      return result;

    } finally {

      setLoading(false);
    }
  };

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

    logout
  };
};