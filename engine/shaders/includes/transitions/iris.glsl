//------------------------------------------------------------
// Iris Transition
//------------------------------------------------------------

uniform float u_transition_progress;

uniform vec2  u_iris_offset;
uniform float u_iris_max_radius;
uniform float u_iris_edge_softness;

uniform int u_iris_direction;
uniform int u_iris_active;


//------------------------------------------------------------
// Apply Iris
//
// Direction:
//     0 = IN
//     1 = OUT
//
// Progress:
//     0.0 → transition beginning
//     1.0 → transition complete
//
// IN:
//     Next visual is revealed through a growing circle.
//
// OUT:
//     Current visual is revealed over the next visual
//     through a shrinking circle.
//------------------------------------------------------------

vec4 apply_iris(
    vec4 current_color,
    vec4 next_color,
    vec2 uv
)
{
    //--------------------------------------------------------
    // No transition
    //--------------------------------------------------------

    if (u_iris_active == 0)
    {
        return current_color;
    }


    //--------------------------------------------------------
    // Position
    //--------------------------------------------------------

    vec2 position =
        uv - u_iris_offset;


    //--------------------------------------------------------
    // Distance from iris center
    //--------------------------------------------------------

    float distance =
        length(position);


    //--------------------------------------------------------
    // Aperture radius
    //--------------------------------------------------------

    float radius =
        u_iris_max_radius *
        u_transition_progress;


    //--------------------------------------------------------
    // Calculate edge
    //--------------------------------------------------------

    float edge;

    if (u_iris_edge_softness <= 0.0)
    {
        edge =
            step(
                radius,
                distance
            );
    }
    else
    {
        edge =
            smoothstep(
                radius - u_iris_edge_softness,
                radius + u_iris_edge_softness,
                distance
            );
    }


    //--------------------------------------------------------
    // Convert edge to aperture mask
    //
    // Inside circle:
    //     mask = 1
    //
    // Outside circle:
    //     mask = 0
    //--------------------------------------------------------

    float mask =
        1.0 - edge;



    //--------------------------------------------------------
    // Composite
    //--------------------------------------------------------

    return mix(
        current_color,
        next_color,
        mask
    );
}