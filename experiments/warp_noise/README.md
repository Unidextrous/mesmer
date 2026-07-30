# Domain Warp

## Concepts

- coordinate transformation
- procedural noise
- value noise
- interpolation
- smoothstep
- coordinate distortion
- function composition

## Parameters

### Transform

u_offset

Moves the coordinate space.

u_scale

Controls coordinate scaling.

u_rotation

Rotates the coordinate space.

### Domain Warp

u_noise_scale

Controls the size of the noise structures.

Higher values create finer distortions.

u_warp_strength

Controls how strongly noise bends the coordinate space.

Higher values create more chaotic distortion.

u_speed

Controls animation speed.

### Appearance

u_color_1

First color.

u_color_2

Second color.

u_intensity

Brightness multiplier.

## How It Works

The shader creates a noise field.

That noise field modifies the coordinates.

The modified coordinates are then passed
through another noise function.

Conceptually:

coordinate

↓

noise distortion

↓

warped coordinate

↓

final noise

↓

color


## Possible Extensions

### More Layers

- fractal noise
- multiple warp passes
- turbulence

### Visuals

- clouds
- smoke
- fire
- lava
- water

### Mesmer Applications

- organic transitions
- breathing textures
- flowing backgrounds
- psychedelic distortions