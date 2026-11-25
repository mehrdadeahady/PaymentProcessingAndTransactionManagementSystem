// API client.
import api from
  "../api/axios";

// Wallet type.
import type {
  Wallet
} from "../types/wallet";


class WalletService {

  async getMyWallet():

  Promise<Wallet> {

    const response =
      await api.get(
        "/api/wallets/me/"
      );

    return response.data;
  }
}

const walletService =
  new WalletService();

export default walletService;