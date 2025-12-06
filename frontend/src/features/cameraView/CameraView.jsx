import { useEffect, useState, useRef } from "react";

const ConnectionBadge = ({ status }) => {
    const statusConfig = {
        connected: { color: "bg-green-500", text: "Conectado", pulse: true },
        connecting: { color: "bg-yellow-500", text: "Conectando...", pulse: true },
        reconnecting: { color: "bg-orange-500", text: "Reconectando...", pulse: true },
        disconnected: { color: "bg-red-500", text: "Desconectado", pulse: false },
    };

    const config = statusConfig[status];

    return (
        <div className="flex items-center gap-2">
            <div className="relative">
                <div className={`w-3 h-3 rounded-full ${config.color}`}></div>
                {config.pulse && (
                    <div className={`absolute inset-0 w-3 h-3 rounded-full ${config.color} animate-ping opacity-75`}></div>
                )}
            </div>
            <span className="text-sm font-medium text-gray-700">{config.text}</span>
        </div>
    );
};

const getLevelStyles = (level) => {
    switch (level) {
        case "success":
            return { bg: "bg-green-50 border-green-200", text: "text-green-700", badge: "bg-green-100 text-green-800", icon: "✅" };
        case "warning":
            return { bg: "bg-yellow-50 border-yellow-200", text: "text-yellow-700", badge: "bg-yellow-100 text-yellow-800", icon: "⚠️" };
        case "error":
            return { bg: "bg-red-50 border-red-200", text: "text-red-700", badge: "bg-red-100 text-red-800", icon: "❌" };
        default:
            return { bg: "bg-blue-50 border-blue-200", text: "text-blue-700", badge: "bg-blue-100 text-blue-800", icon: "ℹ️" };
    }
};

