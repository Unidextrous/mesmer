#version 330


#include "engine_uniforms.glsl"
#include "coordinates.glsl"
#include "transform.glsl"
#include "palette.glsl"


//============================================================
// Gradient Reference Shader
//
// Demonstrates:
// - Coordinate normalization
// - Aspect-ratio correction
// - Translation
// - Rotation
// - Scaling
// - Linear gradient
// - Optional repetition
// - Exponential shaping
// - Color interpolation
//
//============================================================


//------------------------------------------------------------
// Transform
//------------------------------------------------------------

uniform vec2  u_offset;
uniform float u_rotation;
uniform vec2  u_scale;


//------------------------------------------------------------
// Gradient
//------------------------------------------------------------

uniform float u_start;
uniform float u_end;

uniform float u_repeat;
uniform bool  u_repeat_enabled;

uniform bool  u_invert;


//------------------------------------------------------------
// Curve
//------------------------------------------------------------

uniform float u_exponent;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform float u_intensity;


out vec4 frag_color;


void main()
{
    //--------------------------------------------------------
    // Coordinate System
    //--------------------------------------------------------

    vec2 uv = get_uv();
    uv = apply_transform(
        uv,
        u_offset,
        u_rotation,
        u_scale
    );

    //--------------------------------------------------------
    // Linear Gradient
    //--------------------------------------------------------

    float gradient =
        (uv.x - u_start) /
        (u_end - u_start);


    //--------------------------------------------------------
    // Repeat
    //--------------------------------------------------------

    if (u_repeat_enabled)
    {
        gradient *= u_repeat;
        gradient = fract(gradient);
    }


    //--------------------------------------------------------
    // Clamp
    //--------------------------------------------------------

    gradient = clamp(gradient, 0.0, 1.0);


    //--------------------------------------------------------
    // Shape
    //--------------------------------------------------------

    gradient = pow(gradient, u_exponent);


    //--------------------------------------------------------
    // Invert
    //--------------------------------------------------------

    if (u_invert)
    {
        gradient = 1.0 - gradient;
    }


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color =
        sample_palette(gradient);

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}