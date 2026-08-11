# Video Projection Explainer

## Authors:

- Phinehas Fuachie

## Participate

- https://github.com/WebKit/explainers

## tl;dr

We propose a `projection` attribute on the `<video>` element, defaulting to `auto`
so that media describing its own projection needs no markup, and a corresponding
`projection` property on `VideoTrackConfiguration` for reading the projection the
User Agent resolved. This lets the User Agent present 360°, 180°, and
wide-field-of-view content natively instead of each site shipping its own renderer.

## Introduction

Most video is rectilinear: the decoded frame is the image, and displaying it means
drawing that rectangle. A growing amount of video is not. In equirectangular 360°
content the frame is a spherical panorama flattened into a rectangle; in
half-equirectangular 180° content it covers a hemisphere; in parametric wide-FOV
content it is a lens projection with a known field of view. Displaying any of
these as a plain rectangle is wrong — the viewer sees a stretched, distorted
image rather than the scene.

Some formats carry this information in the file. Apple Projected Media Profile
(APMP), for instance, records a projection kind and field of view on the video
track, and a User Agent that parses it knows how to present the content without
the page's help. Many formats carry nothing, and for those the projection is
knowledge the author has and the User Agent does not.

The result today is that a site with projected video must implement its own
viewer: upload each frame into WebGL, build the mesh, and handle the drag
gestures. This is a substantial amount of code to reimplement per site, it forfeits
the User Agent's native controls and platform-appropriate interaction, and it
requires the video to be same-origin or CORS-clean so its frames can be read into
a texture. Content whose projection *is* described in the file gets no benefit
from that fact.

There is also no way for a page to read the projection a User Agent detected,
which is the same gap `VideoTrackConfiguration` closed for codecs, dimensions,
and color space.

## Use cases

A page hosts 360° video and wants it presented with the User Agent's own controls
and look-around interaction, without shipping a WebGL viewer.

A page hosts projected video in a format that carries no projection metadata — or
that the User Agent does not parse — and needs to tell the User Agent what the
geometry is.

A page transcodes or remuxes projected video and wants to confirm that the
projection metadata survived and is parsed as intended, in the way a page today
validates that its `VideoColorSpace` round-trips correctly.

A page wants to present its own affordances for projected content and needs to
know whether the media is projected at all, and how, in order to decide.

## Proposed changes to existing technologies

### HTML Media

The `<video>` element gains a `projection` content attribute, an enumerated
attribute whose keywords name a projection geometry. Its default, `auto`, means
the projection described by the media is used:

```html
<!-- APMP: the file describes its own projection. Nothing to declare. -->
<video src="panorama-apmp.mov" controls></video>

<!-- A format carrying no projection metadata. The author declares it. -->
<video src="panorama.mp4" projection="equirectangular" controls></video>
```

```webidl
enum VideoProjection {
    "auto",
    "rectilinear",
    "equirectangular",
    "halfequirectangular",
    "equiangularcubemap",
    "parametric",
    "fisheye",
};

partial interface HTMLVideoElement {
    [CEReactions, Reflect, Enumerated] attribute DOMString projection;
};
```

`auto` is both the *missing value default* and the *invalid value default*: an
absent attribute and an unrecognized keyword behave identically, and in both cases
the User Agent uses the projection described by the media, if any. A misspelled
declaration therefore cannot break content the User Agent already understands, and
a page can return to metadata-driven behavior by assigning `"auto"`.

Any other keyword is the author's assertion about the geometry, and takes
precedence over the media's own description, since the author's declaration is the
more specific statement. This makes `rectilinear` meaningful rather than merely
the common case: it declares that the frame is to be presented as-is even if the
media describes a projection.

Content that is neither described nor declared is presented as it is today.

`VideoTrackConfiguration` gains matching members, so a page can read what the
User Agent determined:

```webidl
partial dictionary VideoTrackConfiguration {
    VideoProjection projection;
    long horizontalFieldOfView;
};
```

`projection` reports the projection in effect for the track, resolved rather than
requested — it never reports `auto`. A page can therefore distinguish what it
asked for, by reading the attribute, from what the User Agent concluded, by
reading the configuration. `horizontalFieldOfView` reports the horizontal field of
view in degrees where the media describes one, and is absent otherwise; it is
meaningful for `parametric` and `fisheye`, where the geometry is not fully
determined by the projection kind alone.

Consistent with the rest of `VideoTrackConfiguration`, these are filled with
values as understood by the User Agent. A track the User Agent treats as
rectilinear reports `"rectilinear"` rather than nothing.

A change in projection is a change in track configuration, and so fires the
existing `configurationchange` event on `VideoTrackList`.

### Presentation

Declaring a projection does not by itself specify how the User Agent presents the
content, and this proposal deliberately does not require a particular
presentation. A User Agent may render projected content into a viewport the user
can look around, offer it to a head-mounted display, or continue to present the
frame as-is. What the attribute provides is the information needed to make that
choice correctly.

## Privacy considerations

Projection is a property of the media, and like the rest of
`VideoTrackConfiguration` it must not become a channel for reading cross-origin
media. The `projection` and `horizontalFieldOfView` members are therefore empty
for media whose data is CORS cross-origin, as the existing members already are.

The `projection` content attribute raises no such concern: it carries information
from the page to the User Agent, not the reverse, and reflecting it exposes only
what the page itself set.

## Open questions

Should projection be declarable per-source rather than only on the element?
Projection is a property of a track, so media whose sources differ in geometry
cannot be described by a single attribute on `<video>`. A `projection` attribute
on `<source>` would address this at the cost of a second place to look.

Should an unrecognized keyword be silently treated as `auto`, as proposed here, or
reported to the author? Treating it as `auto` keeps described content working, but
does nothing visible for a misspelled declaration.

Should stereoscopic content be described by this attribute? Stereo layout is
orthogonal to projection — content can be either, both, or neither — which
suggests it should be separate, but the two are frequently encountered together.
