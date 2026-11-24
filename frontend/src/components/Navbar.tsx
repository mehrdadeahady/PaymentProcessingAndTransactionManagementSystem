// Material UI components.
import {

  AppBar,

  Toolbar,

  Typography,

  Button,

  Box

} from "@mui/material";

// Router support.
import {
  Link
} from "react-router-dom";

// Authentication hook.
import {
  useAuth
} from "../hooks/useAuth";


/**
 * Application navigation.
 *
 * Shown on all secured pages.
 */
export default function Navbar() {

  // Authentication functions.
  const {
    logout
  } = useAuth();

  return (

    <AppBar
      position="static"
    >

      <Toolbar>

        <Typography

          variant="h6"

          sx={{
            flexGrow: 1
          }}

        >
          FinTech Wallet
        </Typography>

        <Box>

          <Button

            color="inherit"

            component={Link}

            to="/dashboard"

          >
            Dashboard
          </Button>

          <Button

            color="inherit"

            component={Link}

            to="/transfer"

          >
            Transfer
          </Button>

          <Button

            color="inherit"

            onClick={logout}

          >
            Logout
          </Button>

        </Box>

      </Toolbar>

    </AppBar>
  );
}