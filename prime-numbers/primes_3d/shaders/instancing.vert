#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;
layout (location = 3) in vec3 in_offset;
layout (location = 4) in float in_prime;

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;
out vec4 shadowCoord;
out vec3 primeColor;
out float prime;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;
uniform mat4 m_view_light;

mat4 m_shadow_bias = mat4(
    0.5, 0.0, 0.0, 0.0,
    0.0, 0.5, 0.0, 0.0,
    0.0, 0.0, 0.5, 0.0,
    0.5, 0.5, 0.5, 1.0
);


vec3 hash31(float p) {
   vec3 p3 = fract(vec3(p) * vec3(0.1031, 0.1030, 0.0973));
   p3 += dot( p3, p3.yzx + 33.33);
   return fract((p3.xxy + p3.yzz) * p3.zyx);
}


void main() {
    prime = in_prime;
    primeColor = hash31(in_prime);// * 3);
    uv_0 = in_texcoord_0;

    vec3 position = in_position + in_offset;
    fragPos = vec3(m_model * vec4(position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(position, 1.0);

    mat4 shadowMVP = m_proj * m_view_light * m_model;
    shadowCoord = m_shadow_bias * shadowMVP * vec4(position, 1.0);
    shadowCoord.z -= 0.0005;
}