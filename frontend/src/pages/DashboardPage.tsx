// React hooks.
import {

  useEffect,

  useState

} from "react";

// Material UI.
import {

  Container,

  Typography,

  CircularProgress,

  Alert,

  Box

} from "@mui/material";

// Components.
import Navbar from
  "../components/Navbar";

import WalletCard from
  "../components/WalletCard";

import TransactionTable from
  "../components/TransactionTable";

// Services.
import walletService from
  "../services/walletService";

// Hooks.
import {
  useTransactions
} from "../hooks/useTransactions";

// Types.
import type {
  Wallet
} from "../types/wallet";


export default function DashboardPage() {

  const [wallet,
    setWallet
  ] = useState<
    Wallet | null
  >(null);

  const [walletLoading,
    setWalletLoading
  ] = useState(true);

  const [walletError,
    setWalletError
  ] = useState("");

  const {

    transactions,

    loading:
    transactionLoading,

    error:
    transactionError,

    loadTransactions

  } = useTransactions();

  const loadWallet =
    async () => {

      try {

        setWalletLoading(
          true
        );

        setWalletError("");

        const result =
          await walletService
            .getMyWallet();

        setWallet(
          result
        );

      } catch {

        setWalletError(
          "Failed to load wallet."
        );

      } finally {

        setWalletLoading(
          false
        );
      }
    };

  useEffect(() => {

    loadWallet();

    loadTransactions();

  }, []);

  const failedTransactions =

    transactions.filter(
      (item) =>

        item.status ===
        "FAILED"
    ).length;

  const reviewTransactions =

    transactions.filter(
      (item) =>

        item.manual_review_required
    ).length;

  return (

    <>

      <Navbar />

      <Container

        maxWidth="lg"

        sx={{
          mt: 4
        }}

      >

        <Typography

          variant="h4"

          gutterBottom

        >
          Dashboard
        </Typography>

        {

          reviewTransactions > 0 && (

            <Alert

              severity="warning"

              sx={{
                mb: 2
              }}

            >

              {
                reviewTransactions
              }

              {" "}

              transaction(s)
              require manual review.

            </Alert>
          )
        }

        {

          failedTransactions > 0 && (

            <Alert

              severity="error"

              sx={{
                mb: 2
              }}

            >

              {
                failedTransactions
              }

              {" "}

              failed transaction(s)
              detected.

            </Alert>
          )
        }

        {

          walletLoading ? (

            <Box
              textAlign="center"
            >

              <CircularProgress />

            </Box>

          ) : walletError ? (

            <Alert
              severity="error"
            >

              {
                walletError
              }

            </Alert>

          ) : wallet ? (

            <WalletCard
              wallet={wallet}
            />

          ) : null
        }

        <Box
          sx={{
            mt: 4
          }}
        >

          {

            transactionLoading ? (

              <CircularProgress />

            ) : transactionError ? (

              <Alert
                severity="error"
              >

                {
                  transactionError
                }

              </Alert>

            ) : (

              <TransactionTable

                transactions={
                  transactions
                }

              />

            )
          }

        </Box>

      </Container>

    </>

  );
}