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
uniform float u_rotation;


//------------------------------------------------------------
// Domain Warp
//------------------------------------------------------------

uniform float u_noise_scale;
uniform float u_warp_strength;
uniform float u_speed;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform vec3 u_color_1;
uniform vec3 u_color_2;

uniform float u_intensity;


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
// Smooth Value Noise
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
    // Create Warp Field
    //--------------------------------------------------------

    vec2 warp;

    warp.x = noise(
        uv * u_noise_scale
        + vec2(0.0, u_time * u_speed)
    );

    warp.y = noise(
        uv * u_noise_scale
        + vec2(5.2, 1.3)
        + u_time * u_speed
    );


    warp -= 0.5;


    //--------------------------------------------------------
    // Distort Domain
    //--------------------------------------------------------

    vec2 warped_uv =
        uv + warp * u_warp_strength;


    //--------------------------------------------------------
    // Evaluate Final Noise
    //--------------------------------------------------------

    float value = noise(
        warped_uv * u_noise_scale
    );


    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color = mix(
        u_color_1,
        u_color_2,
        value
    );

    color *= u_intensity;


    //--------------------------------------------------------
    // Output
    //--------------------------------------------------------

    frag_color = vec4(color, 1.0);
}