#version 120

#define MAX_LIGHTS 1
struct LightProps
{
    vec3 direction[MAX_LIGHTS];
};

uniform sampler2D textureUnit;
uniform sampler2D normalTextureUnit;
uniform vec4 TexColor;



void main()
{
    vec3 N = normalize(texture2D(normalTextureUnit,gl_TexCoord[0].st).rgb*2.0-1.0);

    vec4 color = vec4(0,0,0,0);
    for(int i = 0; i < MAX_LIGHTS; i++)
    {
        vec3 L = lights.direction[i];
        float dist = length(L);
        L = normalize(L);

        float NdotL = max(dot(N,L),0.0);

        if(NdotL > 0)
        {
            float att = 1.0;
            if(gl_LightSource[i].position.w > 0)
            {
                att = 1.0/ (gl_LightSource[i].constantAttenuation +
                gl_LightSource[i].linearAttenuation * dist +
                gl_LightSource[i].quadraticAttenuation * dist * dist);
            }
            
            vec4 ambient = gl_FrontLightProduct[i].ambient;
            vec4 diffuse = clamp(att*NdotL*gl_FrontLightProduct[i].diffuse,0,1);
        
            color += att*(ambient+diffuse);
        }
    }

    vec4 textureColor = texture2D(textureUnit, vec2(gl_TexCoord[0]));
    gl_FragColor = TexColor*textureColor + gl_FrontLightModelProduct.sceneColor + color;
}