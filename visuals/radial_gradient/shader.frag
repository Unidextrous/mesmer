#version 330

//------------------------------------------------------------
// Engine Uniforms
//------------------------------------------------------------

uniform float u_time;
uniform float u_delta_time;
uniform vec2  u_resolution;
uniform int   u_frame;


//------------------------------------------------------------
// Parameters
//------------------------------------------------------------

uniform vec2  u_offset;
uniform float u_radius;

uniform vec3  u_color_center;
uniform vec3  u_color_edge;

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


    //--------------------------------------------------------
    // Distance Field
    //--------------------------------------------------------

    float distance = length(uv);

    float gradient = distance / u_radius;

    gradient = clamp(gradient, 0.0, 1.0);


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color = mix(
        u_color_center,
        u_color_edge,
        gradient
    );

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}