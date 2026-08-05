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
// Palette
//------------------------------------------------------------

uniform int u_palette_size;

uniform vec3 u_palette_0;
uniform vec3 u_palette_1;
uniform vec3 u_palette_2;
uniform vec3 u_palette_3;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform float u_intensity;


out vec4 frag_color;


//------------------------------------------------------------
// Palette Sampling
//------------------------------------------------------------

vec3 sample_palette(float t)
{
    t = clamp(t, 0.0, 1.0);

    if (u_palette_size <= 1)
    {
        return u_palette_0;
    }

    if (u_palette_size == 2)
    {
        return mix(
            u_palette_0,
            u_palette_1,
            t
        );
    }

    if (u_palette_size == 3)
    {
        if (t < 0.5)
        {
            return mix(
                u_palette_0,
                u_palette_1,
                t * 2.0
            );
        }

        return mix(
            u_palette_1,
            u_palette_2,
            (t - 0.5) * 2.0
        );
    }


    if (t < 1.0 / 3.0)
    {
        return mix(
            u_palette_0,
            u_palette_1,
            t * 3.0
        );
    }

    if (t < 2.0 / 3.0)
    {
        return mix(
            u_palette_1,
            u_palette_2,
            (t - 1.0 / 3.0) * 3.0
        );
    }

    return mix(
        u_palette_2,
        u_palette_3,
        (t - 2.0 / 3.0) * 3.0
    );
}

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

    vec3 color =
        sample_palette(gradient);

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}