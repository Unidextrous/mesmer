#version 330

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
// Engine Uniforms
//------------------------------------------------------------

uniform float u_time;
uniform float u_delta_time;
uniform vec2  u_resolution;
uniform int   u_frame;


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

uniform vec3  u_color_1;
uniform vec3  u_color_2;

uniform float u_intensity;


out vec4 frag_color;

void main()
{
    //--------------------------------------------------------
    // Coordinate System
    //--------------------------------------------------------

    vec2 uv = gl_FragCoord.xy / u_resolution;

    uv -= 0.5;
    uv.x *= u_resolution.x / u_resolution.y;


    //--------------------------------------------------------
    // Transform
    //--------------------------------------------------------

    uv -= u_offset;

    mat2 rotation = mat2(
        cos(u_rotation), -sin(u_rotation),
        sin(u_rotation),  cos(u_rotation)
    );

    uv = rotation * uv;

    uv /= u_scale;


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

    vec3 color = mix(
        u_color_1,
        u_color_2,
        gradient
    );

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}