# Spiral

## Concepts

- normalized coordinates
- coordinate transforms
- polar coordinates
- radius calculations
- angle calculations
- radial frequency
- angular frequency
- procedural patterns
- trigonometric functions
- phase animation
- smooth transitions

## Parameters

### Transform

#### u_offset

Moves the spiral position.

#### u_rotation

Rotates the coordinate system.

#### u_scale

Changes the visual scale.

---

### Geometry

#### u_radius_frequency

Controls how tightly the spiral winds outward.

Higher values create more turns.

#### u_arm_count

Controls the number of spiral arms.

This corresponds to angular frequency.

---

### Animation

#### u_rotation_speed

Controls the movement of the spiral over time.

---

### Fill

#### u_fill_mode

Controls the spiral rendering method.

Values:

0 - Sine fill  
1 - Band fill

---

#### u_arm_width

Controls the width of spiral bands when using band fill.

---

#### u_edge_softness

Controls the softness of sine fill transitions.

---

#### u_leading_edge_softness

Controls the transition at the beginning of each spiral arm.

---

#### u_trailing_edge_softness

Controls the transition at the end of each spiral arm.

---

### Appearance

#### u_color_1

First palette color.

#### u_color_2

Second palette color.

#### u_intensity

Controls overall brightness.