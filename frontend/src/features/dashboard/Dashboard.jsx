import React, { useEffect, useState } from "react";
import { saveAs } from "file-saver";

export default function Dashboard() {
    const [residentes, setResidentes] = useState([]);
    const [accesos, setAccesos] = useState([]);
    const [loading, setLoading] = useState(true);

    // Pagination
    const itemsPerPage = 15;
    const [page, setPage] = useState(1);

    const paginatedData = residentes.slice(
        (page - 1) * itemsPerPage,
        page * itemsPerPage
    );

    useEffect(() => {
        Promise.all([
            fetch("http://localhost:5000/residentes/").then((res) =>
                res.json()
            ),
            fetch("http://localhost:5000/accesos/").then((res) => res.json()),
        ])
            .then(([res1, res2]) => {
                setResidentes(res1.data || []);
                setAccesos(res2.data || []);
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div className="p-6 text-xl">Cargando...</div>;

    // KPIs
    const totalResidentes = residentes.length;
    const activos = residentes.filter((r) => r.estado === "activo").length;
    const inactivos = residentes.filter((r) => r.estado === "inactivo").length;
    const pendientesEntrenamiento = residentes.filter(
        (r) => r.necesita_entrenamiento
    ).length;

    // export
    const exportExcel = () => {
        const rows = [
            ["N°", "Nombre", "DNI", "Departamento", "Estado", "Video"],
            ...residentes.map((r, i) => [
                i + 1,
                r.nombre || "",
                r.dni || "",
                r.departamento || "",
                r.estado || "",
                r.video_url || "",
            ]),
        ];

        const csv = rows.map((r) => r.join(",")).join("\n");
        const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
        saveAs(blob, "residentes.csv");
    };

    return (
        <div className="p-8">

            {/* KPI CARDS */}
            <div className="grid grid-cols-4 gap-6 mb-10">
                <KPI
                    color="bg-blue-100"
                    icon="👥"
                    title="Total Residentes"
                    value={totalResidentes}
                />
                <KPI
                    color="bg-green-100"
                    icon="✅"
                    title="Activos"
                    value={activos}
                />
                <KPI
                    color="bg-red-100"
                    icon="❌"
                    title="Inactivos"
                    value={inactivos}
                />
                <KPI
                    color="bg-yellow-100"
                    icon="⚠️"
                    title="Pendientes Entrenamiento"
                    value={pendientesEntrenamiento}
                />
            </div>

            {/* TABLE */}
            <div className="bg-white shadow-lg rounded-2xl p-6 border">
                <div className="flex justify-between items-center mb-5">
                    <h2 className="text-2xl font-bold text-gray-800">
                        Residentes
                    </h2>

                    <button
                        className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow-md"
                        onClick={exportExcel}
                    >
                        📄 Exportar Excel
                    </button>
                </div>

                <table className="w-full border-collapse text-center text-[15px]">
                    <thead>
                        <tr className="bg-gray-100 text-gray-700">
                            <th className="p-3 border">#</th>
                            <th className="p-3 border">Nombre</th>
                            <th className="p-3 border">DNI</th>
                            <th className="p-3 border">Departamento</th>
                            <th className="p-3 border">Estado</th>
                        </tr>
                    </thead>

                    <tbody>
                        {paginatedData.map((r, index) => (
                            <tr
                                key={r.id}
                                className="hover:bg-gray-50 even:bg-gray-50 border-b"
                            >
                                <td className="p-3 font-semibold">
                                    {(page - 1) * itemsPerPage + index + 1}
                                </td>
                                <td className="p-3">{r.nombre}</td>
                                <td className="p-3">{r.dni ?? "-"}</td>
                                <td className="p-3">
                                    {r.departamento ?? "-"}
                                </td>
                                <td
                                    className={`p-3 font-bold ${
                                        r.estado === "activo"
                                            ? "text-green-600"
                                            : "text-red-600"
                                    }`}
                                >
                                    {r.estado}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Pagination */}
                <div className="flex justify-center gap-3 mt-6">
                    {Array.from({
                        length: Math.ceil(residentes.length / itemsPerPage),
                    }).map((_, i) => (
                        <button
                            key={i}
                            className={`px-3 py-1 rounded-lg shadow ${
                                page === i + 1
                                    ? "bg-blue-600 text-white"
                                    : "bg-gray-200 hover:bg-gray-300"
                            }`}
                            onClick={() => setPage(i + 1)}
                        >
                            {i + 1}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

/* ---------------- KPI component ---------------- */
function KPI({ title, value, icon, color }) {
    return (
        <div
            className={`${color} border rounded-2xl p-6 flex flex-col items-center justify-center shadow`}
        >
            <div className="text-4xl mb-2">{icon}</div>
            <p className="text-lg font-semibold text-gray-600">{title}</p>
            <p className="text-3xl font-bold mt-1">{value}</p>
        </div>
    );
}
