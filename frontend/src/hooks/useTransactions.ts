// React state management.
import {

  useEffect,

  useState

} from "react";

// Transaction service.
import transactionService from
  "../services/transactionService";

// Transaction models.
import type {

  Transaction,

  CreateTransferRequest,

  CreateTransferResponse

} from
  "../types/transaction";


/**
 * Transaction hook.
 *
 * Responsibilities:
 *
 * - Load transactions
 * - Create transfers
 * - Refresh status
 * - Handle loading state
 *
 * Pages should consume
 * this hook instead of
 * calling services directly.
 */
export const useTransactions = () => {

  // Transaction collection.
  const [transactions,
    setTransactions
  ] = useState<Transaction[]>(
    []
  );

  // Loading state.
  const [loading,
    setLoading
  ] = useState(false);

  // Request errors.
  const [error,
    setError
  ] = useState<
    string | null
  >(null);

  /**
   * Load transaction history.
   */
  const loadTransactions =
    async () => {

      try {

        setLoading(true);

        setError(null);

        const data =
          await transactionService
            .getTransactions();

        setTransactions(
          data
        );

      } catch (err) {

        setError(
          "Failed to load transactions"
        );

      } finally {

        setLoading(false);
      }
    };

  /**
   * Create transfer.
   */
  const createTransfer =
    async (

      payload:
      CreateTransferRequest

    ): Promise<
      CreateTransferResponse
    > => {

      setLoading(true);

      try {

        const result =
          await transactionService
            .createTransfer(
              payload
            );

        // Refresh list after
        // transaction creation.
        await loadTransactions();

        return result;

      } finally {

        setLoading(false);
      }
    };

  /**
   * Refresh one transaction.
   *
   * Useful for:
   *
   * PENDING
   * PROCESSING
   * RETRYING
   */
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
        (previous) =>
          previous.map(
            (transaction) =>

              transaction.id ===
              transactionId

                ? updated

                : transaction
          )
      );
    };

  /**
   * Load data automatically.
   */
  useEffect(() => {

    loadTransactions();

  }, []);

  return {

    transactions,

    loading,

    error,

    loadTransactions,

    createTransfer,

    refreshTransaction,
  };
};