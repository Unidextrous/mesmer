vec2 apply_transform(
    vec2 uv,
    vec2 offset,
    float rotation,
    vec2 scale
)
{
    uv -= offset;

    mat2 rotation_matrix = mat2(
        cos(rotation), -sin(rotation),
        sin(rotation),  cos(rotation)
    );

    uv = rotation_matrix * uv;
    uv /= scale;

    return uv;
}