#!/usr/bin/env python3
"""Download + normalize a fixed 50-video DAVIS real-motion evaluation split.
Video rights: CC BY-NC 4.0 declared by mirror; check original DAVIS exceptions.
"""
import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
DATASET = "emirkisa/DAVIS-2017-480p-mp4"

def probe(path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot decode {path}")
    n = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return n, fps

def extract_keyframes(root, path, name, n):
    cap = cv2.VideoCapture(str(path))
    target = root / "data/reference_frames_davis" / name
    target.mkdir(parents=True, exist_ok=True)
    paths = []
    for label, frame_idx in (("first", 0), ("middle", n // 2), ("last", n - 1)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError(f"Cannot decode {name}, frame {frame_idx}")
        out = target / f"{label}.png"
        cv2.imwrite(str(out), frame)
        paths.append(out.relative_to(root).as_posix())
        if label == "first":
            thumb = root / "data/preview/davis" / f"{name}.jpg"
            thumb.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(thumb), frame)
    cap.release()
    return paths

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--input-dir", type=Path, default=None, help="Directory of previously downloaded *_raw_24fps.mp4")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--verify-remote-list", action="store_true")
    ap.add_argument("--skip-errors", action="store_true")
    args = ap.parse_args()
    root = args.root.resolve()
    catalog = json.loads((root / "manifests/real_50_catalog.json").read_text())
    cases = json.loads((root / "manifests/real_300_planned.json").read_text())
    assert len(catalog) == 50 and len(cases) == 300
    if args.verify_remote_list and args.input_dir is None:
        from huggingface_hub import list_repo_files
        remote = set(list_repo_files(repo_id=DATASET, repo_type="dataset"))
        missing = [v["mirror_filename"] for v in catalog if v["mirror_filename"] not in remote]
        if missing:
            raise RuntimeError(f"Missing remote videos: {missing}")
        print("Verified all 50 remote filenames.")
    receipts = {}
    target_count = max(0, min(50, args.limit))
    for i, item in enumerate(catalog[:target_count], 1):
        name = item["sequence_name"]
        out = root / item["video_path"]
        try:
            if not out.exists():
                if args.input_dir:
                    source = args.input_dir / item["mirror_filename"]
                    if not source.is_file():
                        raise FileNotFoundError(source)
                else:
                    from huggingface_hub import hf_hub_download
                    source = Path(hf_hub_download(repo_id=DATASET, repo_type="dataset", filename=item["mirror_filename"]))
                out.parent.mkdir(parents=True, exist_ok=True)
                tmp = out.with_name(out.stem + ".partial.mp4")
                filt = "fps=24,scale=512:320:force_original_aspect_ratio=decrease,pad=512:320:(ow-iw)/2:(oh-ih)/2,setsar=1"
                cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                       "-vf", filt, "-frames:v", "49", "-an", "-c:v", "libx264", "-crf", "22",
                       "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)]
                try:
                    subprocess.run(cmd, check=True)
                    frames, fps = probe(tmp)
                    if frames != 49 or abs(fps - 24) > .1:
                        raise RuntimeError(f"Bad normalized clip {name}: {frames} frames at {fps}fps")
                    tmp.replace(out)
                finally:
                    tmp.unlink(missing_ok=True)
            n, fps = probe(out)
            if n != 49 or abs(fps - 24) > .1:
                raise RuntimeError(f"Invalid clip {name}: {n} frames at {fps:.3f}fps")
            refs = extract_keyframes(root, out, name, n)
            receipts[name] = dict(video_path=item["video_path"], source_filename=item["mirror_filename"],
                                  sha256=hashlib.sha256(out.read_bytes()).hexdigest(), frames=n, fps=fps,
                                  frame_paths=refs, license=item["license"])
            print(f"[{i}/{target_count}] {name}: ready", flush=True)
        except Exception as exc:
            if not args.skip_errors:
                raise
            print(f"[{i}/{target_count}] FAILED {name}: {exc}", flush=True)
    ready = []
    for case in cases:
        if case["source_sequence"] in receipts:
            entry = dict(case)
            entry["asset_status"] = "ready"
            entry["freevis_reference_frame_paths"] = receipts[case["source_sequence"]]["frame_paths"]
            ready.append(entry)
    m = root / "manifests"
    (m / "real_download_receipt.json").write_text(json.dumps(receipts, indent=2) + "\n")
    (m / "real_eval_available.json").write_text(json.dumps(ready, indent=2) + "\n")
    with (m / "real_eval_available.csv").open("w", newline="") as stream:
        cols = ["case_id", "content_id", "style_id", "dataset_split", "src_video_path", "style_image_path", "first_frame_mask_path", "prompt"]
        writer = csv.DictWriter(stream, fieldnames=cols)
        writer.writeheader()
        writer.writerows({k: c.get(k) for k in cols} for c in ready)
    print(f"Materialized {len(receipts)}/50 real videos, {len(ready)}/300 evaluation cases.")
    if target_count == 50 and len(receipts) != 50:
        raise RuntimeError("Incomplete 50-video evaluation set.")

if __name__ == "__main__":
    main()
