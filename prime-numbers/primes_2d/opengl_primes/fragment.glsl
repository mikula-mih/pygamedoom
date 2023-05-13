#version 330 core
layout(location = 0) out vec4 fragColor;

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;


bool isPrime(int n) {
    if (n == 2) return true;
    if (n < 2 || n % 2 == 0) return false;
    for (int i = 3; i <= int(sqrt(float(n))); i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}


vec3 hash31(float p) {
   vec3 p3 = fract(vec3(p) * vec3(0.1031, 0.1030, 0.0973));
   p3 += dot(p3, p3.yzx + 33.33);
   return fract((p3.xxy + p3.yzz)*p3.zyx) + 0.25;
}


void main() {
    float zoom = sin(u_time * 0.2) * 0.2 + 0.3;
    vec2 uv = gl_FragCoord.xy * zoom + 30.0 * u_time;
    vec3 color = vec3(0);

    int num = int(uv.x) | int(uv.y);
    if (isPrime(num)) color += hash31(num);

    fragColor = vec4(color, 1.0);
}

