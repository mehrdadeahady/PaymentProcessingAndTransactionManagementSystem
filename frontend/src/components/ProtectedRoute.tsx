// React node type.
import { ReactNode } from "react";

// Router redirect component.
import {
  Navigate
} from "react-router-dom";

// Authentication hook.
import {
  useAuth
} from "../hooks/useAuth";


// Component properties.
interface ProtectedRouteProps {

  // Wrapped component.
  children: ReactNode;
}


/**
 * Route guard.
 *
 * Prevents access to pages
 * unless user is authenticated.
 *
 * Example:
 *
 * /dashboard
 *
 * /transfer
 */
export default function ProtectedRoute(

  {
    children
  }: ProtectedRouteProps

) {

  // Current auth state.
  const {
    isAuthenticated
  } = useAuth();

  // User not logged in.
  if (!isAuthenticated) {

    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  // User authenticated.
  return <>{children}</>;
}