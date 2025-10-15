#version 120

in vec3 fragmentColor;
in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;

uniform float speed;
uniform float time;

void main() {
    vec2 uv1 = fragmentTexCoord;
    uv1.x += time * speed;
    vec4 col1 = texture2D(imageTexture, uv1);

//    vec2 uv2 = fragmentTexCoord;
//    uv2.x -= time*speed;
//    uv2.y += 7/resolution.y;
//    vec4 col2 = texture2D(imageTexture, uv2);

//    vec4 col = col1 * col2;
//    col.a = col1.a + col2.a;
//    gl_FragColor = col;
    gl_FragColor = col1;
}
