# Spatial Video Rendering — test page

A static test page for WebKit's experimental spatial/projected video rendering
(360° equirectangular, 180° half-equirectangular, parametric wide-FOV, equi-angular
cubemap, and a page-declared fisheye) drawn by a WebGL renderer inside the media controls.

## Testing

1. Serve the directory (see below) and open it in Safari Technology Preview.
2. Enable **Develop › Feature Flags › Spatial Video Rendering**. It is off by default.
3. Reload, then **drag on the video**. If the view rotates, the feature is working.

If the video plays flat and dragging does nothing, the flag is off or the build
predates the feature.

### Declared projection

The Declared tab plays `assets/equirect360-nometadata.mp4`, a 360° clip with no projection
metadata, so `x-webkit-projection` is the only thing that can make it render as a sphere —
on `auto` it plays flat. Sourced from [Pexels](https://www.pexels.com/license/) (free to
use, modification allowed, no attribution required) and trimmed to 1280x640 for size; the
full-resolution source is not tracked.

The other tabs stream Apple's public immersive-media samples, which carry real APMP metadata.

### Equi-angular cubemap

The EAC tabs play `assets/eac360-nometadata.mp4` (1152x768, square 384x384 tiles) and
`assets/eac360-16x9-nometadata.mp4` (1920x1080, 640x540 tiles, the shape YouTube ships).
Both are converted from the same Pexels source as the Declared tab with
`ffmpeg -vf v360=equirect:eac`, so the EAC tabs and the Declared tab on `360` should show the
same scene. If they differ, a cube face is misplaced or rotated. The two tabs differ only in
packing, which is what makes them a pair: face coordinates are normalised per tile, so tile
aspect should not matter. Both frame sizes divide evenly into a 3x2 grid — avoid sizes that do
not, such as 1280x720, where a face boundary lands mid-pixel.

Cubemap has no metadata path — nothing produces `VideoProjectionMetadataKind::EquiAngularCubemap`
— so `x-webkit-projection="eac"` is the only way to select it, and it is never chosen
automatically. That is deliberate: auto-engaging on cubemap content would draw over pages such
as YouTube that already render 360 themselves.

Setting `eac` on the Declared tab is the negative control. That clip is equirectangular, so it
should look plainly wrong; a plausible-looking result there would mean something is off.

### Camera

The Camera panel drives the field of view, yaw and pitch through the reflected
`defaultFieldOfView` / `defaultYaw` / `defaultPitch` IDL attributes on `HTMLVideoElement`.

Dragging and scrolling on the video move the camera without changing those attributes —
the same split as `defaultMuted` and `muted`. The live camera is readable separately as
`fieldOfView` / `yaw` / `pitch`, and reports a `webkitcameramoved` event
(at most one per rendered frame), which is how the readout follows your drag.

### Link to website below
https://phinny01.github.io/SpatialRendererTestPage/
