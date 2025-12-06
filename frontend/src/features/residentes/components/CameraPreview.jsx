export default function CameraPreview({ videoRef }) {
    return (
        <div className="w-full flex justify-center">
            <video
                ref={videoRef}
                autoPlay
                className="rounded-lg border shadow max-w-lg"
            ></video>
        </div>
    );
}
