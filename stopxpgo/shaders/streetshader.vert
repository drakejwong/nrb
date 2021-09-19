#version 120

#define MAX_LIGHTS 1

struct LightProps
{
    vec3 direction[MAX_LIGHTS];
};

attribute vec3 tangent;
attribute vec3 bitangent;



void main()
{
    vec3 N = normalize(gl_NormalMatrix*gl_Normal);
    vec3 T = normalize(gl_NormalMatrix*tangent);
    vec3 B = normalize(gl_NormalMatrix*bitangent);

    mat3 TBNMatrix = mat3(T,B,N);

    vec4 vertex = gl_ModelViewMatrix* p3d_Vertex;
    for(int i = 0; i < MAX_LIGHTS; i++)
    {
        vec4 lightPos = gl_LightSource[i].position;
        lights.direction[i] = vec3(lightPos.w > 0 ? lightPos-vertex : lightPos);
        lights.direction[i] *= TBNMatrix;
    }

    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = gl_ModelViewProjectionMatrix*gl_Vertex;
} 
