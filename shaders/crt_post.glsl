#version 120

uniform sampler2D imageTexture;
uniform vec2 resolution;
varying vec2 fragmentTexCoord;

uniform float invincible;
uniform float time;

vec2 crtDistortion(vec2 uv) {
    uv = uv * 0.9 + 0.05; // [0.05, 0.95]
    uv = uv * 2.0 - 1.0;  // [-1, 1]
    float r = length(uv);
    uv *= 1.0 + 0.07 * r * r; // distortion strength
    uv = (uv + 1.0) * 0.5;    // [0, 1]
    return uv;
}

vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(K.xyz, c.b), vec4(c.b, K.wz, c.r), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.g));
    float d = q.x - min(q.w, q.y);
    float h = abs(q.z + (q.w - q.y) / (6.0 * d + 1e-16));
    return vec3(h, d / q.x, q.x);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

vec3 softlight_mix(vec3 base, vec3 blend){
    return 2.0 * base * blend + base*base -2.0*base*base*blend;
}

vec3 hueInit = vec3(0.66, 0.42, 0.96);

void main() {
    vec2 uv = crtDistortion(fragmentTexCoord);

    // fill black outside of the safe area
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    // Chromatic Aberration
    vec2 pixel = 1.0 / resolution;
    float shift = 1.2; // shift distance per

    float offset = shift * pixel.x;
    float r = texture2D(imageTexture, uv + vec2(-offset, 0.0)).r;
    float g = texture2D(imageTexture, uv).g;
    float b = texture2D(imageTexture, uv + vec2(offset, 0.0)).b;

    vec3 color = vec3(r, g, b);

    // scanline effect
    float scanline = 0.91 + 0.15 * sin(fragmentTexCoord.y * resolution.y * 3.14159);
    color *= scanline;

    color = pow(color, vec3(1.2));
    if (invincible > 0.5) {
        vec3 hsv = hueInit;
        hsv.r += time * 1;
        vec3 rgb = hsv2rgb(hsv);
        color = softlight_mix(color, rgb);
    }
    gl_FragColor = vec4(color, 1.0);
}
