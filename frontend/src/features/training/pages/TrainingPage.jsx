// pages/TrainingPage.jsx
import { useState } from "react";
import DatasetCard from "../components/DatasetCard";
import { useDatasets } from "../hooks/useDatasets";

export default function TrainingPage() {
    const {
        residents,
        loading,
        selected,
        toggleSelect,
        startTraining,
        processing,
    } = useDatasets();

    // Estado para el entrenamiento del modelo
    const [trainingModel, setTrainingModel] = useState(false);
    const [trainMessage, setTrainMessage] = useState("");

    // ---- Entrenar modelo completo ----
    const trainFaceModel = async () => {
        try {
            setTrainingModel(true);
            setTrainMessage("Entrenando modelo…");

            const response = await fetch("http://localhost:8000/train-model", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({}), // No mandar rutas relativas
            });

            const data = await response.json();

            if (data.status === "success") {
                setTrainMessage("Modelo entrenado correctamente 🎉");
            } else {
                setTrainMessage("Error al entrenar: " + data.message);
            }
        } catch (error) {
            console.error(error);
            setTrainMessage("Error al conectar con el microservicio.");
        } finally {
            setTimeout(() => setTrainingModel(false), 1500);
        }
    };

    if (loading)
        return (
            <div className="flex justify-center py-10">
                <p className="text-slate-600 text-lg">Cargando residentes…</p>
            </div>
        );

    return (
        <div className="mx-auto max-w-5xl py-8">
            {/* TÍTULO */}
            <div className="mb-6">
                <h1 className="text-3xl font-bold text-slate-800">
                    Entrenamiento de Reconocimiento Facial
                </h1>
                <p className="text-slate-600 mt-1">
                    Selecciona los residentes que cumplen los criterios para
                    generar su dataset.
                </p>
            </div>

            {/* RESUMEN */}
            <div className="bg-white p-4 rounded-xl shadow mb-6 border border-slate-200">
                <p className="text-lg text-slate-700">
                    Residentes elegibles:{" "}
                    <strong className="text-blue-600">
                        {residents.length}
                    </strong>
                </p>
                <p className="text-slate-500 text-sm mt-1">
                    (Con video, activos y que necesitan entrenamiento)
                </p>
            </div>

            {/* LISTA DE RESIDENTES */}
            {residents.length === 0 ? (
                <p className="text-slate-500 text-center text-lg">
                    No hay residentes que cumplan los criterios.
                </p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {residents.map((r) => (
                        <DatasetCard
                            key={r.id}
                            resident={r}
                            selected={selected.includes(r.id)}
                            onSelect={toggleSelect}
                        />
                    ))}
                </div>
            )}

            {/* BOTÓN GENERAR DATASET */}
            <div className="mt-8 flex justify-end">
                <button
                    className={`px-6 py-3 rounded-xl font-semibold transition
                        ${
                            selected.length === 0
                                ? "bg-slate-300 text-slate-500 cursor-not-allowed"
                                : "bg-blue-600 text-white hover:bg-blue-700 shadow"
                        }
                        ${processing ? "opacity-60 cursor-wait" : ""}
                    `}
                    disabled={selected.length === 0 || processing}
                    onClick={async () => {
                        const result = await startTraining();
                        alert("Dataset generado.");
                    }}
                >
                    {processing
                        ? "Generando dataset…"
                        : `Generar Dataset (${selected.length})`}
                </button>
            </div>

            {/* BOTÓN ENTRENAR MODELO COMPLETO */}
            <div className="mt-6 flex justify-end">
                <button
                    onClick={trainFaceModel}
                    disabled={trainingModel}
                    className={`px-6 py-3 rounded-xl font-semibold transition flex items-center gap-3
                        ${
                            trainingModel
                                ? "bg-gray-400 cursor-wait"
                                : "bg-green-600 hover:bg-green-700 text-white shadow"
                        }
                    `}
                >
                    {trainingModel && (
                        <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    )}
                    {trainingModel
                        ? "Entrenando modelo…"
                        : "Entrenar Modelo Facial"}
                </button>
            </div>

            {/* MENSAJE DE ESTADO */}
            {trainMessage && (
                <p className="mt-3 text-right text-slate-600 text-sm">
                    {trainMessage}
                </p>
            )}
        </div>
    );
}
