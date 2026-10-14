# Media rights, sources and restrictions

**This file is critical before uploading media to a public GitHub repo.** Code and original utilities may be covered by the included MIT LICENSE; that does **not** automatically apply to third-party media or the original authors' videos.

## The 50 DAVIS videos (not bundled)

- DAVIS 2017 challenge download page: https://davischallenge.org/davis2017/code.html
- Community-hosted converted MP4 source: https://huggingface.co/datasets/emirkisa/DAVIS-2017-480p-mp4
- Community conversion explicitly declares **CC BY-NC 4.0**; consequently the prepared 50-video evaluation suite is for noncommercial research use subject to attribution, restrictions and upstream per-video rights. DAVIS video media may have exceptions by original source, so inspect official DAVIS SOURCES.md before redistribution.
- We **do not bundle** the 50 third-party videos with the public starter. The `scripts/prepare_davis.py` downloader brings them to the user's workspace. `data/real_videos/*.mp4` is gitignored deliberately. If a team chooses to redistribute, it must audit per-video rights and give legally required credits.
- DAVIS citation: Jordi Pont-Tuset et al., *The 2017 DAVIS Challenge on Video Object Segmentation* (arXiv:1704.00675, 2017).

## Reference style images bundled in this repository

The six bundled `data/styles/*.png` files **were replaced** on 2026-10-14 using documented artwork sources (not the previous low-quality procedural placeholders). Each is padded and resized to 768×768. Resizing, converting to PNG, and adding a neutral border are modifications of the reproduced artwork, not a new authorship claim.

| File | Title | Creator | Wikimedia Commons source | Rights noted by source |
|---|---|---|---|---|
| `data/styles/ink_wash.png` | Landscape attributed to Sesshū Tōyō (Honolulu Museum of Art) | Sesshū Tōyō (attributed) | [Original file](https://commons.wikimedia.org/wiki/File:Landscape_attributed_to_Sesshu_Toyo%2C_Honolulu_Museum_of_Art.JPG) | Public-domain artwork / verify media page |
| `data/styles/oil_impasto.png` | The Starry Night | Vincent van Gogh | [Original file](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg) | Public domain (PD-Art) |
| `data/styles/watercolor.png` | Gloucester Harbor (1873, watercolor) | Winslow Homer | [Original file](https://commons.wikimedia.org/wiki/File:Winslow_Homer_-_Gloucester_Harbor_(1873%2C_watercolour).jpg) | Public domain (PD-Art) |
| `data/styles/comic_cel.png` | Little Nemo in Slumberland (1908, panels 11–15) | Winsor McCay | [Original file](https://commons.wikimedia.org/wiki/File:Little_Nemo_in_Slumberland_(1908-07-26)_panels_11_to_15.jpg) | Public domain (US); historical comic, not modern cel-shaded animation |
| `data/styles/cubism.png` | Cubist Still Life (1915) | Juan Gris | [Original file](https://commons.wikimedia.org/wiki/File:Juan_Gris_-_Cubist_Still_Life_(1915).jpg) | Public domain (PD-Art) |
| `data/styles/pixel_art.png` | Landscape pixel art (2026) | Fahmirayan | [Original file](https://commons.wikimedia.org/wiki/File:Landscape_pixel_art.png) | CC BY-SA 4.0 — attribution and ShareAlike required |

**IMPORTANT:** `pixel_art.png` is based on `Landscape pixel art.png` by **Fahmirayan**, licensed **CC BY-SA 4.0** ([license](https://creativecommons.org/licenses/by-sa/4.0/)). Its resized/letterboxed derivative is subject to the same license; retain this credit and distribute derivative image versions under CC BY-SA 4.0. MIT applies only to repository code, **not** to these artworks. The five historical artworks are identified on their Wikimedia Commons pages as public-domain or PD-Art; verify jurisdiction-dependent photographic-reproduction rights before further redistribution.

Ink wash is an attribution and comic_cel is **historical comic art** (not a modern animation cel-shading reference). These are style exemplars, not matched-content paintings: subjects differ. Source file names and locations are also recorded in `manifests/styles.json`.
