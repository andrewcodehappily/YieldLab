from __future__ import annotations

import argparse
import time

from app.services.treasury import refresh_treasury_data


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh YieldLab Treasury data")
    parser.add_argument("--attempts", type=int, default=3, help="maximum fetch attempts")
    parser.add_argument("--retry-delay", type=float, default=2.0, help="seconds between attempts")
    parser.add_argument("--months", type=int, default=2, help="number of recent Treasury months to ingest")
    args = parser.parse_args()

    if args.attempts < 1:
        parser.error("--attempts must be at least 1")
    if args.months < 1:
        parser.error("--months must be at least 1")

    last_error: Exception | None = None
    for attempt in range(1, args.attempts + 1):
        try:
            curve, history = refresh_treasury_data(months=args.months)
            print(
                f"Treasury data refreshed: {curve.as_of} "
                f"({len(curve.points)} maturities, {len(history)} historical curves)"
            )
            return 0
        except RuntimeError as exc:
            last_error = exc
            print(f"Attempt {attempt}/{args.attempts} failed: {exc}")
            if attempt < args.attempts:
                time.sleep(max(args.retry_delay, 0.0))

    print(f"Treasury refresh failed; existing data was left untouched: {last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
