from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def _ensure_repo_on_syspath() -> Path:
    """
    Allows running via `python animation_agent\\agent.py ...` (script mode)
    as well as `python -m animation_agent.agent ...` (module mode).
    """
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    return repo_root


_REPO_ROOT = _ensure_repo_on_syspath()

from graph import build_graph


def _load_env_fallback(dotenv_path: Path) -> None:
    """
    Some Windows setups can have dotenv parsing issues (encoding/BOM).
    This ensures GOOGLE_API_KEY is loaded if present in the file.
    """
    if os.getenv("GOOGLE_API_KEY"):
        return
    if not dotenv_path.exists():
        return
    try:
        raw = dotenv_path.read_text(encoding="utf-8-sig")
    except Exception:
        return
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and v and not os.getenv(k):
            os.environ[k] = v


def main() -> int:
    # Load .env from repo root (one directory up from animation_agent/)
    dotenv_path = _REPO_ROOT / ".env"
    load_dotenv(dotenv_path=dotenv_path, override=False)
    _load_env_fallback(dotenv_path)

    user_prompt = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else "Explain Fourier Series"

    app = build_graph()
    state = {"prompt": user_prompt}
    result = app.invoke(state)

    final_video = result.get("final_video")
    if final_video:
        print("Final video:", final_video)
        return 0

    print("No output video was produced.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())