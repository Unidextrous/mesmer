//------------------------------------------------------------
// Palette Constants
//------------------------------------------------------------

const int MAX_PALETTE_SIZE = 8;


//------------------------------------------------------------
// Palette Uniforms
//------------------------------------------------------------

uniform int u_palette_size;
uniform vec3 u_palette[MAX_PALETTE_SIZE];

//------------------------------------------------------------
// Palette Sampling
//------------------------------------------------------------

vec3 sample_palette(float t)
{
    t = clamp(t, 0.0, 1.0);

    if (u_palette_size <= 1)
    {
        return u_palette[0];
    }

    float scaled =
        t * float(u_palette_size - 1);

    int lower =
        int(scaled);

    int upper =
        min(
            lower + 1,
            u_palette_size - 1
        );

    float blend =
        fract(scaled);

    return mix(
        u_palette[lower],
        u_palette[upper],
        blend
    );
}