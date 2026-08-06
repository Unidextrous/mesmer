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

    float position =
        t * float(u_palette_size - 1);
    
    int index =
        int(floor(position));
    
    index = min(
        index,
        u_palette_size - 2
    );
    
    float fraction =
        fract(position);

    return mix(
        u_palette[index],
        u_palette[index + 1],
        fraction
    );
}
