// Material UI components.
import {

  Card,

  CardContent,

  Typography

} from "@mui/material";

// Wallet type.
import type {
  Wallet
} from "../types/wallet";


// Component properties.
interface WalletCardProps {

  // Wallet object.
  wallet: Wallet;
}


/**
 * Wallet summary card.
 *
 * Displays current balance.
 */
export default function WalletCa*d(

  {
    wallet
  }: WalletCard*rops

) {

  return (

    <Card>
*      <CardContent>

        <Typo*raphy
          variant="h6"
     *  >
          Current Balance
    *   </Typography>

        <Typogra*hy
          variant="h4"
        *

          $
          {
        *   Number(
              wallet.ba*ance
            ).toLocaleString(*
          }

        </Typography*

        <Typography
          co*or="text.secondary"
        >
    *     Last Updated:
          {" "}*          {
            new Date(
*             wallet.updated_at
   *        ).toLocaleString()
       *  }
        </Typography>

      <*CardContent>

    </Card>
  );
}
`*
