import { useEffect, useState } from "react";

export default function ResidentStatsCards() {
    const [residentes, setResidentes] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/residentes")
            .then(res => res.json())
            .then(res => setResidentes(res.data))
            .catch(err => console.error("Error cargando residentes", err));
    }, []);

    const total = residentes.length;
    const activos = residentes.filter(r => r.estado === "activo").length;
    const inactivos = residentes.filter(r => r.estado === "inactivo").length;
    const conVideo = residentes.filter(r => r.video_url).length;
    const pendientesEntrenamiento = residentes.filter(r => r.estado === "activo" && JSON.parse(r.necesita_entrenamiento)).length;

    return (
        <div className="grid grid-cols-5 gap-4 mb-6">

            {/* TOTAL */}
            <div className="p-4 bg-white shadow rounded-lg">
                <p className="text-gray-500">Total residentes</p>
                <h2 className="text-2xl font-bold">{total}</h2>
            </div>

            {/* ACTIVOS */}
            <div className="p-4 bg-white shadow rounded-lg">
                <p className="text-gray-500">Activos</p>
                <h2 className="text-2xl font-bold text-green-600">{activos}</h2>
            </div>

            {/* INACTIVOS */}
            <div className="p-4 bg-white shadow rounded-lg">
                <p className="text-gray-500">Inactivos</p>
                <h2 className="text-2xl font-bold text-red-600">{inactivos}</h2>
            </div>

            {/* CON VIDEO */}
            <div className="p-4 bg-white shadow rounded-lg">
                <p className="text-gray-500">Con video</p>
                <h2 className="text-2xl font-bold">{conVideo}</h2>
            </div>

            {/* PENDIENTES ENTRENAMIENTO */}
            <div className="p-4 bg-white shadow rounded-lg">
                <p className="text-gray-500">Pendientes de entrenamiento</p>
                <h2 className="text-2xl font-bold text-yellow-600">{pendientesEntrenamiento}</h2>
            </div>
        </div>
    );
}
