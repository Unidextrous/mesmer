# Plasma

An animated procedural plasma field created by combining multiple sine waves.

## Description

Plasma is a classic procedural graphics effect built from several overlapping wave functions.

This visual combines horizontal, vertical, diagonal, and radial waves into a single continuous field. The resulting value is mapped between two colors to create the characteristic flowing plasma appearance.

This is a Phase 2 shader experiment intended to establish reusable techniques for combining procedural functions into a visual field.

## Techniques Demonstrated

- Screen-space coordinates
- Aspect-ratio correction
- Translation
- Scaling
- Rotation
- Sine waves
- Radial distance
- Combining multiple procedural functions
- Normalizing a scalar field
- Color interpolation
- Time-based animation

## Parameters

### Geometry

#### `u_frequency`

Controls the spatial frequency of the plasma waves.

Higher values produce more tightly packed patterns.

#### `u_amplitude`

Controls the strength of the combined wave field.

### Animation

#### `u_speed`

Controls how quickly the plasma pattern changes over time.

### Appearance

#### `u_color_1`

First color used by the plasma gradient.

#### `u_color_2`

Second color used by the plasma gradient.

#### `u_intensity`

Controls the overall brightness.

### Transform

#### `u_offset`

Moves the plasma field horizontally and vertically.

#### `u_scale`

Scales the plasma field.

#### `u_rotation`

Rotates the plasma field.

## Audio-Reactive Candidates

Potential future audio mappings include:

- Volume → amplitude
- Bass → frequency
- Midrange → wave speed
- Treble → color interpolation

These are currently only candidates and are not implemented by the visual itself.

## Future Experiments

Possible extensions include:

- Additional wave functions
- More color stops
- Color cycling
- Domain warping
- Nonlinear wave combinations
- Audio reactivity
- Contrast control
- Independent wave frequencies
- More complex plasma formulas

## Files

```text
plasma/
├── shader.frag
├── parameters.toml
├── metadata.toml
└── README.md