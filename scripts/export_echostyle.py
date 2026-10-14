#!/usr/bin/env python3
"""Convert the benchmark JSON to a text-only EchoStyle-style prompt list.
Image-reference conditioning is intentionally NOT supported by this export.
"""
import argparse, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--input", default="manifests/real_300_planned.json")
ap.add_argument("--output", default="manifests/echostyle_text_only.json")
ap.add_argument("--limit", type=int, default=0)
args = ap.parse_args()
cases = json.loads((root/args.input).read_text())
if args.limit > 0: cases=cases[:args.limit]
result=[{"src_video_path": c["src_video_path"], "prompt": c["prompt"]} for c in cases]
out=root/args.output
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(f"Wrote {len(result)} text-only entries to {out}")
