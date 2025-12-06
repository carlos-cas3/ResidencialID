import { useState } from "react";

export default function EditModal({ visible, residente, onClose, onSave }) {
    if (!visible) return null;

    const [form, setForm] = useState({
        nombre: residente.nombre,
        dni: residente.dni,
        departamento: residente.departamento,
        video_url: residente.video_url || ""
    });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    return (
        <div className="fixed inset-0 bg-black/40 flex justify-center items-center">
            <div className="bg-white rounded-lg p-6 w-96 shadow-lg">
                <h3 className="text-lg font-bold mb-4">Editar Residente</h3>

                <label className="font-semibold">Nombre</label>
                <input
                    name="nombre"
                    value={form.nombre}
                    onChange={handleChange}
                    className="w-full border p-2 rounded mb-2"
                />

                <label className="font-semibold">DNI</label>
                <input
                    name="dni"
                    value={form.dni}
                    onChange={handleChange}
                    className="w-full border p-2 rounded mb-2"
                />

                <label className="font-semibold">Departamento</label>
                <input
                    name="departamento"
                    value={form.departamento}
                    onChange={handleChange}
                    className="w-full border p-2 rounded mb-2"
                />

                <label className="font-semibold">Video URL</label>
                <input
                    name="video_url"
                    value={form.video_url}
                    onChange={handleChange}
                    className="w-full border p-2 rounded mb-2"
                />

                <div className="flex justify-end space-x-3 mt-4">
                    <button
                        onClick={onClose}
                        className="px-3 py-1 border rounded"
                    >
                        Cancelar
                    </button>

                    <button
                        onClick={() => onSave(residente.id, form)}
                        className="px-3 py-1 bg-blue-600 text-white rounded"
                    >
                        Guardar
                    </button>
                </div>
            </div>
        </div>
    );
}
