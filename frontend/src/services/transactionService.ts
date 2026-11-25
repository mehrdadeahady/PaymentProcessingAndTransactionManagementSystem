// Shared API client.
import api from "../api/axios";

// DTOs.
import type {

  Transaction,

  CreateTransferRequest,

  CreateTransferResponse

} from "../types/transaction";


class TransactionService {

  async createTransfer(

    payload:
    CreateTransferRequest

  ): Promise<
    CreateTransferResponse
  > {

    const response =
      await api.post(

        "/api/transactions/transfer/",

        payload,

        {

          headers: {

            "Idempotency-Key":

            crypto.randomUUID()
          }
        }
      );

    return response.data;
  }

  async getTransactions():

  Promise<Transaction[]> {

    const response =
      await api.get(
        "/api/transactions/"
      );

    return response.data;
  }

  async getTransaction(

    transactionId: number

  ): Promise<Transaction> {

    const response =
      await api.get(

        `/api/transactions/${transactionId}/`
      );

    return response.data;
  }
}

const transactionService =
  new TransactionService();

export default transactionService;