import { useEffect, useState } from "react";
import Avatar from "./Avatar";
import EditModal from "./EditModal";

export default function ResidentsTable() {
    const [residentes, setResidentes] = useState([]);
    const [page, setPage] = useState(1);
    const [orderBy, setOrderBy] = useState("alfabetico");
    const [modalVisible, setModalVisible] = useState(false);
    const [residenteActual, setResidenteActual] = useState(null);
    const perPage = 10;

    const loadResidentes = () => {
        fetch("http://localhost:5000/residentes")
            .then((res) => res.json())
            .then((res) => {
                const activos = res.data.filter((r) => r.estado === "activo");
                setResidentes(activos);
            })
            .catch((err) => console.error("Error cargando residentes", err));
    };

    useEffect(() => {
        loadResidentes();
    }, []);

    const ordenar = (lista) => {
        if (orderBy === "alfabetico") {
            return [...lista].sort((a, b) => a.nombre.localeCompare(b.nombre));
        }
        if (orderBy === "id_desc") {
            return [...lista].sort((a, b) => b.id - a.id);
        }
        if (orderBy === "id_asc") {
            return [...lista].sort((a, b) => a.id - b.id);
        }
        return lista;
    };

    const residentesOrdenados = ordenar(residentes);

    const start = (page - 1) * perPage;
    const paginated = residentesOrdenados.slice(start, start + perPage);
    const totalPages = Math.ceil(residentes.length / perPage);

    const handleEdit = async (id, nuevosValores) => {
        await fetch(`http://localhost:5000/residentes/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevosValores),
        });

        setModalVisible(false);
        loadResidentes();
    };

    const handleDelete = async (id) => {
        await fetch(`http://localhost:5000/residentes/${id}`, {
            method: "DELETE",
        });
        loadResidentes();
    };

    return (
        <div className="bg-white shadow rounded-lg p-4 mt-6">
            <h2 className="text-xl font-bold mb-4">Lista de Residentes</h2>

            <div className="mb-4">
                <label className="mr-2 font-semibold">Ordenar por:</label>
                <select
                    value={orderBy}
                    onChange={(e) => {
                        setOrderBy(e.target.value);
                        setPage(1);
                    }}
                    className="border p-1 rounded"
                >
                    <option value="alfabetico">Alfabético (A–Z)</option>
                    <option value="id_desc">
                        Ingresados (Nuevo → Antiguo)
                    </option>
                    <option value="id_asc">Ingresados (Antiguo → Nuevo)</option>
                </select>
            </div>

            <table className="w-full text-left border-collapse">
                <thead>
                    <tr className="border-b text-gray-600">
                        <th className="p-2">Foto</th>
                        <th className="p-2">Nombre</th>
                        <th className="p-2">DNI</th>
                        <th className="p-2">Departamento</th>
                        <th className="p-2">Video</th>
                        <th className="p-2">Acciones</th>
                    </tr>
                </thead>

                <tbody>
                    {Array.from({ length: perPage }).map((_, i) => {
                        const r = paginated[i]; 
                        return (
                            <tr key={i} className="border-b h-16">
                                <td className="p-2">
                                    {r ? <Avatar name={r.nombre} /> : null}
                                </td>
                                <td className="p-2">{r ? r.nombre : ""}</td>
                                <td className="p-2">{r ? r.dni : ""}</td>
                                <td className="p-2">
                                    {r ? r.departamento : ""}
                                </td>
                                <td className="p-2">
                                    {r && r.video_url ? (
                                        <a
                                            href={r.video_url}
                                            target="_blank"
                                            className="text-blue-500 underline"
                                        >
                                            Ver video
                                        </a>
                                    ) : (
                                        ""
                                    )}
                                </td>
                                <td className="p-2">
                                    {r ? (
                                        JSON.parse(r.necesita_entrenamiento) ? (
                                            <span className="px-2 py-1 text-xs bg-yellow-200 text-yellow-800 rounded-full">
                                                Pendiente
                                            </span>
                                        ) : (
                                            <span className="px-2 py-1 text-xs bg-green-200 text-green-800 rounded-full">
                                                Entrenado
                                            </span>
                                        )
                                    ) : (
                                        ""
                                    )}
                                </td>
                                <td className="p-2 space-x-2">
                                    {r ? (
                                        <>
                                            <button
                                                className="text-blue-500"
                                                onClick={() => {
                                                    setResidenteActual(r);
                                                    setModalVisible(true);
                                                }}
                                            >
                                                Editar
                                            </button>
                                            <button
                                                className="text-red-500"
                                                onClick={() => {
                                                    if (
                                                        confirm(
                                                            "¿Eliminar este residente?"
                                                        )
                                                    )
                                                        handleDelete(r.id);
                                                }}
                                            >
                                                Eliminar
                                            </button>
                                        </>
                                    ) : null}
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>

            <div className="flex justify-center mt-4 space-x-3">
                <button
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    className="px-3 py-1 border rounded"
                >
                    Anterior
                </button>

                <span>
                    Página {page} de {totalPages}
                </span>

                <button
                    onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                    className="px-3 py-1 border rounded"
                >
                    Siguiente
                </button>
            </div>

            {/* MODAL DE EDICIÓN */}
            <EditModal
                visible={modalVisible}
                residente={residenteActual}
                onClose={() => setModalVisible(false)}
                onSave={handleEdit}
            />
        </div>
    );
}
