from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glUseProgram, glDeleteProgram

class Shader:
    def __init__(self):
        self.m_ProgramId = -1

    def create_program(self, vert_shader_code : str, frag_shader_code : str):
        self.m_ProgramId = compileProgram(
            compileShader(vert_shader_code, GL_VERTEX_SHADER),
            compileShader(frag_shader_code, GL_FRAGMENT_SHADER)
        )
    
    def Use(self):
        glUseProgram(self.m_ProgramId)

    def Destroy(self):
        glDeleteProgram(self.m_ProgramId)