#version 330

uniform vec2 u_resolution;

out vec4 frag_color;

void main()
{
    vec2 uv = gl_FragCoord.xy / u_resolution;

    uv -= 0.5;
    uv.x *= u_resolution.x / u_resolution.y;

    float distance_from_center = length(uv);

    float rings = sin(distance_from_center * 20.0) * 0.5 + 0.5;

    frag_color = vec4(rings, rings, rings, 1.0);
}