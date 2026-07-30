# Circle

## Concepts

- normalized coordinates
- aspect-ratio correction
- distance fields
- length()
- step()
- thresholding
- mix()

## Parameters

### Transform

u_offset

Moves the circle.

u_scale

Scales the circle.

### Circle

u_radius

Radius of the circle.

### Appearance

u_color_inside

Color inside the circle.

u_color_outside

Color outside the circle.

u_intensity

Brightness multiplier.

## Possible Extensions

### Edge

u_edge_softness

Uses `smoothstep()` to soften the edge.

### Outline

u_outline_width

Creates an outline by comparing two radii.

### Animation

u_pulse_speed

Animates the radius over time.

u_pulse_amount

Controls the pulse amplitude.

### Distortion

- Noise
- Domain warping
- Audio-reactive radius