> **GitHub packaging note:** The repository includes 50-video and 300-pair manifests and six *procedural fallback* PNGs. Seven offline smoke-test videos and the distinct high-detail AI style PNGs are in a separately supplied companion ZIP, not checked into GitHub. Fifty DAVIS videos require downloading; the full evaluation set is not bundled.

# Data card — Video Style Transfer Benchmark v0.2

## Intended uses

A repeatable training-free video stylization **evaluation framework** with six visually distinct style reference images, optional segmentation masks, and a reproducible list of 50 real source videos from DAVIS 2017. Intended for academic prototyping and comparative evaluation after the real videos are materialized; not for training foundation models.

## Components and accessibility

| Component | Count | Where | Materialized at distribution time? |
|---|---:|---|---|
| Directly playable smoke videos | 7 | `data/videos/` | **Yes** |
| Generated style exemplars | 6 | `data/styles/` | **Yes** |
| Smoke video × reference pairs | 42 | `manifests/evaluation.json` | **Yes** |
| Pinned independent DAVIS source sequences | 50 | `manifests/real_50_catalog.json` | **No — acquire separately** |
| Real video × style cases | 300 | `manifests/real_300_planned.json` | Plan only until downloaded |
| Real source videos once acquired | 50 | `data/real_videos/` | On user's computer after downloader succeeds |
| Optional real foreground masks | Up to 50 × 49 | `data/davis_masks/` | No — requires official DAVIS annotations |

## Dataset origin and derivation

- Real sequences: DAVIS 2017 480p challenge train/val, with a convenient community-hosted conversion into raw 24-fps MP4: `https://huggingface.co/datasets/emirkisa/DAVIS-2017-480p-mp4`.
- Full DAVIS 2017 official archive: `https://davischallenge.org/davis2017/code.html`. Use official source for annotation masks, terms-of-use and citation.
- Fixed, named 50-video sample: 49 frames, 24 fps, scaled (with preserved aspect ratio + letterbox) to 512×320, encoded with libx264 CRF 22.
- Styles: six **AI-generated** 512×512 reference images, based on a matching scene to separate stylistic differences from extreme semantic differences. No painting here is copied from a specific museum original.
- Smoke video artifacts: four still-photo Ken Burns simulations plus three synthetic moving-shape clips, inherited from starter v0.1, with provenance in `ASSET_LICENSES.md`. Synthetic masks exist only for three moving-shape clips.

## Limitations

- This benchmark has **no paired stylized ground-truth targets** and **no official evaluation scores**. All style fidelity assessments are reference-conditioned, human-rated, or proxy metrics.
- 49 frames at 24 fps means roughly 2.04 seconds per source; short clips do not test minute-scale drift or long narratives. For those, create and document a separate long-video protocol.
- DAVIS is focused on challenging object segmentation and may over-represent moving foregrounds relative to everyday creator footage.
- Shared reference scenery can encourage inadvertent leakage of that scenery into output videos; include multiple reference contents per style for robust scientific claims.
- AI-generated style images may not reproduce historically accurate artistic techniques. Human checks are required.
- Style reference images are not positive stylized video samples; you cannot compute classical supervised paired-video PSNR/SSIM.
- Style-transfer baseline code, model weights and semantic prompts appropriate to a specific diffusion implementation are not included.
- Licensing varies across components; **do not blanket-license the entire repo's third-party media MIT**.
