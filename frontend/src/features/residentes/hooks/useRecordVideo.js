// hooks/useRecordVideo.js
import { useRef, useState } from "react";

export function useRecordVideo() {
    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const mediaRecorderRef = useRef(null);

    const [chunks, setChunks] = useState([]);
    const [isRecording, setIsRecording] = useState(false);
    const [cameraError, setCameraError] = useState(null); // ← Nuevo estado

    const [time, setTime] = useState(0);
    const [frames, setFrames] = useState(0);
    const [fps, setFps] = useState(0);

    const timerIntervalRef = useRef(null);

    const startCamera = async () => {
        try {
            setCameraError(null); // Limpiar error anterior

            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false,
            });

            streamRef.current = stream;
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }

            console.log("✅ Cámara iniciada correctamente en el frontend");
            return true;

        } catch (err) {
            console.error("❌ Error iniciando cámara:", err);

            let errorMessage = "No se pudo iniciar la cámara.\n\n";

            // ✅ Detectar el tipo de error
            if (err.name === "NotAllowedError") {
                errorMessage += "📌 Permisos de cámara bloqueados en el navegador\n";
                errorMessage += "→ Ve a Configuración del sitio y permite el acceso a la cámara";
            } else if (err.name === "NotReadableError") {
                errorMessage += "⚠️ La cámara está siendo usada por otra aplicación\n\n";
                errorMessage += "Posibles causas:\n";
                errorMessage += "• El reconocimiento facial está activo (cierra esa pestaña)\n";
                errorMessage += "• Otra aplicación (Zoom, Teams, etc.) tiene la cámara abierta\n";
                errorMessage += "• El microservicio de Python está usando la cámara";
            } else if (err.name === "NotFoundError") {
                errorMessage += "📌 No se encontró ninguna cámara conectada";
            } else {
                errorMessage += `📌 Error: ${err.name}\n${err.message}`;
            }

            setCameraError(errorMessage);
            alert(errorMessage);
            return false;
        }
    };

    const startRecording = () => {
        if (!streamRef.current) {
            alert("⚠️ Primero debes iniciar la cámara");
            return;
        }

        mediaRecorderRef.current = new MediaRecorder(streamRef.current);

        setChunks([]);

        mediaRecorderRef.current.ondataavailable = (e) => {
            setFrames((prev) => prev + 1);
            setChunks((prev) => [...prev, e.data]);
        };

        mediaRecorderRef.current.start(100);
        setIsRecording(true);

        let lastTime = performance.now();
        let frameCount = 0;

        timerIntervalRef.current = setInterval(() => {
            setTime((prev) => prev + 1);
            frameCount++;
            const now = performance.now();
            const elapsed = (now - lastTime) / 1000;
            setFps(frameCount / elapsed);
            frameCount = 0;
            lastTime = now;
        }, 1000);
    };

    const stopRecording = () => {
        mediaRecorderRef.current?.stop();

        if (timerIntervalRef.current) {
            clearInterval(timerIntervalRef.current);
            timerIntervalRef.current = null;
        }

        setIsRecording(false);
    };

    const stopCamera = () => {
        streamRef.current?.getTracks()?.forEach((t) => t.stop());

        if (timerIntervalRef.current) {
            clearInterval(timerIntervalRef.current);
            timerIntervalRef.current = null;
        }

        console.log("🔴 Cámara detenida en el frontend");
    };

    const getBlob = () => new Blob(chunks, { type: "video/mp4" });

    return {
        videoRef,
        isRecording,
        cameraError, // ← Exponer error
        startCamera,
        stopCamera,
        startRecording,
        stopRecording,
        getBlob,
        time,
        frames,
        fps,
    };
}