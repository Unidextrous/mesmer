#version 330

//============================================================
// Spiral Reference Shader
//
// Demonstrates:
// - Polar coordinates
// - Radius calculations
// - Angle calculations
// - Procedural patterns
// - Animation through phase shifting
// - Coordinate transforms
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
// Spiral Geometry
//------------------------------------------------------------

uniform float u_radius_frequency;
uniform float u_angle_frequency;

uniform float u_rotation_speed;


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
        cos(u_rotation),
       -sin(u_rotation),
        sin(u_rotation),
        cos(u_rotation)
    );

    uv = rotation * uv;

    uv /= u_scale;


    //--------------------------------------------------------
    // Polar Coordinates
    //--------------------------------------------------------

    float radius = length(uv);

    float angle = atan(uv.y, uv.x);


    //--------------------------------------------------------
    // Spiral Pattern
    //--------------------------------------------------------

    float spiral =
        sin(
            radius * u_radius_frequency
            +
            angle * u_angle_frequency
            -
            u_time * u_rotation_speed
        );


    //--------------------------------------------------------
    // Convert to 0-1 range
    //--------------------------------------------------------

    float pattern = step(0.0, spiral);


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