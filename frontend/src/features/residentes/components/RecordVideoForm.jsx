// RecordVideoForm.jsx
import { useState, useEffect } from "react";
import { useRecordVideo } from "../hooks/useRecordVideo";
import { useCameraControl } from "../../../context/CameraContext";
import CameraPreview from "./CameraPreview";
import RecordTimer from "./RecordTimer";
import { uploadRecordedResident } from "../services/residents.service";

export default function RecordVideoForm() {
    const { requestCamera, releaseCamera, cameraInUse } = useCameraControl();

    const {
        videoRef,
        isRecording,
        cameraError,
        startCamera,
        stopCamera,
        startRecording,
        stopRecording,
        getBlob,
        time,
        frames,
        fps,
    } = useRecordVideo();

    const [nombre, setNombre] = useState("");
    const [dni, setDni] = useState("");
    const [departamento, setDepartamento] = useState("");
    const [cameraReady, setCameraReady] = useState(false);

    useEffect(() => {
        const initCamera = async () => {
            // ✅ Verificar si otra parte de React está usando la cámara
            const canUseCamera = requestCamera("recording");

            if (!canUseCamera) {
                alert(
                    "⚠️ La cámara está marcada como en uso en otra pestaña de React.\n\n" +
                    "Si cerraste la pestaña de Reconocimiento pero aún ves este mensaje, " +
                    "es posible que el backend de Python todavía tenga la cámara abierta.\n\n" +
                    "Solución: Reinicia el servidor de Python (microservicio)."
                );
                return;
            }

            // ✅ Intentar iniciar la cámara del navegador
            const success = await startCamera();
            setCameraReady(success);
        };

        initCamera();

        return () => {
            stopCamera();
            releaseCamera("recording");
        };
    }, []);

    const handleSubmit = async () => {
        const video = getBlob();

        const formData = new FormData();
        formData.append("video", video);
        formData.append("nombre", nombre);
        formData.append("dni", dni);
        formData.append("departamento", departamento);

        await uploadRecordedResident(formData);
        alert("Residente registrado");
    };

    return (
        <div className="bg-white shadow rounded-lg p-6 max-w-3xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">
                Registrar por Grabación
            </h2>

            {/* ⚠️ Advertencia si otra pestaña de React usa la cámara */}
            {cameraInUse && cameraInUse !== "recording" && (
                <div className="mb-4 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
                    <p className="text-yellow-800 font-semibold">
                        ⚠️ La cámara está marcada como en uso en <strong>Reconocimiento Facial</strong>
                    </p>
                    <p className="text-yellow-700 text-sm mt-1">
                        Cierra esa pestaña para poder grabar aquí.
                    </p>
                </div>
            )}

            {/* ⚠️ Error de cámara */}
            {cameraError && (
                <div className="mb-4 p-4 bg-red-50 border-2 border-red-300 rounded-lg">
                    <p className="text-red-800 font-semibold">
                        ❌ Error al acceder a la cámara
                    </p>
                    <pre className="text-red-700 text-sm mt-2 whitespace-pre-wrap">
                        {cameraError}
                    </pre>
                    <button
                        onClick={async () => {
                            const success = await startCamera();
                            setCameraReady(success);
                        }}
                        className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded"
                    >
                        🔄 Reintentar
                    </button>
                </div>
            )}

            {/* ✅ Estado de la cámara */}
            <div className="mb-4 p-3 bg-gray-100 rounded-lg">
                <p className="text-sm">
                    Estado de la cámara:{" "}
                    <span className={cameraReady ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
                        {cameraReady ? "✅ Lista" : "❌ No disponible"}
                    </span>
                </p>
            </div>

            <CameraPreview videoRef={videoRef} />

            <RecordTimer time={time} frames={frames} fps={fps} />

            {/* Botones */}
            <div className="flex space-x-4 mt-4">
                {!isRecording ? (
                    <button
                        onClick={startRecording}
                        disabled={!cameraReady}
                        className={`px-4 py-2 rounded ${
                            !cameraReady
                                ? "bg-gray-400 cursor-not-allowed"
                                : "bg-green-600 hover:bg-green-700 text-white"
                        }`}
                    >
                        Iniciar Grabación
                    </button>
                ) : (
                    <button
                        onClick={stopRecording}
                        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                    >
                        Detener
                    </button>
                )}
            </div>

            {/* Formulario */}
            <div className="grid grid-cols-3 gap-4 mt-5">
                <input
                    className="border p-2 rounded"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />
                <input
                    className="border p-2 rounded"
                    placeholder="DNI"
                    value={dni}
                    onChange={(e) => setDni(e.target.value)}
                />
                <input
                    className="border p-2 rounded"
                    placeholder="Departamento"
                    value={departamento}
                    onChange={(e) => setDepartamento(e.target.value)}
                />
            </div>

            <button
                onClick={handleSubmit}
                disabled={!cameraReady}
                className={`mt-6 px-6 py-2 rounded ${
                    !cameraReady
                        ? "bg-gray-400 cursor-not-allowed"
                        : "bg-blue-600 hover:bg-blue-700 text-white"
                }`}
            >
                Guardar
            </button>
        </div>
    );
}