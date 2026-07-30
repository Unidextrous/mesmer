# Kaleidoscope

## Concepts

- polar coordinates
- angle calculations
- coordinate folding
- symmetry
- modulo repetition
- interpolation
- procedural patterns
- layered wave functions
- interference patterns

## Parameters

### Transform

u_offset

Moves the coordinate space.

u_scale

Controls zoom.

u_rotation

Rotates the entire pattern.

---

### Kaleidoscope

u_segments

Controls the number of mirrored sections.

Higher values create more symmetry.

u_radius_frequency

Controls radial repetition.

Higher values create more rings/details.

u_angle_frequency

Controls detail inside each segment.

u_speed

Controls animation speed.

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

The shader converts Cartesian coordinates:

x, y

into polar coordinates:

radius, angle

The angle is divided into repeated slices.

Each slice is mirrored, creating the
kaleidoscope effect.

Conceptually:

coordinates

↓

polar conversion

↓

angle folding

↓

procedural pattern

↓

color


---


### Pattern Layers

The visual combines multiple mathematical wave functions.

Each layer creates a separate pattern:

layer 1:

radius + angle


layer 2:

radius - angle


Combining these creates interference,
producing more complex structures than a
single procedural function.

---


## Possible Extensions

- color cycling
- domain warping
- audio-reactive segments
- rotating symmetry
- fractal kaleidoscope
- recursive folding
- additional pattern layers