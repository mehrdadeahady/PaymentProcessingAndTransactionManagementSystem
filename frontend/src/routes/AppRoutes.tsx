// Router components.
import {

  Routes,

  Route,

  Navigate

} from "react-router-dom";

// Auth hook.
import {
  useAuth
} from "../hooks/useAuth";

// Route guard.
import ProtectedRoute from
  "../components/ProtectedRoute";

// Pages.
import LoginPage from
  "../pages/LoginPage";

import RegisterPage from
  "../pages/RegisterPage";

import DashboardPage from
  "../pages/DashboardPage";

import TransferPage from
  "../pages/TransferPage";


export default function AppRoutes() {

  const {
    isAuthenticated
  } = useAuth();

  return (

    <Routes>

      <Route

        path="/"

        element={

          isAuthenticated

            ? (

                <Navigate

                  to="/dashboard"

                  replace

                />

              )

            : (

                <Navigate

                  to="/login"

                  replace

                />

              )
        }

      />

      <Route

        path="/login"

        element={
          <LoginPage />
        }

      />

      <Route

        path="/register"

        element={
          <RegisterPage />
        }

      />

      <Route

        path="/dashboard"

        element={

          <ProtectedRoute>

            <DashboardPage />

          </ProtectedRoute>

        }

      />

      <Route

        path="/transfer"

        element={

          <ProtectedRoute>

            <TransferPage />

          </ProtectedRoute>

        }

      />

      <Route

        path="*"

        element={

          <Navigate

            to="/"

            replace

          />

        }

      />

    </Routes>
  );
}