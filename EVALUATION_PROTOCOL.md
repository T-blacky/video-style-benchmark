# Evaluation protocol (proposed; not the original papers' official benchmark)

## Overview

- Primary suite: 50 independently sourced DAVIS 2017 video sequences, each paired with **all six** style reference images (300 cases). Do not mix the seven offline smoke videos into this 300-case benchmark.
- Screening suite: 50 cases, each distinct video paired with one of six styles in a round-robin manner; see `real_50_screening_planned.json`. Screening is for cheap configuration comparison, not a substitute for the 300 cases.
- Fixed normalization: 49 frames per sequence, 512 × 320, 24 fps (~2.04s). Keep the same source frames, prompts and style refs when comparing methods.
- Input for image-reference methods: video + reference style image (+ optional segmentation mask for UniVST).
- Input for text-only TokenFlow/EchoStyle baseline: video + style description prompt; clearly label **different conditioning** in the results.

## Suggested columns and interpretation

| Dimension | Manual rubric (1–5; higher better) | Potential machine metric (with caveats) |
|---|---|---|
| Style fidelity | Similarity of brushwork, linework, palette and texture to reference style, not just artistic-looking output | CSD-style embeddings (require implementation and reference calibration); CLIP alone can confound style with content |
| Content structure | Preserve identity, scene geometry, relevant objects | DINO feature comparison / semantic similarity; imperfect for heavy styles |
| Motion preservation | Preserve the source motion trajectory | Optical-flow consistency; require alignment and matching scale |
| Temporal stability | No flicker, random re-rendering or unstable textures | Optical-flow-warped temporal error, disocclusion mask; ordinary adjacent-frame differences are **not** sufficient |
| Localized preservation | Preserve pixels/appearance outside the mask (UniVST) | Outside-mask LPIPS / color change and target-mask style metrics; only when masks provided |
| Visual quality | Detail, absence of artifacts and perceptual appeal | Human preference evaluation, blind to method identity |
| Resource cost | Wall-clock seconds and peak allocated VRAM (record GPU model) | Direct timing and `torch.cuda.max_memory_allocated()` where supported |

## Human evaluation template

`manifests/human_eval_template.csv` is blank by design. Suggested process: pick 30+ cases balanced by subject, motion and style; randomize output order; three independent raters score 1–5 for style, content, motion, temporal stability and quality. Record means, uncertainty intervals and the fraction of failed generations. Report variance between raters and do **not** compute an overall unweighted score as if dimensions were interchangeable.

## Pitfalls

- Six references intentionally share *similar* scenery so their **style features** can be compared more easily, but the same scene may induce content leakage in image-condition methods. Later add alternate-content reference images per style and treat this as a separate experiment.
- DAVIS was designed for segmentation, not style transfer; no styled ground-truth videos are included. You **cannot** report supervised PSNR/SSIM against a nonexistent stylized target.
- If source videos are downscaled/cropped/padded differently between methods, the comparison is biased.
- Different architectures, reference generation schemes, diffusion steps, seed choices and hardware can dominate measured improvements. Record exact commands and versions.
- Train/val labels describe DAVIS provenance only; they do **not** mean one part of this benchmark is used to train a training-free model.
- Not all 50 sequences are necessarily usable for all methods. If a method needs masks, report the subset size and why cases were excluded.

## Scoring and reporting

Always publish the denominator: e.g. *N=300 attempted, N=287 successful*. Report performance separately by style and content type, using video-level aggregation to avoid treating six cases of the same source video as six independent source clips.

## References

- UniVST: https://arxiv.org/abs/2410.20084 (localized style transfer; optional mask propagation)
- FreeViS: https://arxiv.org/abs/2510.01686 (arbitrary style image and multiple generated stylized keyframes)
- TokenFlow: https://arxiv.org/abs/2307.10373 (text-driven video editing consistency baseline)
- DAVIS: https://davischallenge.org/davis2017/code.html (video source / annotated segmentation origin)