// src/context/CameraContext.jsx
import { createContext, useContext, useState } from "react";

const CameraContext = createContext();

export const useCameraControl = () => {
    const context = useContext(CameraContext);
    if (!context) {
        throw new Error("useCameraControl debe usarse dentro de CameraProvider");
    }
    return context;
};

export const CameraProvider = ({ children }) => {
    const [cameraInUse, setCameraInUse] = useState(null); // null | "recognition" | "recording"

    const requestCamera = (component) => {
        if (cameraInUse && cameraInUse !== component) {
            return false; // Cámara ocupada
        }
        setCameraInUse(component);
        return true;
    };

    const releaseCamera = (component) => {
        if (cameraInUse === component) {
            setCameraInUse(null);
        }
    };

    return (
        <CameraContext.Provider value={{ cameraInUse, requestCamera, releaseCamera }}>
            {children}
        </CameraContext.Provider>
    );
};