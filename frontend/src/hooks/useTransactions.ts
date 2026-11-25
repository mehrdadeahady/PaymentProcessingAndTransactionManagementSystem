// React hooks.
import {

  useState

} from "react";

// Service layer.
import transactionService
from "../services/transactionService";

// Types.
import type {

  Transaction,

  CreateTransferRequest,

  CreateTransferResponse

} from
"../types/transaction";


export const useTransactions = () => {

  const [transactions,
    setTransactions
  ] = useState<Transaction[]>(
    []
  );

  const [loading,
    setLoading
  ] = useState(false);

  const [error,
    setError
  ] = useState<
    string | null
  >(null);

  const loadTransactions =
    async () => {

      try {

        setLoading(true);

        setError(null);

        const result =
          await transactionService
            .getTransactions();

        setTransactions(
          result
        );

      } catch {

        setError(
          "Failed to load transactions."
        );

      } finally {

        setLoading(false);
      }
    };

  const createTransfer =
    async (

      payload:
      CreateTransferRequest

    ): Promise<
      CreateTransferResponse
    > => {

      try {

        setLoading(true);

        const result =
          await transactionService
            .createTransfer(
              payload
            );

        return result;

      } finally {

        setLoading(false);
      }
    };

  const refreshTransaction =
    async (
      transactionId: number
    ) => {

      const updated =
        await transactionService
          .getTransaction(
            transactionId
          );

      setTransactions(
        (current) =>

          current.map(
            (item) =>

              item.id ===
              transactionId

                ? updated

                : item
          )
      );
    };

  return {

    transactions,

    loading,

    error,

    loadTransactions,

    createTransfer,

    refreshTransaction
  };
};