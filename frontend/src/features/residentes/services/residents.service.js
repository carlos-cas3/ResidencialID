const API_URL = "http://localhost:5000/residentes";

export async function uploadRecordedResident(formData) {
    return fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
    });
}

export async function uploadVideoResident(formData) {
    return fetch(`${API_URL}/upload/`, {
        method: "POST",
        body: formData,
    });
}
