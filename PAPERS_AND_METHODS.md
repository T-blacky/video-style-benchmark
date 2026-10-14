# Relationship to related research

**This is a newly designed evaluation collection, NOT the official dataset, benchmark numbers or protocol of the cited papers.**

| Work | Source | Conditioning | What it contributes to this benchmark | Not provided here |
|---|---|---|---|---|
| **UniVST** | [paper](https://arxiv.org/abs/2410.20084), [repo](https://github.com/QuanjianSong/UniVST) | Content video + style image + optional foreground mask | Separate mask-aware tests, spatially localized output quality, temporal coherence; masks can be sourced from DAVIS segmentation | DDIM inversion, point-matching mask propagation, localized style-transfer inference |
| **FreeViS** | [paper](https://arxiv.org/abs/2510.01686), [project](https://xujiacong.github.io/FreeViS/) | Content video + an arbitrary style image; video keyframes are stylized by an image-style-transfer method to make extra *stylized* refs | One style image for each content sequence, explicit first/middle/last **content** keyframes, style and motion evaluation | The stylized keyframes (cannot be derived without an image stylizer) or FreeViS inference weights |
| **TokenFlow** | [paper](https://arxiv.org/abs/2307.10373), [repo](https://github.com/omerbt/TokenFlow) | Content video + target **text** editing prompt | Text-conditioned temporal consistency baseline | Image-reference conditioning; the style image path is intentionally ignored |
| **EchoStyle** | [repo](https://github.com/HKUST-C4G/EchoStyle) | Content video + text prompt in documented inference JSON | Exportable text baseline and motivation for compatibility | LoRA training data or a generic image-reference input API |

## Why DAVIS 2017 instead of the v0.1 photo pan clips?

The older seven-video package contained camera simulations and very simple synthetic motion. It cannot reasonably test occlusion, object integrity and fine-grained motion. DAVIS 2017 supplies independent real scene sequences with moving subjects and many segmentation challenges. The new 50-source suite selects videos with at least 49 source frames (verified from published dataset metadata) and reserves masks for an optional separate UniVST analysis. DAVIS is **not** a video-stylization ground-truth dataset. We use it as a source of content sequences.

## Why the six style exemplars?

A reference image needs to contain unmistakable characteristics. We deliberately move from four low-contrast hand-drawn gradients to six more distinguishable styles:

1. Monochrome expressive **ink wash**
2. Thick orange/blue **oil impasto**
3. Translucent pastel **watercolor**
4. Bold dark outlines / flat-color **comic cel-shading**
5. Fragmented geometric **cubism**
6. Block-based 16-bit **pixel art**

Each generated image uses a similar mountain-lake-cabin composition: fewer semantic-content differences between styles, though **shared scene content can itself leak into outputs**. Do not interpret reference-image style as separate from reference content without additional controlled tests.

## Differences between a real benchmark and a smoke test

The seven bundled MP4s and their 42 pairs are directly runnable with no network. They prove paths, decoding, prompts, masking on 3 synthetic clips, metadata and adapters function. They are not real-world comparisons. The 50 DAVIS MP4s are **not** bundled in this ZIP/GitHub starter. The acquisition script downloads them from the third-party Hugging Face DAVIS conversion; a complete materialized benchmark has **50 real MP4s** and 300 paired cases. The repo carries the full 50-video plan and the script, not a false claim that the files are already present.

## Reproducibility rules

- Keep all 50 source names fixed; do not sample a different 50 every time.
- Keep the six refs, normalization settings and prompt text fixed across methods.
- For the same video's six styles, aggregate metrics by **source video** before estimating confidence intervals.
- Label text-only TokenFlow or EchoStyle baselines separately from image-reference pipelines; same styled text cannot guarantee equivalent conditioning.
- Report `N attempted` and `N usable`, failed downloads, inference failures, and any masks missing.
- For UniVST localization, obtain annotated masks from official DAVIS 2017 archives and align/rescale them with the normalized content frames before scoring. Never fabricate masks for real-world video.

See [`EVALUATION_PROTOCOL.md`](EVALUATION_PROTOCOL.md) for metrics and [`ASSET_LICENSES.md`](ASSET_LICENSES.md) for source attribution and allowed redistribution.