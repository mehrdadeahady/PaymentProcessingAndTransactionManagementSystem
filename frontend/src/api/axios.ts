// HTTP client library.
import axios from "axios";


// Create shared API instance.
const api = axios.create({

  // Django API base URL.
  baseURL:
    import.meta.env.VITE_API_URL,

  // Request timeout.
  timeout: 30000,
});


// Add JWT token automatically.
api.interceptors.request.use(

  (config) => {

    // Read token from browser storage.
    const token =
      localStorage.getItem(
        "access_token"
      );

    // Attach Authorization header.
    if (
      token &&
      config.headers
    ) {

      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  }
);


// Global response handling.
api.interceptors.response.use(

  // Successful response.
  (response) => response,

  // Failed response.
  (error) => {

    // Unauthorized.
    if (
      error.response?.status === 401
    ) {

      // Remove stale token.
      localStorage.removeItem(
        "access_token"
      );

      localStorage.removeItem(
        "refresh_token"
      );
    }

    return Promise.reject(
      error
    );
  }
);


// Export HTTP client.
export default api;