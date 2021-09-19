#version 330

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;


  vec4 baseColor;
  float roughness;
  float metallic;
  float refractiveIndex;
} p3d_Material;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec2 p3d_MultiTexCoord1;
in vec2 p3d_MultiTexCoord2;
in vec4 p3d_Color;

// Output to fragment shader
out vec4 vertexColor;
out vec2 texcoord;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  texcoord = p3d_MultiTexCoord0;
  vertexColor = vec4(0.5, 0.0, 0.0, 1.0);
}