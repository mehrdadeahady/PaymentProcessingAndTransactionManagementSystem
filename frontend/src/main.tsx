// React.
import React from "react";

import ReactDOM from
  "react-dom/client";

// Material UI reset.
import {
  CssBaseline
} from "@mui/material";

// Root component.
import App from "./App";

// Auth provider.
import {
  AuthProvider
} from "./context/AuthContext";


ReactDOM.createRoot(

  document.getElementById(
    "root"
  ) as HTMLElement

).render(

  <React.StrictMode>

    <AuthProvider>

      <CssBaseline />

      <App />

    </AuthProvider>

  </React.StrictMode>
);