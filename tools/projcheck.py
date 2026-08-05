#!/usr/bin/env python3
"""Report the projection metadata WebKit reads, so a transcode can be verified."""

import sys
import AVFoundation
import CoreMedia
from Foundation import NSURL

SPATIAL_HINTS = ("projection", "fieldofview", "immersive", "spatial", "viewpacking", "heroeye")


def describe(path):
    url = NSURL.fileURLWithPath_(path)
    asset = AVFoundation.AVURLAsset.URLAssetWithURL_options_(url, None)
    name = path.split("/")[-1]

    tracks = asset.tracksWithMediaType_(AVFoundation.AVMediaTypeVideo)
    if not tracks:
        print(f"{name}: NO VIDEO TRACK\n")
        return

    track = tracks[0]
    size = track.naturalSize()
    formats = track.formatDescriptions()
    if not formats:
        print(f"{name}: no format description\n")
        return

    ext = CoreMedia.CMFormatDescriptionGetExtensions(formats[0]) or {}
    ext = dict(ext)

    print(name)
    print(f"   dims: {int(size.width)}x{int(size.height)}")

    spatial = {k: v for k, v in ext.items() if any(h in str(k).lower() for h in SPATIAL_HINTS)}
    if spatial:
        for k in sorted(spatial, key=str):
            print(f"   {k} = {spatial[k]}")
    else:
        print("   spatial/projection extensions: (NONE)")
    print()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        describe(p)
