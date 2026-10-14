#!/usr/bin/env python3
"""Validate pinned benchmark metadata, optionally requiring 50 downloaded real videos."""
import argparse
import json
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parents[1]
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--require-real", action="store_true")
    ap.add_argument("--require-styles", action="store_true")
    args = ap.parse_args()
    root = args.root
    get = lambda name: json.loads((root / "manifests" / name).read_text())
    videos = get("real_50_catalog.json")
    styles = get("styles.json")
    cases = get("real_300_planned.json")
    quick = get("real_50_screening_planned.json")
    assert len(videos) == len({x["sequence_name"] for x in videos}) == 50
    assert len(styles) == len({x["id"] for x in styles}) == 6
    assert len(cases) == len({x["case_id"] for x in cases}) == 300
    assert len(quick) == len({x["content_id"] for x in quick}) == 50
    assert {x["style_id"] for x in cases} == {x["id"] for x in styles}
    assert {x["content_id"] for x in cases} == {x["id"] for x in videos}
    assert {x["dataset_split"] for x in cases} <= {"train", "val"}
    if args.require_styles or args.require_real:
        for s in styles:
            p = root / s["reference_image"]
            assert p.is_file(), f"Missing style reference {p}; run scripts/generate_styles.py or install companion assets."
    if args.require_real:
        for v in videos:
            p = root / v["video_path"]
            assert p.is_file(), f"Missing downloaded video {p}"
            cap = cv2.VideoCapture(str(p))
            assert cap.isOpened(), f"Cannot decode {p}"
            n = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            assert n == 49 and abs(fps - 24) < .1, f"Invalid video {p}: {n} frames / {fps} fps"
    print("PASS: 50 unique video IDs, 6 styles, 300 cases, 50-case screening split.")
    print("Note: without --require-real, this only validates manifests, NOT media availability.")
if __name__ == "__main__":
    main()
