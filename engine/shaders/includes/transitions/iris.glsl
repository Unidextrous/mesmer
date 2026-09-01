    //------------------------------------------------------------
    // Iris Transition
    //------------------------------------------------------------

    uniform float u_transition_progress;

    uniform vec2  u_iris_offset;
    uniform float u_iris_max_radius;
    uniform float u_iris_edge_softness;

    uniform vec3  u_iris_color;
    uniform float u_iris_opacity;

    uniform int   u_iris_direction;


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
    //------------------------------------------------------------

    vec4 apply_iris(
        vec4 color,
        vec2 uv
    )
    {
        //--------------------------------------------------------
        // Direction
        //--------------------------------------------------------

        float progress =
            u_transition_progress;

        if (u_iris_direction == 1)
        {
            progress =
                1.0 - progress;
        }


        //--------------------------------------------------------
        // Position
        //--------------------------------------------------------

        vec2 position =
            uv - u_iris_offset;


        //--------------------------------------------------------
        // Distance
        //--------------------------------------------------------

        float distance =
            length(position);


        //--------------------------------------------------------
        // Aperture
        //--------------------------------------------------------

        float radius =
            u_iris_max_radius *
            progress;


        //--------------------------------------------------------
        // Edge
        //--------------------------------------------------------

        float edge =
            smoothstep(
                radius - u_iris_edge_softness,
                radius + u_iris_edge_softness,
                distance
            );


        //--------------------------------------------------------
        // Transition Color
        //--------------------------------------------------------

        vec3 output_color =
            mix(
                color.rgb,
                u_iris_color,
                edge * u_iris_opacity
            );


        //--------------------------------------------------------
        // Output
        //--------------------------------------------------------

        return vec4(
            output_color,
            color.a
        );
    }