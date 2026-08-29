from __future__ import annotations

import argparse
import base64
import hashlib
import re
from pathlib import Path


DATA_IMAGE = re.compile(
    r"data:image/(?P<mime>[a-zA-Z0-9.+-]+);base64,(?P<payload>[a-zA-Z0-9+/=]+)"
)
LOCAL_SCREENSHOT = re.compile(r'(?P<prefix>"src":")(?P<path>screenshots/[^"?]+)(?P<suffix>")')

EXTENSIONS = {
    "jpeg": "jpg",
    "jpg": "jpg",
    "png": "png",
    "webp": "webp",
    "gif": "gif",
    "svg+xml": "svg",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--asset-root",
        type=Path,
        help="Root containing screenshot paths referenced by the source HTML.",
    )
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    assets = args.output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        mime = match.group("mime").lower()
        payload = base64.b64decode(match.group("payload"), validate=True)
        digest = hashlib.sha256(payload).hexdigest()
        if digest in written:
            return written[digest]
        extension = EXTENSIONS.get(mime, mime.split("+")[0])
        relative = f"assets/{digest[:2]}/{digest}.{extension}"
        target = args.output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        written[digest] = relative
        return relative

    rendered, replacements = DATA_IMAGE.subn(replace, text)

    local_replacements = 0
    if args.asset_root:
        def replace_local(match: re.Match[str]) -> str:
            nonlocal local_replacements
            source = args.asset_root / match.group("path")
            payload = source.read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            extension = source.suffix.removeprefix(".").lower()
            relative = f"assets/{digest[:2]}/{digest}.{extension}"
            target = args.output / relative
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
            local_replacements += 1
            return f'{match.group("prefix")}{relative}{match.group("suffix")}'

        rendered = LOCAL_SCREENSHOT.sub(replace_local, rendered)

    (args.output / "index.html").write_text(rendered, encoding="utf-8")
    print(f"externalized={replacements}")
    print(f"local_screenshots={local_replacements}")
    print(f"unique_assets={len(written)}")


if __name__ == "__main__":
    main()
