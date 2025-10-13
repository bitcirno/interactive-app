#version 120

uniform sampler2D imageTexture;
uniform vec2 resolution;
varying vec2 fragmentTexCoord;


vec2 crtDistortion(vec2 uv) {
    uv = uv * 0.9 + 0.05; // [0.05, 0.95]
    uv = uv * 2.0 - 1.0;  // [-1, 1]
    float r = length(uv);
    uv *= 1.0 + 0.07 * r * r; // distortion strength
    uv = (uv + 1.0) * 0.5;    // [0, 1]
    return uv;
}

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
    gl_FragColor = vec4(color, 1.0);
}
