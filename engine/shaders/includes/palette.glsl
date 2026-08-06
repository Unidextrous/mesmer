//------------------------------------------------------------
// Palette Uniforms
//------------------------------------------------------------

uniform int u_palette_size;

uniform vec3 u_palette_0;
uniform vec3 u_palette_1;
uniform vec3 u_palette_2;
uniform vec3 u_palette_3;

//------------------------------------------------------------
// Palette Sampling
//------------------------------------------------------------

vec3 sample_palette(float t)
{
    t = clamp(t, 0.0, 1.0);

    if (u_palette_size <= 1)
    {
        return u_palette_0;
    }

    if (u_palette_size == 2)
    {
        return mix(
            u_palette_0,
            u_palette_1,
            t
        );
    }

    if (u_palette_size == 3)
    {
        if (t < 0.5)
        {
            return mix(
                u_palette_0,
                u_palette_1,
                t * 2.0
            );
        }

        return mix(
            u_palette_1,
            u_palette_2,
            (t - 0.5) * 2.0
        );
    }


    if (t < 1.0 / 3.0)
    {
        return mix(
            u_palette_0,
            u_palette_1,
            t * 3.0
        );
    }

    if (t < 2.0 / 3.0)
    {
        return mix(
            u_palette_1,
            u_palette_2,
            (t - 1.0 / 3.0) * 3.0
        );
    }

    return mix(
        u_palette_2,
        u_palette_3,
        (t - 2.0 / 3.0) * 3.0
    );
}
