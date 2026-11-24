// Transaction statuses.
//
// Must match Django model.
export type TransactionStatus =

  | "PENDING"

  | "PROCESSING"

  | "SUCCESS"

  | "FAILED"

  | "RETRYING";


// Transaction model.
export interface Transaction {

  // Transaction id.
  id: number;

  // Sender user id.
  sender: number;

  // Receiver user id.
  receiver: number;

  // Monetary amount.
  amount: string;

  // Status.
  status: TransactionStatus;

  // Retry attempts.
  retry_count: number;

  // Provider transaction id.
  provider_reference?: string;

  // Manual review flag.
  manual_review_required: boolean;

  // Creation timestamp.
  created_at: string;

  // Update timestamp.
  updated_at: string;
}


// Transfer request.
export interface CreateTransferRequest {

  // Receiver user id.
  receiver_id: number;

  // Transfer amount.
  amount: string;
}


// Transfer response.
export interface CreateTransferResponse {

  // Transaction id.
  transaction_id: number;

  // Current status.
  status: string;
}
