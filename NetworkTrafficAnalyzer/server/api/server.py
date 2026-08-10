import os
import sys
from pathlib import Path

# Add server directory to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(project_root / ".env")
except ImportError:
    pass

# Config Environment Variables
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DEFAULT_PACKET_COUNT = int(os.getenv("DEFAULT_PACKET_COUNT", "100"))
CAPTURES_DIR_NAME = os.getenv("CAPTURES_DIR", "captures")
CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS_RAW.split(",") if o.strip()]

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    from typing import Optional
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from analyzer import PacketFilter, TrafficStatistics, PacketCapture

if HAS_FASTAPI:
    app = FastAPI(
        title="Network Traffic Analyzer API",
        description="REST API server for capturing, analyzing network traffic, and exporting reports.",
        version="1.0.0"
    )

    # Enable CORS for cross-origin deployments
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global in-memory statistics store
    latest_stats = TrafficStatistics()

    class CaptureRequest(BaseModel):
        count: Optional[int] = DEFAULT_PACKET_COUNT
        protocol: Optional[str] = None
        host: Optional[str] = None
        port: Optional[int] = None
        output_file: Optional[str] = f"{CAPTURES_DIR_NAME}/capture.pcap"

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "host": HOST,
            "port": PORT,
            "default_count": DEFAULT_PACKET_COUNT
        }

    @app.get("/stats")
    def get_statistics():
        """Retrieve latest traffic analysis statistics."""
        return latest_stats.get_summary()

    def run_capture_task(count: int, protocol: str, host: str, port: int, output_file: str):
        global latest_stats
        latest_stats = TrafficStatistics()
        packet_filter = PacketFilter(protocol=protocol, host=host, port=port)
        capturer = PacketCapture(packet_filter=packet_filter, stats=latest_stats)
        capturer.capture(count=count)
        if output_file:
            capturer.save_pcap(output_file)

    @app.post("/capture")
    def start_capture(req: CaptureRequest, background_tasks: BackgroundTasks):
        """Trigger a network packet capture task in background."""
        background_tasks.add_task(
            run_capture_task,
            req.count or DEFAULT_PACKET_COUNT,
            req.protocol,
            req.host,
            req.port,
            req.output_file or f"{CAPTURES_DIR_NAME}/capture.pcap"
        )
        payload = req.model_dump() if hasattr(req, "model_dump") else req.dict()
        return {
            "message": "Packet capture initiated",
            "config": payload
        }

    @app.get("/captures")
    def list_captures():
        """List captured PCAP files in captures directory."""
        captures_dir = project_root / CAPTURES_DIR_NAME
        if not captures_dir.exists():
            return {"files": []}
        files = [f.name for f in captures_dir.glob("*.pcap")]
        return {"files": files}

    @app.get("/captures/download/{filename}")
    def download_pcap(filename: str):
        """Download a saved PCAP file."""
        file_path = project_root / CAPTURES_DIR_NAME / filename
        if not file_path.exists() or not filename.endswith(".pcap"):
            raise HTTPException(status_code=404, detail="PCAP file not found")
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.tcpdump.pcap"
        )

    # Mount static client frontend if present
    client_dir = project_root.parent / "client"
    if not client_dir.exists():
        client_dir = project_root / "client"
    if client_dir.exists():
        app.mount("/", StaticFiles(directory=str(client_dir), html=True), name="client")

    def start_server(host=HOST, port=PORT):
        import uvicorn
        uvicorn.run(app, host=host, port=port)

else:
    def start_server(host=HOST, port=PORT):
        print("FastAPI / Uvicorn not installed. Please install requirements.txt to run API server.")


if __name__ == "__main__":
    start_server()
