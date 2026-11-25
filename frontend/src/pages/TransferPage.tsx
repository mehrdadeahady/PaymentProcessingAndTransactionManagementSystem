// React.
import {
  useState
} from "react";

// Material UI.
import {

  Container,

  Paper,

  Typography,

  TextField,

  Button,

  Alert

} from "@mui/material";

// Components.
import Navbar from
  "../components/Navbar";

// Hooks.
import {
  useTransactions
} from "../hooks/useTransactions";

// Types.
import type {

  CreateTransferResponse

} from "../types/transaction";


export default function TransferPage() {

  const [receiverId,
    setReceiverId
  ] = useState("");

  const [amount,
    setAmount
  ] = useState("");

  const [response,
    setResponse
  ] = useState<
    CreateTransferResponse | null
  >(null);

  const [error,
    setError
  ] = useState("");

  const {

    loading,

    createTransfer

  } = useTransactions();

  const handleSubmit =
    async (
      event:
      React.FormEvent
    ) => {

      event.preventDefault();

      setError("");

      try {

        const result =
          await createTransfer({

            receiver_id:
            Number(receiverId),

            amount
          });

        setResponse(
          result
        );

      } catch {

        setError(
          "Transfer failed."
        );
      }
    };

  return (

    <>

      <Navbar />

      <Container
        maxWidth="sm"
      >

        <Paper

          sx={{
            mt: 4,
            p: 4
          }}

        >

          <Typography

            variant="h4"

            gutterBottom

          >
            Transfer Funds
          </Typography>

          {

            error && (

              <Alert
                severity="error"
              >
                {error}
              </Alert>

            )
          }

          {

            response && (

              <Alert
                severity="success"
              >

                Transaction #

                {
                  response.transaction_id
                }

                {" created."}

              </Alert>

            )
          }

          <form
            onSubmit={
              handleSubmit
            }
          >

            <TextField

              fullWidth

              required

              margin="normal"

              label="Receiver ID"

              value={receiverId}

              onChange={(e) =>
                setReceiverId(
                  e.target.value
                )
              }

            />

            <TextField

              fullWidth

              required

              margin="normal"

              label="Amount"

              value={amount}

              onChange={(e) =>
                setAmount(
                  e.target.value
                )
              }

            />

            <Button

              type="submit"

              variant="contained"

              disabled={loading}

              sx={{
                mt: 2
              }}

            >
              Send
            </Button>

          </form>

        </Paper>

      </Container>

    </>

  );
}