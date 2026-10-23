#!/usr/bin/env python3
"""Generate PNG diagrams from Mermaid .mmd files using mermaid.ink API."""
import base64
import urllib.request
import io
import sys
import os

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip3 install Pillow")
    sys.exit(1)


def mermaid_to_png_kroki(mmd_file, png_file):
    """Use kroki.io POST API — no URL length limits."""
    with open(mmd_file, 'r') as f:
        code = f.read()

    # kroki.io accepts a zlib-compressed, base64url-encoded body via GET,
    # or raw mermaid source via POST to /mermaid/png
    url = "https://kroki.io/mermaid/png"
    data = code.encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        method='POST',
        headers={
            'Content-Type': 'text/plain',
            'Accept': 'image/png',
            'User-Agent': 'Mozilla/5.0',
        }
    )
    print(f"  POST {url} ({len(data)} bytes) ...")
    with urllib.request.urlopen(req, timeout=90) as response:
        raw = response.read()
    img = Image.open(io.BytesIO(raw))
    img.save(png_file, 'PNG')
    sz = os.path.getsize(png_file)
    print(f"  Saved: {png_file} ({img.size[0]}x{img.size[1]}px, {sz//1024}KB)")
    return True


def mermaid_to_png(mmd_file, png_file):
    with open(mmd_file, 'r') as f:
        code = f.read()

    # First try mermaid.ink GET (plain base64url) — works for shorter diagrams
    encoded = base64.urlsafe_b64encode(code.encode('utf-8')).decode('utf-8').rstrip('=')
    url = f"https://mermaid.ink/img/{encoded}"
    print(f"[{mmd_file}] mermaid.ink URL length: {len(url)}")

    if len(url) <= 8000:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                data = response.read()
            img = Image.open(io.BytesIO(data))
            img.save(png_file, 'PNG')
            sz = os.path.getsize(png_file)
            print(f"  Saved via mermaid.ink: {png_file} ({img.size[0]}x{img.size[1]}px, {sz//1024}KB)")
            return True
        except urllib.error.HTTPError as e:
            print(f"  mermaid.ink HTTP {e.code} — falling back to kroki.io ...")
        except Exception as e:
            print(f"  mermaid.ink error: {e} — falling back to kroki.io ...")

    # Fall back to kroki.io POST for large diagrams
    print(f"  Using kroki.io POST fallback ...")
    return mermaid_to_png_kroki(mmd_file, png_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: generate_diagrams.py <file.mmd> [file2.mmd ...]")
        sys.exit(1)

    diagrams_dir = os.getcwd()
    ok = True
    for mmd_arg in sys.argv[1:]:
        mmd_path = mmd_arg if os.path.isabs(mmd_arg) else os.path.join(diagrams_dir, mmd_arg)
        png_path = os.path.splitext(mmd_path)[0] + '.png'
        print(f"\nGenerating: {mmd_path} -> {png_path}")
        if not mermaid_to_png(mmd_path, png_path):
            ok = False
    print("\nAll done!" if ok else "\nSome diagrams failed.")
    sys.exit(0 if ok else 1)
