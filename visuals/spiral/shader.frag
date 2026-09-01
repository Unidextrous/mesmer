#version 330

#include "engine_uniforms.glsl"
#include "coordinates.glsl"
#include "transform.glsl"
#include "palette.glsl"

#include "transitions/iris.glsl"

//============================================================
// Spiral Visual
//
// Demonstrates:
// - Polar coordinates
// - Procedural spiral generation
// - Radial and angular frequency
// - Multiple fill modes
// - Edge control
// - Animated phase shifting
//
//============================================================


//------------------------------------------------------------
// Transform
//------------------------------------------------------------

uniform vec2  u_offset;
uniform float u_rotation;
uniform vec2  u_scale;

//------------------------------------------------------------
// Geometry
//------------------------------------------------------------

uniform float u_radius_frequency;
uniform float u_arm_count;


//------------------------------------------------------------
// Animation
//------------------------------------------------------------

uniform float u_rotation_speed;


//------------------------------------------------------------
// Fill
//------------------------------------------------------------

uniform int u_fill_mode;
uniform float u_arm_width;

uniform float u_edge_softness;
uniform float u_leading_edge_softness;
uniform float u_trailing_edge_softness;


//------------------------------------------------------------
// Appearance
//------------------------------------------------------------

uniform float u_intensity;


out vec4 frag_color;


//------------------------------------------------------------
// Constants
//------------------------------------------------------------

const float PI = 3.14159265358979323846;


//============================================================
// Main
//============================================================

void main()
{
    //--------------------------------------------------------
    // Coordinate System
    //--------------------------------------------------------

    vec2 uv = get_uv();
    uv = apply_transform(
        uv,
        u_offset,
        u_rotation,
        u_scale
    );


    //--------------------------------------------------------
    // Geometry
    //--------------------------------------------------------

    float radius =
        length(uv);

    float angle =
        atan(
            uv.y,
            uv.x
        );


    //--------------------------------------------------------
    // Phase
    //--------------------------------------------------------

    float phase =
        radius * u_radius_frequency
        +
        angle * u_arm_count
        -
        u_time * u_rotation_speed;


    //--------------------------------------------------------
    // Spiral Position
    //--------------------------------------------------------

    float arm_position =
        fract(
            phase / (2.0 * PI)
        );

    //--------------------------------------------------------
    // Sine Fill
    //--------------------------------------------------------


    float pattern = 0.0;


    if (u_fill_mode == 0)
    {
        float fill =
            sin(phase);

        pattern =
            smoothstep(
                -u_edge_softness,
                u_edge_softness,
                fill
            );
    }


    //--------------------------------------------------------
    // Bands Fill
    //--------------------------------------------------------


    else if (u_fill_mode == 1)
    {

        float leading =
            smoothstep(
                0.0,
                u_leading_edge_softness,
                arm_position
            );


        float trailing =
            1.0 -
            smoothstep(
                u_arm_width,
                u_arm_width + u_trailing_edge_softness,
                arm_position
            );


        pattern =
            leading *
            trailing;
    }

    //--------------------------------------------------------
    // Color
    //--------------------------------------------------------

    vec3 color =
        sample_palette(pattern);

    color *=
        u_intensity;


    //--------------------------------------------------------
    // Iris Transition
    //--------------------------------------------------------

    frag_color =
        apply_iris(
            vec4(color, 1.0),
            uv
        );
        
}