from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


MAX_SESSION_LOG_FILES = 5


class SessionLogManager:
    def __init__(self, backend_dir: Path):
        self.backend_dir = backend_dir
        self.logs_dir = backend_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.backend_logger = logging.getLogger("prosada")
        self.backend_logger.setLevel(logging.INFO)
        self.current_backend_log: Path | None = None

    def _prune(self, prefix: str, keep: int = MAX_SESSION_LOG_FILES) -> None:
        files = sorted(
            self.logs_dir.glob(f"{prefix}-*.log"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for stale in files[keep:]:
            stale.unlink(missing_ok=True)

    def start_backend_session(self, session_id: str) -> Path:
        path = self.logs_dir / f"backend-session-{session_id}.log"
        # Avoid duplicate handlers if startup hook runs multiple times under reload.
        if not any(
            isinstance(h, logging.FileHandler) and Path(getattr(h, "baseFilename", "")).resolve() == path.resolve()
            for h in self.backend_logger.handlers
        ):
            file_handler = logging.FileHandler(path, encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
            )
            self.backend_logger.addHandler(file_handler)
        self.current_backend_log = path
        self._prune("backend-session")
        return path

    def append_frontend_logs(self, session_id: str, entries: Iterable[Dict[str, Any]]) -> Path:
        path = self.logs_dir / f"frontend-session-{session_id}.log"
        with path.open("a", encoding="utf-8") as fh:
            for entry in entries:
                record = {
                    "receivedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "level": entry.get("level", "info"),
                    "source": entry.get("source", "frontend"),
                    "message": entry.get("message", ""),
                    "timestamp": entry.get("timestamp"),
                    "context": entry.get("context", {}),
                }
                fh.write(json.dumps(record, ensure_ascii=True) + "\n")
        self._prune("frontend-session")
        return path

    def list_recent_logs(self) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        for path in sorted(self.logs_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True):
            rows.append(
                {
                    "name": path.name,
                    "path": str(path),
                    "modifiedAt": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),
                }
            )
        return rows

