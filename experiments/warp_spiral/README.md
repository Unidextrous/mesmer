# Warped Spiral

## Concepts

- polar coordinates
- spiral functions
- procedural noise
- value noise
- coordinate distortion
- domain warping
- smoothstep()

## Parameters

### Transform

u_offset

Moves the coordinate space.

u_scale

Controls zoom.

u_rotation

Rotates the visual.

---

### Spiral

u_arms

Controls angular repetition.

Higher values create more spiral sections.

u_frequency

Controls radial spiral tightness.

Higher values create tighter spirals.

u_speed

Controls spiral animation.

---

### Domain Warp

u_noise_scale

Controls noise detail size.

u_warp_strength

Controls how strongly the spiral bends.

u_warp_speed

Controls the movement of the distortion field.

---

### Appearance

u_color_1

First color.

u_color_2

Second color.

u_intensity

Brightness multiplier.

---

## How It Works

The shader first creates a noise-based distortion field.

The coordinates are shifted by this field.

The warped coordinates are then converted into polar coordinates:

radius = distance from center

angle = direction from center

The spiral formula is evaluated using these warped coordinates.

Conceptually:

coordinates

↓

domain warp

↓

polar coordinates

↓

spiral function

↓

color


## Possible Extensions

- multiple warp layers
- audio-reactive distortion
- color cycling
- turbulence
- feedback effects