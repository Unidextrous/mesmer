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

uniform vec3 u_color;
uniform float u_intensity;


out vec4 frag_color;


void main()
{
    vec3 color = u_color * u_intensity;

    frag_color = vec4(color, 1.0);
}