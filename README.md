# Spatial Video Rendering — test page

A static test page for WebKit's experimental spatial/projected video rendering
(360° equirectangular, 180° half-equirectangular, parametric wide-FOV, and a
page-declared fisheye) drawn by a WebGL renderer inside the media controls.

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

### Camera

The Camera panel drives the field of view, yaw and pitch through the reflected
`fieldOfView` / `yaw` / `pitch` IDL attributes on `HTMLVideoElement`.

Dragging and scrolling on the video move the camera without changing those attributes —
the same split as `muted` and `defaultMuted`. The live camera is readable separately as
`cameraYaw` / `cameraPitch` / `cameraFieldOfView`, and reports a `webkitcameramoved` event
(at most one per rendered frame), which is how the sliders follow your drag.

### Link to website below
https://phinny01.github.io/SpatialRendererTestPage/
