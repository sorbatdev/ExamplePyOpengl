# external
from ctypes import c_void_p
from OpenGL.GL import *
import glm
import numpy as np

# internal
from shader import Shader
from window import *
from keycodes import *

width = 1280
height = 720
forward = False
back = False

aspect = GLfloat(width / height)

def OnKeyPressed(key):
    if key == KEY_W:
        global forward 
        forward = True
    elif key == KEY_S:
        global back
        back = True

def OnKeyReleased(key):
    global forward, back
    if key == KEY_W:
        forward = False
    elif key == KEY_S:
        back = False

AddToCallback(EVENT_KEY_PRESS, OnKeyPressed)
AddToCallback(EVENT_KEY_RELEASE, OnKeyReleased)

window = Window(width, height, "Window")

# attaching to a variable is optional
m_GLFWwindow = window.Create()

s = Shader("basicshader")

vertices = np.array([
     0.5,  0.5, 0.0,
     0.5, -0.5, 0.0,
    -0.5, -0.5, 0.0,
    -0.5,  0.5, 0.0
], dtype=np.float32)

indices = np.array([
    0, 1, 3,   
    1, 2, 3 
], dtype=np.uint32)

vao = glGenVertexArrays(1)

vbo = glGenBuffers(1)
# ebo = glGenBuffers(1)

glBindVertexArray(vao)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * len(vertices), vertices, GL_STATIC_DRAW)

# glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
# glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), c_void_p(0))
glEnableVertexAttribArray(0)

model = glm.mat4(1.0)
view = glm.lookAt(
    glm.vec3(0.0, 0.0, -3.0),
    glm.vec3(0.0, 0.0, 0.0),
    glm.vec3(0.0, 1.0, 0.0)
)
projection = glm.perspective(glm.radians(60.0),float(width)/float(height),0.1,1000.0)

pv = projection * view

def Move():
    global model
    if forward:
        model = glm.translate(model, glm.vec3(0.0, 0.0, -0.01))
    if back:
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.01))

# set the clear color once
glClearColor(0.3, 0.534, 0.12, 1.0)

while (not window.ShouldClose()):
    glClear(GL_COLOR_BUFFER_BIT)

    Move()
    s.Use()
    glBindVertexArray(vao)
    glUniformMatrix4fv(glGetUniformLocation(s.m_ProgramId, "pv"), 1, GL_FALSE, glm.value_ptr(pv))
    glUniformMatrix4fv(glGetUniformLocation(s.m_ProgramId, "model"), 1, GL_FALSE, glm.value_ptr(model))
    glDrawArrays(GL_TRIANGLES, 0, 6)
    
    window.Update()

glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
s.Destroy()
window.Terminate()