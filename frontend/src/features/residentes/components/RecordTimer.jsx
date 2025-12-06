export default function RecordTimer({ time, fps, frames }) {
    return (
        <div className="mt-4 flex items-center gap-6 text-gray-700">
            <div className="flex flex-col">
                <span className="text-xs font-semibold text-gray-500">
                    Tiempo
                </span>
                <span className="text-lg font-bold">{time}s</span>
            </div>

            <div className="flex flex-col">
                <span className="text-xs font-semibold text-gray-500">FPS</span>
                <span className="text-lg font-bold">{fps}</span>
            </div>

            <div className="flex flex-col">
                <span className="text-xs font-semibold text-gray-500">
                    Frames
                </span>
                <span className="text-lg font-bold">{frames}</span>
            </div>
        </div>
    );
}
