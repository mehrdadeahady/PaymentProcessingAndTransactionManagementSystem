// Transaction status values.
export type TransactionStatus =

  | "PENDING"

  | "PROCESSING"

  | "SUCCESS"

  | "FAILED"

  | "RETRYING";


// Transaction model.
export interface Transaction {

  id: number;

  sender: number;

  receiver: number;

  amount: string;

  status:
  TransactionStatus;

  retry_count: number;

  provider_reference:
  string | null;

  manual_review_required:
  boolean;

  created_at: string;

  updated_at: string;
}


// Create transfer request.
export interface CreateTransferRequest {

  receiver_id: number;

  amount: string;
}


// Create transfer response.
export interface CreateTransferResponse {

  transaction_id: number;

  status: string;
}