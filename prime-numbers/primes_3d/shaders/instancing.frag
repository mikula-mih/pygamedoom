#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;
in vec3 primeColor;
in float prime;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
uniform sampler2DShadow shadowMap;
uniform vec2 u_resolution;
uniform samplerCube u_texture_skybox;
//uniform float u_time;


float getShadow() {
    float shadow = textureProj(shadowMap, shadowCoord);
    return shadow;
}


float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / u_resolution;
    return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                     oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
}


float getSoftShadowX16() {
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}


float getSoftShadowX64() {
    float shadow;
    float swidth = 0.6;
    float endp = swidth * 3.0 + swidth / 2.0;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 64;
}


vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);

    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    float shadow = getSoftShadowX64();// * 0.00001 + 0.99999;
    return color * (ambient + (diffuse + specular) * shadow);
}


float linearizeDepth(float depth) {
    float nearz = 0.1;
    float farz = 300.0;
    return 2.0 * nearz * farz / (farz + nearz - (2.0 * depth - 1.0) * (farz - nearz));
}


vec3 sRGBtoLinear(vec3 color) {
    float gamma = 2.2;
    return pow(color, vec3(gamma));
}


vec3 getReflection() {
    vec3 viewDir = fragPos - camPos;
    vec3 reflectedDir = reflect(viewDir, normalize(normal));
    return texture(u_texture_skybox, reflectedDir).rgb;
}


void main() {
    vec3 color = sRGBtoLinear(texture(u_texture_0, uv_0).rgb);
    if (prime < 0) {
        color *= getLight(sRGBtoLinear(getReflection())) * 2.5;
    } else {
        color *= 0.0000001;
        color += primeColor * getLight(sRGBtoLinear(getReflection())) * 3.5;
//        color += primeColor * 0.000001 + getLight(sRGBtoLinear(getReflection())) * 0.00001;
//        color = getLight(primeColor);
    }

//    color *= getLight(sRGBtoLinear(getReflection())) * 2.5;

    float gamma = 2.2;
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
//
//    float depth = gl_FragCoord.z;
//    float linearized = (linearizeDepth(depth) - 2.0) / 60;
//    fragColor = vec4(color, 1.0) * 0.000001 + vec4(vec3(linearized), 1.0);
}










