> **GitHub packaging note:** Six low-detail procedural PNG fallback images are included under `data/styles/`; high-detail AI style PNGs and seven smoke MP4s remain in the separate v0.2 companion ZIP. The 50 DAVIS real videos are intentionally excluded from GitHub.

# Media rights, sources and restrictions

**This file is critical before uploading media to a public GitHub repo.** Code and original utilities may be covered by the included MIT LICENSE; that does **not** automatically apply to third-party media or the original authors' videos.

## The 50 DAVIS videos (not bundled)

- DAVIS 2017 challenge download page: https://davischallenge.org/davis2017/code.html
- Community-hosted converted MP4 source: https://huggingface.co/datasets/emirkisa/DAVIS-2017-480p-mp4
- Community conversion explicitly declares **CC BY-NC 4.0**; consequently the prepared 50-video evaluation suite is for noncommercial research use subject to attribution, restrictions and upstream per-video rights. DAVIS video media may have exceptions by original source, so inspect official DAVIS SOURCES.md before redistribution.
- We **do not bundle** the 50 third-party videos with the public starter. The `scripts/prepare_davis.py` downloader brings them to the user's workspace. `data/real_videos/*.mp4` is gitignored deliberately. If a team chooses to redistribute, it must audit per-video rights and give legally required credits.
- DAVIS citation: Jordi Pont-Tuset et al., *The 2017 DAVIS Challenge on Video Object Segmentation* (arXiv:1704.00675, 2017).

## Generated reference styles

- `data/styles/{ink_wash,oil_impasto,watercolor,comic_cel,cubism,pixel_art}.png`: original AI-generated visual references created for this starter kit with a common mountain-lake-cabin composition. They are not copies of original UniVST/FreeViS/TokenFlow reference sets. We do not claim a museum artwork or other third-party source license for them.

## Seven offline smoke clips

Four videos are simulations of camera motion on photographs distributed by `scikit-image.data`:

- `astronaut_pan.mp4`: `skimage.data.astronaut`; NASA-associated sample (public-domain or no known restriction noted in scikit-image docs). This is NOT original filmed footage in this dataset.
- `chelsea_pan.mp4`: `skimage.data.chelsea`; Stefan van der Walt, CC0 in scikit-image data docs.
- `coffee_pan.mp4`: `skimage.data.coffee`; Rachel Michetti, CC0 in scikit-image data docs.
- `rocket_pan.mp4`: `skimage.data.rocket`; SpaceX sample, publicly licensed as documented in the source scikit-image data docs.

The clips `single_object.mp4`, `crossing_objects.mp4`, and `bouncing_object.mp4` and their masks were made from simple programmatic graphics for v0.1 smoke testing. Source reference: https://scikit-image.org/docs/stable/api/skimage.data.html

**No video here should be falsely presented as an official paper test output.**