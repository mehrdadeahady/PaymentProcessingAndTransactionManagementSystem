// Shared API client.
import api from "../api/axios";

// Transaction DTOs.
import type {

  Transaction,

  CreateTransferRequest,

  CreateTransferResponse

} from "../types/transaction";


/**
 * Transaction service.
 *
 * Responsibilities:
 *
 * - Create transfers
 * - Load transaction history
 * - Load transaction details
 *
 * Pages should call
 * this service rather
 * than axios directly.
 */
class TransactionService {

  /**
   * Create transfer.
   *
   * Triggers backend
   * transaction workflow.
   */
  async createTransfer(

    payload:
    CreateTransferRequest

  ): Promise<
    CreateTransferResponse
  > {

    // Create idempotency key.
    //
    // Prevents duplicate
    // transfers caused by:
    //
    // double-clicking
    // retries
    // network failures
    const idempotencyKey =
      crypto.randomUUID();

    const response =
      await api.post(

        "/api/transactions/transfer/",

        payload,

        {

          headers: {

            "Idempotency-Key":
            idempotencyKey
          }
        }
      );

    return response.data;
  }

  /**
   * Load all transactions
   * for current user.
   *
   * Backend example:
   *
   * GET /api/transactions/
   */
  async getTransactions():

  Promise<Transaction[]> {

    const response =
      await api.get(
        "/api/transactions/"
      );

    return response.data;
  }

  /**
   * Get single transaction.
   */
  async getTransaction(

    transactionId: number

  ): Promise<Transaction> {

    const response =
      await api.get(

        `/api/transactions/${transactionId}/`
      );

    return response.data;
  }

  /**
   * Refresh transaction status.
   *
   * Useful for:
   *
   * PENDING
   * PROCESSING
   * RETRYING
   */
  async getTransactionStatus(

    transactionId: number

  ): Promise<string> {

    const response =
      await api.get(

        `/api/transactions/${transactionId}/`
      );

    return response.data.status;
  }

  /**
   * Load failed transactions.
   *
   * Useful for future
   * operations dashboards.
   */
  async getFailedTransactions():

  Promise<Transaction[]> {

    const response =
      await api.get(

        "/api/transactions/?status=FAILED"
      );

    return response.data;
  }

  /**
   * Load transactions requiring
   * manual review.
   */
  async getManualReviewTransactions():

  Promise<Transaction[]> {

    const response =
      await api.get(

        "/api/transactions/?manual_review_required=true"
      );

    return response.data;
  }
}


// Singleton instance.
const transactionService =
  new TransactionService();

export default transactionService;
