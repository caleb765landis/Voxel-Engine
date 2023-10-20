#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2D u_texture_0;

in vec3 voxel_color;
in vec2 uv;
in float shading;

void main() {
    vec3 tex_color = texture(u_texture_0, uv).rgb;

    // all actions with textures should be carried out in linear color space
    // so make a gamma color correction
    tex_color = pow(tex_color, gamma);

    tex_color.rgb *= voxel_color;
    // tex_color = tex_color * 0.001 + vec3(1);
    tex_color *= shading;

    fragColor = vec4(tex_color, 1);
}