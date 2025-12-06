import { CheckCircle, User, IdCard, Home, Video } from "lucide-react";

export default function DatasetCard({ resident, selected, onSelect }) {
    return (
        <div
            onClick={() => onSelect(resident.id)}
            className={`cursor-pointer p-5 rounded-xl border transition-all shadow-sm flex justify-between items-center gap-4
                ${selected ? "border-blue-500 bg-blue-50" : "border-slate-200 bg-white hover:shadow-md"}
            `}
        >
            {/* Bloque de Información */}
            <div className="flex items-center gap-4 flex-1">
                {/* Foto o ícono */}
                <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center">
                    <User className="w-6 h-6 text-slate-600" />
                </div>

                <div className="flex flex-col">
                    <h3 className="text-slate-900 font-semibold text-lg">
                        {resident.nombre}
                    </h3>

                    <div className="flex items-center gap-3 text-slate-600 text-sm mt-1">
                        <span className="flex items-center gap-1">
                            <IdCard className="w-4 h-4" />
                            DNI: {resident.dni}
                        </span>

                        <span className="flex items-center gap-1">
                            <Home className="w-4 h-4" />
                            Dpto: {resident.departamento}
                        </span>
                    </div>

                    <div className="flex items-center gap-1 text-green-700 text-sm mt-1">
                        <Video className="w-4 h-4" />
                        <span>Video disponible</span>
                        <CheckCircle className="w-4 h-4" />
                    </div>
                </div>
            </div>

            {/* Checkbox */}
            <div>
                <input
                    type="checkbox"
                    checked={selected}
                    onChange={() => onSelect(resident.id)}
                    className="w-5 h-5 accent-blue-600 cursor-pointer"
                    onClick={(e) => e.stopPropagation()}
                />
            </div>
        </div>
    );
}