export default function CameraView() {
    const [logs, setLogs] = useState([]);
    const [connectionStatus, setConnectionStatus] = useState("connecting");
    const [cameraActive, setCameraActive] = useState(false);
    const [streamUrl, setStreamUrl] = useState("");
    const logsEndRef = useRef(null);

    const scrollToBottom = () => {
        logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [logs]);

    // Limpiar al desmontar
    useEffect(() => {
        return () => {
            if (cameraActive) {
                stopCamera();
            }
        };
    }, [cameraActive]);

    // Conectar a eventos SSE
    useEffect(() => {
        const events = new EventSource("http://localhost:8000/events");

        events.onopen = () => {
            console.log("✅ Conectado a eventos en tiempo real");
            setConnectionStatus("connected");
        };

        events.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setLogs((prev) => [data, ...prev].slice(0, 100));
            } catch (e) {
                console.error("Error parsing event:", e);
            }
        };

        events.onerror = () => {
            console.warn("❌ Error en SSE, intentando reconectar...");
            setConnectionStatus("reconnecting");
        };

        return () => {
            events.close();
            setConnectionStatus("disconnected");
        };
    }, []);

    const startCamera = async () => {
        try {
            // ✅ Llamar al backend para iniciar la cámara
            const res = await fetch("http://localhost:8000/camera/start", {
                method: "POST"
            });
            const data = await res.json();

            if (data.status === "success" || data.status === "already_running") {
                setCameraActive(true);
                setStreamUrl(`http://localhost:8000/video-stream?t=${Date.now()}`);
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error("Error iniciando cámara:", error);
            alert("No se pudo conectar con el microservicio");
        }
    };

    const stopCamera = async () => {
        try {
            await fetch("http://localhost:8000/camera/stop", {
                method: "POST"
            });
            setCameraActive(false);
            setStreamUrl("");
        } catch (error) {
            console.error("Error deteniendo cámara:", error);
        }
    };

    return (
        <div className="flex flex-col lg:flex-row gap-6 p-6 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
            {/* ---------- VIDEO STREAM ----------- */}
            <div className="flex-1 bg-white shadow-2xl rounded-2xl p-6 border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                        🎥 Reconocimiento Facial
                    </h2>
                    {cameraActive && (
                        <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-semibold flex items-center gap-2">
                            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                            LIVE
                        </span>
                    )}
                </div>

                {/* Control de cámara */}
                <div className="mb-4">
                    <button
                        onClick={cameraActive ? stopCamera : startCamera}
                        className={`px-6 py-3 rounded-xl font-semibold transition-all shadow-lg ${
                            cameraActive
                                ? "bg-red-600 hover:bg-red-700 text-white"
                                : "bg-green-600 hover:bg-green-700 text-white"
                        }`}
                    >
                        {cameraActive ? "⏹️ Detener Cámara" : "▶️ Iniciar Cámara"}
                    </button>
                </div>

                {/* Video Stream */}
                <div className="relative border-4 border-gray-300 rounded-2xl overflow-hidden bg-black aspect-video">
                    {cameraActive ? (
                        <img
                            src={streamUrl}
                            alt="Video stream"
                            className="w-full h-full object-contain"
                            onLoad={() => {
                                console.log("✅ Stream cargado correctamente");
                            }}
                            onError={(e) => {
                                console.error("❌ Error cargando stream");
                            }}
                        />
                    ) : (
                        <div className="flex items-center justify-center h-full">
                            <div className="text-center text-gray-400">
                                <svg className="w-24 h-24 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                                <p className="text-xl font-semibold">Cámara Detenida</p>
                                <p className="text-sm mt-2">Presiona "Iniciar Cámara" para comenzar el reconocimiento</p>
                                <p className="text-xs mt-3 text-gray-500">
                                    ✅ La cámara estará disponible para grabar video cuando esté detenida
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                <div className="mt-4 flex items-center justify-between text-sm text-gray-600">
                    <p>📍 Estado: <span className={cameraActive ? "text-green-600 font-semibold" : "text-gray-500"}>{cameraActive ? "Activo" : "Inactivo"}</span></p>
                    <p>🔄 Reconocimiento facial en tiempo real</p>
                </div>
            </div>

            {/* ---------- LIVE EVENTS ---------- */}
            <div className="w-full lg:w-96 bg-white shadow-2xl rounded-2xl p-6 border border-gray-200 flex flex-col">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                        ⚡ Eventos en Vivo
                    </h2>
                    <ConnectionBadge status={connectionStatus} />
                </div>

                <div className="mb-4 px-4 py-2 bg-gray-50 rounded-lg border border-gray-200">
                    <p className="text-sm text-gray-600">
                        Total de eventos: <span className="font-bold text-gray-800">{logs.length}</span>
                    </p>
                </div>

                <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar" style={{ maxHeight: "calc(100vh - 300px)" }}>
                    {logs.length === 0 && (
                        <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                            <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                            </svg>
                            <p className="text-lg font-medium">Esperando eventos...</p>
                            <p className="text-sm mt-1">Los eventos aparecerán aquí en tiempo real</p>
                        </div>
                    )}

                    {logs.map((log, index) => {
                        const styles = getLevelStyles(log.level);
                        return (
                            <div key={index} className={`p-4 rounded-xl border-2 ${styles.bg} transition-all duration-300 hover:shadow-lg transform hover:-translate-y-1`}>
                                <div className="flex items-start justify-between mb-2">
                                    <span className="text-xs font-mono text-gray-500">{log.timestamp}</span>
                                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${styles.badge} flex items-center gap-1`}>
                                        <span>{styles.icon}</span>
                                        {log.level.toUpperCase()}
                                    </span>
                                </div>
                                <p className={`text-sm font-medium ${styles.text} leading-relaxed`}>{log.message}</p>
                            </div>
                        );
                    })}
                    <div ref={logsEndRef} />
                </div>

                {logs.length > 0 && (
                    <button
                        onClick={() => setLogs([])}
                        className="mt-4 w-full px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center gap-2"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Limpiar eventos
                    </button>
                )}
            </div>

            <style>{`
                .custom-scrollbar::-webkit-scrollbar {
                    width: 8px;
                }
                .custom-scrollbar::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb {
                    background: #cbd5e1;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb:hover {
                    background: #94a3b8;
                }
            `}</style>
        </div>
    );
}