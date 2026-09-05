#version 330

#include "engine_uniforms.glsl"
#include "coordinates.glsl"
#include "transitions/iris.glsl"

uniform sampler2D u_current_texture;
uniform sampler2D u_next_texture;

in vec2 uv;

out vec4 frag_color;

void main()
{
    vec4 current_color =
        texture(
            u_current_texture,
            uv
        );

    vec4 next_color =
        texture(
            u_next_texture,
            uv
        );

    vec2 transition_uv =
        get_uv();

    frag_color =
        apply_iris(
            current_color,
            next_color,
            transition_uv
        );
}