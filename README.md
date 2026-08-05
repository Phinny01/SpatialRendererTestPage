# Spatial Video Rendering — test page

A static test page for WebKit's experimental spatial/projected video rendering
(360° equirectangular, 180° half-equirectangular, parametric wide-FOV, and a
fisheye override) drawn by a WebGL renderer inside the media controls.

## Testing

1. Serve the directory (see below) and open it in Safari Technology Preview.
2. Enable **Develop › Feature Flags › Spatial Video Rendering**. It is off by default.
3. Reload, then **drag on the video**. If the view rotates, the feature is working.
