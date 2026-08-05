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

## Serving

```sh
./start.sh        # http://localhost:8778
```

Any static host works. Serve over HTTP — opening `index.html` as a `file://` URL
is not reliable.

## How the projection is chosen

Metadata first: for APMP content the projection is read from the video track and
nothing is required of the page. The 360°, 180°, and Wide FOV tiles take this
path.

For formats that carry no projection metadata, the page declares it with the
`x-webkit-spatial` attribute:

| Value | Projection |
| --- | --- |
| `equirect360` (or any unrecognized value) | Equirectangular 360° |
| `180` | Half-equirectangular 180° |
| `wfov` | Parametric wide-FOV |
| `fisheye` | Fisheye |

When present, the attribute takes precedence over metadata. The Fisheye tile uses
this path.

## Video sources

The page streams Apple's public
[HLS immersive media examples](https://developer.apple.com/streaming/examples/)
directly; no media is redistributed here.

| Tile | Stream |
| --- | --- |
| 360° | `immersive-media/360Lighthouse/mvp.m3u8` |
| 180° | `immersive-media/180Lighthouse/mvp.m3u8` |
| Wide FOV | `immersive-media/wfovCausewayWalk/mvp.m3u8` |
| Fisheye | the 180° stream with `x-webkit-spatial="fisheye"` |

These streams send `Access-Control-Allow-Origin: *`, which matters: the renderer
uploads video frames as a WebGL texture, and a cross-origin frame *without* CORS
throws a `SecurityError` that the renderer catches and tears down — the video
keeps playing **flat, with no error**, looking identical to "the feature is off".
The `<video>` elements therefore set `crossorigin="anonymous"`.

Self-hosted clips must be same-origin with the page, or CORS-enabled, for the
same reason. To check that a transcode preserved projection metadata:

```sh
python3 tools/projcheck.py <files>
```

`avconvert` strips it unless both `--disableSpatialConversion` and
`--disableMetadataFilter` are passed (see `tools/build-assets.sh`).
