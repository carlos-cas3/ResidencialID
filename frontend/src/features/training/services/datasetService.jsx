// src/features/training/services/datasetService.js

const API_URL = "http://localhost:5000/residentes";

// 1. Obtener candidatos para dataset
export async function getResidentsForDataset() {
    const res = await fetch(`${API_URL}/training-candidates`);
    if (!res.ok) {
        throw new Error(`Error ${res.status}: ${res.statusText}`);
    }
    return res.json();
}

// 2. Ejecutar entrenamiento (recibe array de IDs)
export async function startDatasetTraining(payload) {
    const res = await fetch(`${API_URL}/train-dataset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    
    if (!res.ok) {
        throw new Error(`Error ${res.status}: ${res.statusText}`);
    }
    
    return res.json();
}