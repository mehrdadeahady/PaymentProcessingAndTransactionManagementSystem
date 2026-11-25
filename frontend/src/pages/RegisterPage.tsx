// React state.
import {
  useState
} from "react";

// Router navigation.
import {
  useNavigate,
  Link
} from "react-router-dom";

// Material UI.
import {

  Container,

  Paper,

  Typography,

  TextField,

  Button,

  Alert,

  Box

} from "@mui/material";

// Auth service.
import authService from
  "../services/authService";


export default function RegisterPage() {

  const navigate =
    useNavigate();

  const [email,
    setEmail
  ] = useState("");

  const [username,
    setUsername
  ] = useState("");

  const [password,
    setPassword
  ] = useState("");

  const [success,
    setSuccess
  ] = useState("");

  const [error,
    setError
  ] = useState("");

  const handleSubmit =
    async (
      event:
      React.FormEvent
    ) => {

      event.preventDefault();

      setError("");

      setSuccess("");

      try {

        await authService.register({

          email,

          username,

          password
        });

        setSuccess(
          "Account created successfully."
        );

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

            type="email"

            value={email}

            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }

          />

          <TextField

            fullWidth

            required

            margin="normal"

            label="Username"

            value={username}

            onChange={(e) =>
              setUsername(
                e.target.value
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

            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }

          />

          <Button

            type="submit"

            fullWidth

            variant="contained"

            sx={{
              mt: 3
            }}

          >
            Register
          </Button>

        </Box>

      </Paper>

    </Container>
  );
}