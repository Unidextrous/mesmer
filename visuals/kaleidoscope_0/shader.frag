#version 330

//------------------------------------------------------------
// Engine uniforms
//------------------------------------------------------------

uniform float u_time;
uniform float u_delta_time;
uniform vec2  u_resolution;
uniform int   u_frame;


//------------------------------------------------------------
// Transform
//------------------------------------------------------------

uniform vec2  u_offset;
uniform vec2  u_scale;
uniform float u_rotation;


//------------------------------------------------------------
// Kaleidoscope
//------------------------------------------------------------

uniform float u_segments;

uniform float u_radius_frequency;
uniform float u_angle_frequency;

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
    // Coordinates
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
    // Polar coordinates
    //--------------------------------------------------------

    float radius = length(uv);

    float angle = atan(
        uv.y,
        uv.x
    );


    //--------------------------------------------------------
    // Kaleidoscope folding
    //--------------------------------------------------------

    float slice = 6.283185 / u_segments;

    angle = mod(angle, slice);

    angle = abs(
        angle - slice * 0.5
    );


    //--------------------------------------------------------
    // Pattern inside slice
    //--------------------------------------------------------

    float pattern =
        sin(
            radius * u_radius_frequency
            +
            angle * u_angle_frequency
            -
            u_time * u_speed
        );


    pattern =
        pattern * 0.5 + 0.5;


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color = mix(
        u_color_1,
        u_color_2,
        pattern
    );


    color *= u_intensity;


    frag_color = vec4(color, 1.0);
}