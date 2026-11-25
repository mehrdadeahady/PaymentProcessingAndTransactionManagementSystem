// React context.
import {

  createContext,

  useState,

  ReactNode

} from "react";


// Auth contract.
interface AuthContextType {

  token:
    string | null;

  isAuthenticated:
    boolean;

  loginUser:
    (
      token: string
    ) => void;

  logoutUser:
    () => void;
}


// Context instance.
export const AuthContext =
  createContext<
    AuthContextType | undefined
  >(undefined);


// Provider properties.
interface ProviderProps {

  children:
    ReactNode;
}


export const AuthProvider = (

  {
    children
  }: ProviderProps

) => {

  const initialToken =
    localStorage.getItem(
      "access_token"
    );

  const [token,
    setToken
  ] = useState<
    string | null
  >(initialToken);

  const loginUser = (
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