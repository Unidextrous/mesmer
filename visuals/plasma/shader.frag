#version 330

//------------------------------------------------------------
// Engine uniforms
//------------------------------------------------------------

uniform float u_time;
uniform float u_delta_time;
uniform vec2 u_resolution;
uniform int u_frame;


//------------------------------------------------------------
// Transform
//------------------------------------------------------------

uniform vec2 u_offset;
uniform vec2 u_scale;
uniform float u_rotation;


//------------------------------------------------------------
// Plasma
//------------------------------------------------------------

uniform float u_frequency;
uniform float u_speed;
uniform float u_amplitude;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform vec3 u_color_1;
uniform vec3 u_color_2;

uniform float u_intensity;


out vec4 frag_color;


//------------------------------------------------------------
// Main
//------------------------------------------------------------

void main()
{
    //--------------------------------------------------------
    // Coordinates
    //--------------------------------------------------------

    vec2 uv =
        gl_FragCoord.xy /
        u_resolution;

    uv -= 0.5;

    // Aspect-ratio correction

    uv.x *=
        u_resolution.x /
        u_resolution.y;


    //--------------------------------------------------------
    // Transform
    //--------------------------------------------------------

    uv -= u_offset;

    uv /= u_scale;


    float c =
        cos(u_rotation);

    float s =
        sin(u_rotation);

    mat2 rotation =
        mat2(
            c, -s,
            s,  c
        );

    uv =
        rotation *
        uv;


    //--------------------------------------------------------
    // Animated coordinates
    //--------------------------------------------------------

    float time =
        u_time *
        u_speed;


    //--------------------------------------------------------
    // Plasma waves
    //--------------------------------------------------------

    float wave_1 =
        sin(
            uv.x *
            u_frequency
            +
            time
        );


    float wave_2 =
        sin(
            uv.y *
            u_frequency
            -
            time
        );


    float wave_3 =
        sin(
            (uv.x + uv.y) *
            u_frequency
            +
            time * 0.7
        );


    float wave_4 =
        sin(
            length(uv) *
            u_frequency
            -
            time * 1.3
        );


    //--------------------------------------------------------
    // Combine waves
    //--------------------------------------------------------

    float plasma =
        (
            wave_1
            +
            wave_2
            +
            wave_3
            +
            wave_4
        )
        * 0.25;


    plasma *=
        u_amplitude;


    //--------------------------------------------------------
    // Convert to 0-1 range
    //--------------------------------------------------------

    float t =
        plasma * 0.5
        +
        0.5;


    t =
        clamp(
            t,
            0.0,
            1.0
        );


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color =
        mix(
            u_color_1,
            u_color_2,
            t
        );


    color *=
        u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color =
        vec4(
            color,
            1.0
        );
}