from __future__ import annotations

import argparse
import time

from app.services.treasury import refresh_cached_curve


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh YieldLab Treasury curve cache")
    parser.add_argument("--attempts", type=int, default=3, help="maximum fetch attempts")
    parser.add_argument("--retry-delay", type=float, default=2.0, help="seconds between attempts")
    args = parser.parse_args()

    if args.attempts < 1:
        parser.error("--attempts must be at least 1")

    last_error: Exception | None = None
    for attempt in range(1, args.attempts + 1):
        try:
            curve = refresh_cached_curve()
            print(
                f"Treasury cache refreshed: {curve.as_of} "
                f"({len(curve.points)} maturities)"
            )
            return 0
        except RuntimeError as exc:
            last_error = exc
            print(f"Attempt {attempt}/{args.attempts} failed: {exc}")
            if attempt < args.attempts:
                time.sleep(max(args.retry_delay, 0.0))

    print(f"Treasury refresh failed; existing cache was left untouched: {last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
