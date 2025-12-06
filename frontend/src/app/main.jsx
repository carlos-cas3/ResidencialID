import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { CameraProvider } from "../context/CameraContext";
import App from "./App";
import "../index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <CameraProvider>
        <BrowserRouter>
            <App />
        </BrowserRouter>

        </CameraProvider>
    </React.StrictMode>
);