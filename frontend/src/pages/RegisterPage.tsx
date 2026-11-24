// React state.
import {
  useState
} from "react";

// Router navigation.
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

// Authentication service.
import authService from
  "../services/authService";


/**
 * Registration page.
 *
 * Responsibilities:
 *
 * - Create user account
 * - Create wallet
 * - Redirect to login
 */
export default function RegisterPage() {

  // Router navigation.
  const navigate =
    useNavigate();

  // Form values.
  const [email,
    setEmail
  ] = useState("");

  const [username,
    setUsername
  ] = useState("");

  const [password,
    setPassword
  ] = useState("");

  // Success message.
  const [success,
    setSuccess
  ] = useState("");

  // Error message.
  const [error,
    setError
  ] = useState("");

  /**
   * Register account.
   */
  const handleSubmit =
    async (
      event: React.FormEvent
    ) => {

      // Prevent page refresh.
      event.preventDefault();

      // Clear messages.
      setError("");

      setSuccess("");

      try {

        // Call backend.
        await authService.register({

          email,

          username,

          password
        });

        // Success feedback.
        setSuccess(
          "Account created successfully."
        );

        // Redirect after success.
        setTimeout(

          () => {

            navigate(
              "/login"
            );

          },

          1500
        );

      } catch {

        setError(
          "Registration failed."
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
          Create Account
        </Typography>

        {
          success && (

            <Alert

              severity="success"

              sx={{
                mt: 2
              }}

            >
              {success}
            </Alert>
          )
        }

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

            margin="normal"

            label="Username"

            value={username}

            onChange={(event) =>
              setUsername(
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

            sx={{
              mt: 3
            }}

          >
            Register
          </Button>

        </Box>

        <Typography
          sx={{
            mt: 2
          }}
        >

          Already have an account?

          {" "}

          <Link
            to="/login"
          >
            Login
          </Link>

        </Typography>

      </Paper>

    </Container>
  );
}