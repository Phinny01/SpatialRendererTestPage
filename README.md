# Spatial Video Rendering — test page

A static test page for WebKit's experimental spatial/projected video rendering
(360° equirectangular, 180° half-equirectangular, parametric wide-FOV, and a
fisheye override) drawn by a WebGL renderer inside the media controls.

## Testing

1. Serve the directory (see below) and open it in Safari Technology Preview.
2. Enable **Develop › Feature Flags › Spatial Video Rendering**. It is off by default.
3. Reload, then **drag on the video**. If the view rotates, the feature is working.

If the video plays flat and dragging does nothing, the flag is off or the build
predates the feature.

## Serving

```sh
./start.sh        # http://localhost:8778
```

Any static host works. Opening `index.html` as a `file://` URL is not reliable —
serve it over HTTP.

## Video sources

The page streams Apple's public
[HLS immersive media examples](https://developer.apple.com/streaming/examples/)
directly; no media is redistributed here.

| Tile | Stream |
| --- | --- |
| 360° | `immersive-media/360Lighthouse/mvp.m3u8` |
| 180° | `immersive-media/180Lighthouse/mvp.m3u8` |
| Wide FOV | `immersive-media/wfovCausewayWalk/mvp.m3u8` |
| Fisheye (forced) | the 180° stream with `x-webkit-spatial="fisheye"` |

Three tiles resolve their projection from track metadata; the fisheye tile sets
`x-webkit-spatial="fisheye"` to exercise the attribute override path.

These streams send `Access-Control-Allow-Origin: *`, which matters: the renderer
uploads video frames as a WebGL texture, and a cross-origin frame *without* CORS
throws a `SecurityError` that the renderer catches and tears down — the video
keeps playing **flat, with no error**, looking identical to "the feature is off".
The `<video>` elements therefore set `crossorigin="anonymous"`.

## Using your own clips

Point `CLIPS` in `index.html` at your own files, then verify the metadata
survived:

```sh
python3 tools/projcheck.py <files>
```

`avconvert` **strips projection metadata unless both** `--disableSpatialConversion`
and `--disableMetadataFilter` are passed (see `tools/build-assets.sh`). Without
them clips still play, but metadata-driven tiles silently fall back to flat
video. Self-hosted clips must be same-origin with the page, or CORS-enabled, for
the reason above.
