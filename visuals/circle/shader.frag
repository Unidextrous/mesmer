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

uniform vec2 u_offset;
uniform vec2 u_scale;


//------------------------------------------------------------
// Circle
//------------------------------------------------------------

uniform float u_radius;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform vec3 u_color_inside;
uniform vec3 u_color_outside;

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
    uv /= u_scale;


    //--------------------------------------------------------
    // Signed Distance Field
    //--------------------------------------------------------

    float distance = length(uv);

    float circle = step(distance, u_radius);


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color = mix(
        u_color_outside,
        u_color_inside,
        circle
    );

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}