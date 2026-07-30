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
// Checkerboard
//------------------------------------------------------------

uniform float u_cells;


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
    // Square Checkerboard
    //--------------------------------------------------------

    vec2 grid = floor(uv * u_cells);

    float pattern = mod(grid.x + grid.y, 2.0);


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