#version 330

uniform vec2 u_resolution;

out vec4 frag_color;

void main()
{
    vec2 uv = gl_FragCoord.xy / u_resolution;

    uv -= 0.5;
    uv.x *= u_resolution.x / u_resolution.y;

    float radius = length(uv);
    float angle = atan(uv.y, uv.x);

    float pattern = sin(radius * 20.0 + angle * 1.0);
    pattern = pattern * 0.5 + 0.5;

    frag_color = vec4(pattern, pattern, pattern, 1.0);
}