# Ripple

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

Moves the ripple position.

#### u_rotation

Rotates the coordinate system.

#### u_scale

Changes the visual scale.

---

### Geometry

#### u_radius_frequency

Controls the frequency of the ripple.

Higher values create more turns.

---

### Animation

#### u_rotation_speed

Controls the movement of the ripple over time.

---

### Fill

#### u_fill_mode

Controls the ripple rendering method.

Values:

0 - Sine fill  
1 - Band fill

---

#### u_arm_width

Controls the width of ripple bands when using band fill.

---

#### u_edge_softness

Controls the softness of sine fill transitions.

---

#### u_leading_edge_softness

Controls the transition at the beginning of each ripple.

---

#### u_trailing_edge_softness

Controls the transition at the end of each ripple.

---

### Appearance

#### u_color_1

First palette color.

#### u_color_2

Second palette color.

#### u_intensity

Controls overall brightness.