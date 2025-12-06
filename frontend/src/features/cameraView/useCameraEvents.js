import { useEffect, useState } from "react";

export default function useCameraEvents() {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const source = new EventSource("http://localhost:8000/events");

        source.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setLogs((prev) => [data, ...prev]);
        };

        return () => source.close();
    }, []);

    return logs;
}
