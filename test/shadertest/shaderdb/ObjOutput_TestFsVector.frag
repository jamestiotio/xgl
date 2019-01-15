#version 450 core

layout(location = 0) in flat ivec3 i0;
layout(location = 1) in vec3 i1;

layout(location = 0) out ivec3 o0;
layout(location = 1) out vec3 o1;

void main()
{
    o0 = i0;
    o1 = i1;
}
// BEGIN_SHADERTEST
/*
; RUN: amdllpc -v %gfxip %s | FileCheck -check-prefix=SHADERTEST %s
; SHADERTEST-LABEL: {{^// LLPC}} SPIRV-to-LLVM translation results
; SHADERTEST: AMDLLPC SUCCESS
*/
// END_SHADERTEST