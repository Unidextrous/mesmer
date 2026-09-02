#version 330

uniform sampler2D u_texture;

in vec2 uv;

out vec4 frag_color;

void main()
{
    frag_color = texture(u_texture, uv);
}