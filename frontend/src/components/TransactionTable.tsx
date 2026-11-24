// Material UI components.
import {

  Paper,

  Table,

  TableBody,

  TableCell,

  TableHead,

  TableRow,

  Typography,

  Chip

} from "@mui/material";


// Transaction type.
import type {

  Transaction

} from "../types/transaction";


// Component properties.
interface TransactionTableProps {

  // Transactions to display.
  transactions: Transaction[];
}


/**
 * Transaction history table.
 *
 * Displays:
 *
 * - Transaction ID
 * - Amount
 * - Status
 * - Retry Count
 * - Manual Review Flag
 * - Creation Date
 */
export default function TransactionTable(

  {
    transactions
  }: TransactionTableProps

) {

  return (

    <Paper>

      <Typography

        variant="h6"

        sx={{
          p: 2
        }}

      >
        Transaction History
      </Typography>

      <Table>

        <TableHead>

          <TableRow>

            <TableCell>
              ID
            </TableCell>

            <TableCell>
              Amount
            </TableCell>

            <TableCell>
              Status
            </TableCell>

            <TableCell>
              Retries
            </TableCell>

            <TableCell>
              Manual Review
            </TableCell>

            <TableCell>
              Created At
            </TableCell>

          </TableRow>

        </TableHead>

        <TableBody>

          {
            transactions.map(
              (
                transaction
              ) => (

                <TableRow
                  key={
                    transaction.id
                  }
                >

                  <TableCell>
                    {
                      transaction.id
                    }
                  </TableCell>

                  <TableCell>

                    $

                    {
                      Number(
                        transaction.amount
                      ).toLocaleString()
                    }

                  </TableCell>

                  <TableCell>

                    <Chip

                      label={
                        transaction.status
                      }

                      color={

                        transaction.status ===
                        "SUCCESS"

                          ? "success"

                        : transaction.status ===
                          "FAILED"

                          ? "error"

                          : "warning"
                      }

                    />

                  </TableCell>

                  <TableCell>

                    {
                      transaction.retry_count
                    }

                  </TableCell>

                  <TableCell>

                    {
                      transaction.manual_review_required
                        ? "Yes"
                        : "No"
                    }

                  </TableCell>

                  <TableCell>

                    {
                      new Date(
                        transaction.created_at
                      ).toLocaleString()
                    }

                  </TableCell>

                </TableRow>

              )
            )
          }

        </TableBody>

      </Table>

    </Paper>
  );
}