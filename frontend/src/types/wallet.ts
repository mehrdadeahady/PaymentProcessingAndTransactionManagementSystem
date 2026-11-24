// Wallet model returned
// by backend APIs.
export interface Wallet {

  // Wallet database id.
  id: number;

  // Owner id.
  user: number;

  // Current balance.
  balance: string;

  // Last update timestamp.
  updated_at: string;
}