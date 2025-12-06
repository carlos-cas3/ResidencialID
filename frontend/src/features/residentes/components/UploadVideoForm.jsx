import { useState } from "react";
import { uploadVideoResident } from "../services/residents.service";

export default function UploadVideoForm() {
    const [video, setVideo] = useState(null);
    const [nombre, setNombre] = useState("");
    const [dni, setDni] = useState("");
    const [departamento, setDepartamento] = useState("");

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("video", video);
        formData.append("nombre", nombre);
        formData.append("dni", dni);
        formData.append("departamento", departamento);

        await uploadVideoResident(formData);
        alert("Residente registrado");
    };

    return (
        <div className="bg-white shadow rounded-lg p-6 max-w-xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">
                Registrar Subiendo Video
            </h2>

            <input
                type="file"
                accept="video/*"
                onChange={(e) => setVideo(e.target.files[0])}
                className="border p-2 rounded w-full"
            />

            <div className="grid grid-cols-3 gap-4 mt-5">
                <input
                    className="border p-2 rounded"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />
                <input
                    className="border p-2 rounded"
                    placeholder="DNI"
                    value={dni}
                    onChange={(e) => setDni(e.target.value)}
                />
                <input
                    className="border p-2 rounded"
                    placeholder="Departamento"
                    value={departamento}
                    onChange={(e) => setDepartamento(e.target.value)}
                />
            </div>

            <button
                onClick={handleUpload}
                className="mt-6 bg-blue-600 text-white px-6 py-2 rounded"
            >
                Subir
            </button>
        </div>
    );
}
