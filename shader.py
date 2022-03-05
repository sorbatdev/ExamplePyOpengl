from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glUseProgram, glDeleteProgram

class Shader:
    def __init__(self, shader_name):
        self.m_ShaderName = shader_name
        self.m_VertShaderPath = "shaders/" + shader_name + ".vert"
        self.m_FragShaderPath = "shaders/" + shader_name + ".frag"

        m_VertCode = ""
        m_FragCode = ""
        with open(self.m_VertShaderPath, mode='r') as f:
            m_VertCode = f.read()

        with open(self.m_FragShaderPath, mode='r') as f:
            m_FragCode = f.read()

        self.m_ProgramId = Shader.create_program(m_VertCode, m_FragCode)

    @staticmethod
    def create_program(vert_shader_code : str, frag_shader_code : str):
        program_id = compileProgram(
            compileShader(vert_shader_code, GL_VERTEX_SHADER),
            compileShader(frag_shader_code, GL_FRAGMENT_SHADER)
        )

        return program_id
    
    def Use(self):
        glUseProgram(self.m_ProgramId)

    def Destroy(self):
        glDeleteProgram(self.m_ProgramId)