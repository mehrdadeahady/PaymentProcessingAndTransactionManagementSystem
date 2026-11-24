// Shared API client.
import api from "../api/axios";

// Wallet types.
import type {
  Wallet
} from "../types/wallet";


/**
 * Wallet service.
 *
 * Encapsulates wallet-related
 * API operations.
 */
class WalletService {

  /**
   * Load current user's wallet.
   *
   * Backend endpoint example:
   *
   * GET /api/wallets/me/
   */
  async getMyWallet():

  Promise<Wallet> {

    const response =
      await api.get(
        "/api/wallets/me/"
      );

    return response.data;
  }

  /**
   * Load wallet by id.
   *
   * Useful for admin views.
   */
  async getWalletById(
    walletId: number
  ): Promise<Wallet> {

    const response =
      await api.get(
        `/api/wallets/${walletId}/`
      );

    return response.data;
  }
}


// Singleton instance.
const walletService =
  new WalletService();

export default walletService;