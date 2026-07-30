#version 330

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
// Wave
//------------------------------------------------------------

uniform float u_frequency;
uniform float u_amplitude;
uniform float u_speed;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform vec3 u_color_1;
uniform vec3 u_color_2;

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
    // Wave
    //--------------------------------------------------------

    float wave = sin(
        uv.x * u_frequency
        + u_time * u_speed
    );


    //--------------------------------------------------------
    // Convert range
    // -1.0 -> 1.0 becomes 0.0 -> 1.0
    //--------------------------------------------------------

    float pattern = wave * 0.5 + 0.5;


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color = mix(
        u_color_1,
        u_color_2,
        pattern
    );

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}