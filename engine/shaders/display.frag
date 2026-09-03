#version 330

#include "engine_uniforms.glsl"
#include "coordinates.glsl"
#include "transitions/iris.glsl"

uniform sampler2D u_texture;

in vec2 uv;

out vec4 frag_color;

void main()
{
    vec4 color =
        texture(u_texture, uv);

    vec2 transition_uv =
        get_uv();

    frag_color =
        apply_iris(
            color,
            transition_uv
        );
}