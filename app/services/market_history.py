from __future__ import annotations

import json
from pathlib import Path

from app.models import MarketHistoryData

PROJECT_DIR = Path(__file__).resolve().parents[2]
MARKET_HISTORY_FILE = PROJECT_DIR / "data" / "sp500_inversion_history.json"


def load_market_history(path: Path = MARKET_HISTORY_FILE) -> MarketHistoryData:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return MarketHistoryData.model_validate(payload)
