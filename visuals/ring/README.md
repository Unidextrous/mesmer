# Ring

## Concepts

- normalized coordinates
- aspect-ratio correction
- distance fields
- length()
- abs()
- step()
- thresholding
- mix()

## Parameters

### Transform

u_offset

Moves the ring.

u_scale

Scales the ring.

### Ring

u_radius

Distance from the center to the ring.

u_thickness

Width of the ring.

### Appearance

u_color_inside

Color of the ring.

u_color_outside

Background color.

u_intensity

Brightness multiplier.

## Possible Extensions

### Edge

u_edge_softness

Uses `smoothstep()` for anti-aliased edges.

### Multiple Rings

- Ring count
- Ring spacing
- Animated expansion

### Animation

u_pulse_speed

Animates radius.

u_pulse_amount

Controls pulse strength.

### Advanced

- Dashed rings using angle calculations
- Audio-reactive thickness
- Glow effects
- Multiple overlapping rings