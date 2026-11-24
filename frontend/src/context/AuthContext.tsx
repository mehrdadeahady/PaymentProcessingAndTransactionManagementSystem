// React context utilities.
import {

  createContext,

  useState,

  ReactNode

} from "react";


// Context contract.
interface AuthContextType {

  // JWT token.
  token:
    string | null;

  // Logged-in state.
  isAuthenticated:
    boolean;

  // Save token.
  loginUser:
    (
      token: string
    ) => void;

  // Remove token.
  logoutUser:
    () => void;
}


// Create Auth Context.
export const AuthContext =
  createContext<AuthContextType>(
    {} as AuthContextType
  );


// Provider properties.
interface ProviderProps {

  children:
    ReactNode;
}


/**
 * Auth provider.
 *
 * Wraps entire app.
 *
 * Provides:
 *
 * - JWT state
 * - Login state
 * - Logout behavior
 */
export const AuthProvider = (

  {
    children
  }: ProviderProps

) => {

  // Initial token.
  const initialToken =
    localStorage.getItem(
      "access_token"
    );

  // State.
  const [token,
    setToken
  ] = useState<
    string | null
  >(initialToken);

  /**
   * Login.
   */
  const loginUser =
    (
      accessToken: string
    ) => {

      localStorage.setItem(

        "access_token",

        accessToken
      );

      setToken(
        accessToken
      );
    };

  /**
   * Logout.
   */
  const logoutUser =
    () => {

      localStorage.removeItem(
        "access_token"
      );

      localStorage.removeItem(
        "refresh_token"
      );

      setToken(null);
    };

  return (

    <AuthContext.Provider

      value={{

        token,

        isAuthenticated:
          Boolean(token),

        loginUser,

        logoutUser
      }}

    >
      {children}

    </AuthContext.Provider>
  );
};