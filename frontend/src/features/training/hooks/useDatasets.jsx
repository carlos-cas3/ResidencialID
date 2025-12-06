// hooks/useDatasets.jsx
import { useEffect, useState } from "react";
import {
    getResidentsForDataset,
    startDatasetTraining,
} from "../services/datasetService";

export const useDatasets = () => {
    const [residents, setResidents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selected, setSelected] = useState([]);
    const [processing, setProcessing] = useState(false);

    const loadResidents = async () => {
        setLoading(true);
        try {
            const data = await getResidentsForDataset();
            setResidents(data.data || []);
        } catch (err) {
            console.error("Error cargando residentes:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadResidents();
    }, []);

    const toggleSelect = (id) => {
        setSelected((prev) =>
            prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
        );
    };

    const startTraining = async () => {
        if (selected.length === 0) return;

        setProcessing(true);

        try {
            // ✅ Enviar todos los IDs en una sola petición
            const result = await startDatasetTraining({ 
                residentes: selected  // ← Cambio clave aquí
            });

            console.log("Resultado del entrenamiento:", result);

            // Refrescar lista y limpiar selección
            await loadResidents();
            setSelected([]);
            
            return result;
        } catch (err) {
            console.error("Error durante entrenamiento:", err);
            alert("Ocurrió un error durante el entrenamiento");
            throw err;
        } finally {
            setProcessing(false);
        }
    };

    return {
        residents,
        loading,
        selected,
        toggleSelect,
        startTraining,
        processing,
    };
};