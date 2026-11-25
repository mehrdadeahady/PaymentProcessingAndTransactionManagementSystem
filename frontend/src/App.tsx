// Router.
import {
  BrowserRouter
} from "react-router-dom";

// Route definitions.
import AppRoutes from
  "./routes/AppRoutes";


export default function App() {

  return (

    <BrowserRouter>

      <AppRoutes />

    </BrowserRouter>

  );
}