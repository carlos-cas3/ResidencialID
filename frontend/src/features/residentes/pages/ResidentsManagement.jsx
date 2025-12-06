import { useState } from "react";
import ResidentsTable from "../components/ResidentsTable";
import ResidentStatsCards from "../components/ResidentStatsCards";
import RecordVideoForm from "../components/RecordVideoForm";
import UploadVideoForm from "../components/UploadVideoForm";

export default function ResidentsManagement() {
    const [tab, setTab] = useState("resumen");

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">Gestión de Residentes</h1>

            {/* Tabs */}
            <div className="flex space-x-4 border-b mb-6">
                {["resumen", "grabar", "subir"].map((t) => (
                    <button
                        key={t}
                        onClick={() => setTab(t)}
                        className={`pb-2 px-3 border-b-2 ${
                            tab === t
                                ? "border-blue-600 text-blue-600 font-semibold"
                                : "border-transparent text-gray-500"
                        }`}
                    >
                        {t === "resumen" && "🧾 Vista General"}
                        {t === "grabar" && "📸 Registrar Grabando"}
                        {t === "subir" && "📤 Registrar Subiendo Video"}
                    </button>
                ))}
            </div>

            {/* Contenido */}
            {tab === "resumen" && (
                <>
                    <ResidentStatsCards />
                    <ResidentsTable />
                </>
            )}

            {tab === "grabar" && <RecordVideoForm />}

            {tab === "subir" && <UploadVideoForm />}
        </div>
    );
}
