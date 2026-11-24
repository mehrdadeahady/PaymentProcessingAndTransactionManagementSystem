// React state management.
import {
  useState
} from "react";

// React Router navigation.
import {
  useNavigate,
  Link
} from "react-router-dom";

// Material UI components.
import {

  Container,

  Paper,

  Typography,

  TextField,

  Button,

  Alert,

  Box

} from "@mui/material";

// Authentication hook.
import {
  useAuth
} from "../hooks/useAuth";


/**
 * Login page.
 *
 * Responsibilities:
 *
 * - Authenticate user
 * - Store JWT tokens
 * - Redirect to dashboard
 */
export default function LoginPage() {

  // Router navigation.
  const navigate =
    useNavigate();

  // Auth hook.
  const {
    login,
    loading
  } = useAuth();

  // Email field.
  const [email,
    setEmail
  ] = useState("");

  // Password field.
  const [password,
    setPassword
  ] = useState("");

  // Error message.
  const [error,
    setError
  ] = useState("");

  /**
   * Handle login form.
   */
  const handleSubmit =
    async (
      event: React.FormEvent
    ) => {

      // Prevent page refresh.
      event.preventDefault();

      // Clear previous errors.
      setError("");

      try {

        // Authenticate user.
        await login(
          email,
          password
        );

        // Navigate to dashboard.
        navigate(
          "/dashboard"
        );

      } catch {

        setError(
          "Invalid email or password."
        );
      }
    };

  return (

    <Container
      maxWidth="sm"
    >

      <Paper

        sx={{

          mt: 8,

          p: 4
        }}

      >

        <Typography

          variant="h4"

          gutterBottom

        >
          FinTech Wallet
        </Typography>

        <Typography
          color="text.secondary"
        >
          Sign in to your account
        </Typography>

        {
          error && (

            <Alert

              severity="error"

              sx={{
                mt: 2
              }}

            >
              {error}
            </Alert>
          )
        }

        <Box

          component="form"

          onSubmit={
            handleSubmit
          }

          sx={{
            mt: 3
          }}

        >

          <TextField

            fullWidth

            required

            margin="normal"

            label="Email"

            value={email}

            onChange={(event) =>
              setEmail(
                event.target.value
              )
            }

          />

          <TextField

            fullWidth

            required

            type="password"

            margin="normal"

            label="Password"

            value={password}

            onChange={(event) =>
              setPassword(
                event.target.value
              )
            }

          />

          <Button

            fullWidth

            type="submit"

            variant="contained"

            disabled={loading}

            sx={{
              mt: 3
            }}

          >
            Login
          </Button>

        </Box>

        <Box
          sx={{
            mt: 2
          }}
        >

        