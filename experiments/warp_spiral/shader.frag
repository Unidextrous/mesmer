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
uniform vec2  u_scale;
uniform float u_rotation;


//------------------------------------------------------------
// Spiral
//------------------------------------------------------------

uniform float u_arms;
uniform float u_frequency;
uniform float u_speed;


//------------------------------------------------------------
// Domain Warp
//------------------------------------------------------------

uniform float u_noise_scale;
uniform float u_warp_strength;
uniform float u_warp_speed;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform vec3 u_color_1;
uniform vec3 u_color_2;

uniform float u_intensity;


//------------------------------------------------------------
// Output
//------------------------------------------------------------

out vec4 frag_color;


//------------------------------------------------------------
// Hash Noise
//------------------------------------------------------------

float random(vec2 position)
{
    return fract(
        sin(
            dot(
                position,
                vec2(12.9898, 78.233)
            )
        )
        * 43758.5453
    );
}


//------------------------------------------------------------
// Value Noise
//------------------------------------------------------------

float noise(vec2 position)
{
    vec2 i = floor(position);
    vec2 f = fract(position);

    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(
        mix(a, b, u.x),
        mix(c, d, u.x),
        u.y
    );
}


//------------------------------------------------------------
// Main
//------------------------------------------------------------

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
        cos(u_rotation), -sin(u_rotation),
        sin(u_rotation),  cos(u_rotation)
    );

    uv = rotation * uv;

    uv /= u_scale;


    //--------------------------------------------------------
    // Domain Warp
    //--------------------------------------------------------

    vec2 warp;

    warp.x = noise(
        uv * u_noise_scale
        + vec2(0.0, u_time * u_warp_speed)
    );

    warp.y = noise(
        uv * u_noise_scale
        + vec2(5.2, 1.3)
        + u_time * u_warp_speed
    );

    warp -= 0.5;


    uv += warp * u_warp_strength;


    //--------------------------------------------------------
    // Polar Coordinates
    //--------------------------------------------------------

    float radius = length(uv);

    float angle = atan(
        uv.y,
        uv.x
    );


    //--------------------------------------------------------
    // Spiral Function
    //--------------------------------------------------------

    float spiral =
        sin(
            angle * u_arms
            + radius * u_frequency
            - u_time * u_speed
        );


    spiral =
        smoothstep(
            0.0,
            1.0,
            spiral * 0.5 + 0.5
        );


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color = mix(
        u_color_1,
        u_color_2,
        spiral
    );


    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}