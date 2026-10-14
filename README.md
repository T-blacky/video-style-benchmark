# Video Style Transfer Benchmark

A reproducible **training-free video style-transfer evaluation protocol** with a fixed DAVIS-2017 content split, reference-style images, and method-aware manifests. Informed by [UniVST](https://arxiv.org/abs/2410.20084), [FreeViS](https://arxiv.org/abs/2510.01686), [TokenFlow](https://arxiv.org/abs/2307.10373), and [EchoStyle](https://github.com/HKUST-C4G/EchoStyle).

> **Availability / reproducibility notice:** This repository includes **six real artwork style-reference PNGs** in `data/styles/`. The 50 DAVIS video identities and 300 planned cases are documented, but actual DAVIS MP4s must be downloaded separately.

## What is provided?

| Component | Count | Availability in GitHub |
|---|---:|---|
| Fixed independent DAVIS source sequences | 50 | IDs, splits and downloadable filenames in JSON; MP4s require local download |
| Video–style testing cases | 300 | Full JSON manifest, all combinations |
| Fast screening split | 50 | One case per video, rotating through six styles |
| Reference style categories | 6 | Six curated art-reference PNGs included in `data/styles/` |
| Curated artwork reference PNGs | 6 | All six installed in GitHub; individual artwork credits in ASSET_LICENSES.md |
| Offline synthetic smoke video clips | 7 | Only in companion ZIP, not this checkout |
| DAVIS object masks | Optional | Original annotations downloaded separately; not bundled |
| Stylized target video / ground truth | 0 | No paired ground truth; do not claim reconstruction accuracy |

Six visually distinct reference categories are **ink wash**, **oil with pronounced visible brushwork**, **watercolor**, **comic-book illustration**, **cubism**, and **pixel art**. The actual images are documented works from Wikimedia Commons, not the earlier schematic drawings. **Unlike the previous prototypes, these are different artworks, not the same scene in six styles.** This improves visual style separability but introduces content/subject confounding, so treat this as a curated style-reference set, not a controlled same-content style study.

## Quick start (download 50 real videos)

Prerequisites: Python ≥ 3.10, FFmpeg with H.264 encode support installed on your PATH, internet access for Hugging Face (or local mirror video files). This dataset mirror declares **CC BY-NC 4.0**, noncommercial with attribution; check DAVIS source-specific rights before redistributing.

```bash
git clone https://github.com/T-blacky/video-style-benchmark.git
cd video-style-benchmark
python -m pip install -r requirements-download.txt
python scripts/validate.py
python scripts/prepare_davis.py --verify-remote-list
python scripts/validate.py --require-real
```

The downloader retrieves 50 distinct raw DAVIS-2017 MP4 sequences via [emirkisa/DAVIS-2017-480p-mp4](https://huggingface.co/datasets/emirkisa/DAVIS-2017-480p-mp4), then normalizes each to 49 frames, 512×320, 24 fps, MP4 H.264. No overlay videos are used. First/middle/last **unstylized** frames are also extracted.

**Pilot run for 2 videos:**

```bash
python scripts/prepare_davis.py --limit 2
python scripts/validate.py
```

A pilot run is not the complete benchmark; `--require-real` requires all 50. To use locally downloaded mirror MP4 files, run `python scripts/prepare_davis.py --input-dir /your/mp4/directory`.

### Preview: bundled curated artwork references

The six images below now reference actual paintings/comic/pixel art. They replace the earlier low-detail procedural placeholders. **Image subjects differ**, so evaluate style fidelity together with content leakage, not with pixel-level alignment.

| Ink wash | Thick oil impasto | Watercolor |
|---|---|---|
| ![Ink](data/styles/ink_wash.png) | ![Oil](data/styles/oil_impasto.png) | ![Watercolor](data/styles/watercolor.png) |

| Comic cel | Cubism | Pixel art |
|---|---|---|
| ![Comic](data/styles/comic_cel.png) | ![Cubism](data/styles/cubism.png) | ![Pixel](data/styles/pixel_art.png) |

### Reference-artwork sources and regeneration

Images in `data/styles/` are now part of the repository. For provenance, see [ASSET_LICENSES.md](ASSET_LICENSES.md) and `manifests/styles.json`. To refresh images from the same documented Wikimedia source artworks:

```bash
python -m pip install Pillow requests
python scripts/install_style_artworks.py
```

The six reference images are normalized to 768×768 with padding to avoid cropping the artwork. `scripts/generate_styles.py` is kept solely for legacy compatibility and **must not replace these curated images**. The GitHub Actions image installer ensures new source images are verified before being committed.

The v0.2 companion ZIP's separately generated AI references are **different assets** and should not be mixed with the Wikimedia reference set during comparison. The original 7 smoke-test videos remain optional and external.


## Input schema

`manifests/real_300_planned.json` contains records like:

```json
{
  "case_id": "davis_bear__ink_wash",
  "source_sequence": "bear",
  "style_id": "ink_wash",
  "src_video_path": "data/real_videos/bear.mp4",
  "style_image_path": "data/styles/ink_wash.png",
  "first_frame_mask_path": null,
  "prompt": "..."
}
```

- `src_video_path`: original real-motion video, **not** stylized ground truth.
- `style_image_path`: arbitrarily selected visual style reference.
- `prompt`: consistent English text description usable by text-only baselines.
- `first_frame_mask_path`: `null` for global stylization; use original DAVIS object masks (externally sourced) when evaluating localized edits.
- `freevis_reference_frame_paths`: first/middle/last *content* keyframes saved by the download script. These frames are **NOT pre-stylized FreeViS references**. A FreeViS adapter must synthesize styled keyframes.
- `asset_status`: `planned_not_bundled` until sources and local images are materialized. The downloader creates `manifests/real_eval_available.json` after successful video preparation.

The `manifests/real_50_screening_planned.json` split uses **exactly 50 distinct video sequences**, each with one style chosen round-robin. Use the full 300 cases for balanced style-by-video analysis.

## Research-method alignment

| Approach | Conditioning | How to use this benchmark |
|---|---|---|
| **UniVST** ([paper](https://arxiv.org/abs/2410.20084)) | Video + style image, optional mask | Use the same source videos/styles, bring in original DAVIS mask annotations for local transfer |
| **FreeViS** ([paper](https://arxiv.org/abs/2510.01686)) | Video, arbitrary style image, additional method-generated styled references | Select first/middle/last content frames and generate their stylized variants in the method adapter |
| **TokenFlow** ([paper](https://arxiv.org/abs/2307.10373)) | Video + *text* editing prompt | Compare as a clearly labeled **text-conditioned** baseline, not a matched image-conditioned method |
| **EchoStyle** ([repository](https://github.com/HKUST-C4G/EchoStyle)) | Published test JSON uses `src_video_path` + `prompt` | Run `python scripts/export_echostyle.py` for a text-only adapter; a separate image-conditioned adapter is needed |

This benchmark design is **independent**; it is not the official UniVST, FreeViS, TokenFlow or EchoStyle evaluation set. See [PAPERS_AND_METHODS.md](PAPERS_AND_METHODS.md) for the method discussion.

## Proposed evaluation protocol

There are no reference stylized target videos, so **do not calculate output-versus-ground-truth video PSNR/SSIM** as if paired ground truth exists. Instead track style fidelity (reference comparison or blinded human ratings), content and motion retention, temporal consistency / flicker, stylization artifacts, failure rate and wall-clock runtime. Track inference settings, model commit, seed and GPU. Report results stratified by the **50 unique source videos** and six styles. Global-style comparisons must not be compared directly to local-mask tasks.

Detailed rules: [EVALUATION_PROTOCOL.md](EVALUATION_PROTOCOL.md) · [DATA_CARD.md](DATA_CARD.md) · [ASSET_LICENSES.md](ASSET_LICENSES.md).

## Directory layout

```text
.
├── README.md
├── PAPERS_AND_METHODS.md
├── EVALUATION_PROTOCOL.md
├── DATA_CARD.md
├── ASSET_LICENSES.md
├── manifests/
│   ├── real_50_catalog.json
│   ├── real_300_planned.json
│   ├── real_50_screening_planned.json
│   └── styles.json
├── scripts/
│   ├── prepare_davis.py
│   ├── generate_styles.py
│   ├── export_echostyle.py
│   └── validate.py
└── data/
    ├── styles/              # six curated real-artwork style PNGs (already included)
    ├── real_videos/         # downloaded locally, gitignored
    └── reference_frames_davis/ # created on download
```

### License and attribution

Code in this repository is MIT licensed. That **does not apply** to DAVIS or other third-party videos. DAVIS footage comes via the linked community conversion with the declared **CC BY-NC 4.0** restriction and possible per-source exceptions. The included reference images are real artworks with individual public-domain or Creative Commons notices; the pixel-art example is CC BY-SA 4.0 and requires attribution. This image licensing is **separate** from the MIT code license. See ASSET_LICENSES.md. Keep provenance for every experimental input and preserve appropriate citation and usage restrictions.

### References

- UniVST: https://arxiv.org/abs/2410.20084
- FreeViS: https://arxiv.org/abs/2510.01686
- TokenFlow: https://arxiv.org/abs/2307.10373
- EchoStyle: https://github.com/HKUST-C4G/EchoStyle
- DAVIS: https://arxiv.org/abs/1704.00675 and https://davischallenge.org/davis2017/code.html
