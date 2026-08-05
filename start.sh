#!/bin/bash
# Serve this directory and print URLs you can open on this Mac or a nearby device.
#
# A plain file:// open will NOT work: the renderer uploads video frames to a WebGL
# texture, and a file:// video is an opaque origin, so the upload is rejected and
# the video silently falls back to flat. It must be served over http.

cd "$(dirname "$0")"
PORT=8778

pkill -f "serve.py" 2>/dev/null
sleep 1
python3 serve.py >/tmp/spatial_testbed.log 2>&1 &
sleep 1.5

if ! curl -s -o /dev/null --max-time 4 "http://127.0.0.1:$PORT/"; then
    echo "Server failed to start. See /tmp/spatial_testbed.log"
    exit 1
fi

LAN=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)

echo "Spatial video test page is running."
echo
echo "  This Mac:      http://localhost:$PORT/"
[ -n "$LAN" ] && echo "  Same network:  http://$LAN:$PORT/"
echo
echo "Requires a WebKit build containing the spatial video patch"
echo "(webkit.org/b/319971), with Develop > Feature Flags >"
echo "\"Spatial Video Rendering\" enabled. It is off by default."
echo
echo "Stop with: pkill -f serve.py"
