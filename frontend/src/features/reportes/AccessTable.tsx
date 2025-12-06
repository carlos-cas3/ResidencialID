import React, { useEffect, useMemo, useState } from "react";
import * as XLSX from "xlsx";

type Acceso = {
    id: number;
    tipo: string;
    fecha: string;
    hora: string;
    imagen_url?: string | null;
    residente_id?: number | null;
    nombre_residente?: string;
};

export default function AccessTable() {
    const [data, setData] = useState<Acceso[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // filtros
    const [search, setSearch] = useState("");
    const [tipoFilter, setTipoFilter] = useState("all");
    const [knownFilter, setKnownFilter] = useState("all");

    // paginación
    const [page, setPage] = useState(1);
    const pageSize = 10;

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const res = await fetch("http://localhost:5000/accesos/");
                const json = await res.json();
                setData(json.data || []);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Filtrado
    const filtered = useMemo(() => {
        let rows = [...data];

        if (search.trim()) {
            const q = search.toLowerCase();
            rows = rows.filter(
                (r) =>
                    (r.nombre_residente ?? "").toLowerCase().includes(q) ||
                    (r.tipo ?? "").toLowerCase().includes(q) ||
                    (r.fecha ?? "").toLowerCase().includes(q)
            );
        }

        if (tipoFilter !== "all") {
            rows = rows.filter((r) => r.tipo === tipoFilter);
        }

        if (knownFilter !== "all") {
            const isKnown = knownFilter === "yes";
            rows = rows.filter(
                (r) => Boolean(r.residente_id) === isKnown
            );
        }

        return rows;
    }, [data, search, tipoFilter, knownFilter]);

    const totalPages = Math.ceil(filtered.length / pageSize);

    const pageRows = useMemo(() => {
        const start = (page - 1) * pageSize;
        return filtered.slice(start, start + pageSize);
    }, [filtered, page]);

    // Exportar Excel
    const exportExcel = () => {
        const wsData = filtered.map((r) => ({
            ID: r.id,
            Tipo: r.tipo,
            Fecha: r.fecha,
            Hora: r.hora,
            Residente: r.nombre_residente,
            Imagen: r.imagen_url,
        }));

        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(wsData);
        XLSX.utils.book_append_sheet(wb, ws, "Accesos");

        XLSX.writeFile(wb, `Accesos_${Date.now()}.xlsx`);
    };

    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            {/* Filtros */}
            <div className="flex flex-wrap gap-4 mb-4 justify-between">
                <input
                    value={search}
                    onChange={(e) => {
                        setSearch(e.target.value);
                        setPage(1);
                    }}
                    placeholder="Buscar por nombre..."
                    className="px-3 py-2 border rounded-md"
                />

                <select
                    value={tipoFilter}
                    onChange={(e) => {
                        setTipoFilter(e.target.value);
                        setPage(1);
                    }}
                    className="px-3 py-2 border rounded-md"
                >
                    <option value="all">Todos los tipos</option>
                    <option value="Entrando">Entrando</option>
                    <option value="Saliendo">Saliendo</option>
                    <option value="NoDetectado">NoDetectado</option>
                </select>

                <select
                    value={knownFilter}
                    onChange={(e) => {
                        setKnownFilter(e.target.value);
                        setPage(1);
                    }}
                    className="px-3 py-2 border rounded-md"
                >
                    <option value="all">Todos (conocidos y desconocidos)</option>
                    <option value="yes">Solo residentes conocidos</option>
                    <option value="no">Solo desconocidos</option>
                </select>

                <button
                    onClick={exportExcel}
                    className="px-4 py-2 bg-slate-900 text-white rounded-md"
                >
                    Exportar Excel
                </button>
            </div>

            {/* Tabla */}
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-4 py-2 text-left text-sm">ID</th>
                            <th className="px-4 py-2 text-left text-sm">Tipo</th>
                            <th className="px-4 py-2 text-left text-sm">Fecha</th>
                            <th className="px-4 py-2 text-left text-sm">Hora</th>
                            <th className="px-4 py-2 text-left text-sm">Residente</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr>
                                <td colSpan={5} className="text-center p-4">
                                    Cargando...
                                </td>
                            </tr>
                        ) : error ? (
                            <tr>
                                <td colSpan={5} className="text-center p-4 text-red-500">
                                    Error: {error}
                                </td>
                            </tr>
                        ) : pageRows.length === 0 ? (
                            <tr>
                                <td colSpan={5} className="text-center p-4">
                                    No hay registros.
                                </td>
                            </tr>
                        ) : (
                            pageRows.map((r) => (
                                <tr key={r.id} className="border-t">
                                    <td className="px-4 py-2">{r.id}</td>
                                    <td className="px-4 py-2">{r.tipo}</td>
                                    <td className="px-4 py-2">{r.fecha}</td>
                                    <td className="px-4 py-2">{r.hora}</td>
                                    <td className="px-4 py-2">
                                        {r.residente_id
                                            ? r.nombre_residente
                                            : "DESCONOCIDO"}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* paginación */}
            <div className="flex justify-between items-center mt-4">
                <div>
                    Página {page} de {totalPages}
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={() => setPage((p) => Math.max(1, p - 1))}
                        disabled={page === 1}
                        className="px-3 py-1 border rounded disabled:opacity-50"
                    >
                        Anterior
                    </button>
                    <button
                        onClick={() =>
                            setPage((p) => Math.min(totalPages, p + 1))
                        }
                        disabled={page === totalPages}
                        className="px-3 py-1 border rounded disabled:opacity-50"
                    >
                        Siguiente
                    </button>
                </div>
            </div>
        </div>
    );
}
