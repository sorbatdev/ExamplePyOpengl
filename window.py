from glfw.GLFW import *

EVENT_KEY_PRESS   = 0
EVENT_KEY_RELEASE = 1
EVENT_KEY_REPEAT  = 2

EVENT_WINDOW_RESIZE         = 3
EVENT_WINDOW_FBUFFER_RESIZE = 4
EVENT_WINDOW_CLOSE          = 5

m_Callbacks = {
    EVENT_KEY_PRESS   : [],
    EVENT_KEY_RELEASE : [],
    EVENT_KEY_REPEAT  : [],
    EVENT_WINDOW_RESIZE : [],
    EVENT_WINDOW_FBUFFER_RESIZE: [],
    EVENT_WINDOW_CLOSE : []
}

def AddToCallback(cb_type, cb):
    m_Callbacks.get(cb_type).append(cb)


# Window class for a single instance of a glfwWindow
class Window:
    kIsInitialized = False

    def __init__(self, width : int, height: int, title : str, version_major : int = 3, version_minor : int = 3):
        self.width = width
        self.height = height
        self.title = title
        self.version_major = version_major
        self.version_minor = version_minor
    
    def Create(self):
        if not Window.kIsInitialized:
            glfwInit()
            Window.kIsInitialized = True
        
        self.window = glfwCreateWindow(self.width, self.height, self.title, None, None)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, self.version_major)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, self.version_minor)
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

        glfwMakeContextCurrent(self.window)

        glfwSetKeyCallback(self.window, Window.OnKeyEvent)
        glfwSetWindowCloseCallback(self.window, Window.OnWindowClose)

        return self.window # returns the _GLFWwindow, but this is optional

    def Update(self):
        glfwSwapBuffers(self.window)
        glfwPollEvents()

    def ShouldClose(self):
        return glfwWindowShouldClose(self.window)

    def Terminate(self):
        glfwDestroyWindow(self.window)
        glfwTerminate()

    @staticmethod
    def OnKeyEvent(_, key, scancode, action, mods):
        if action == GLFW_PRESS:
            for callback in m_Callbacks.get(EVENT_KEY_PRESS):
                callback(key)
        if action == GLFW_RELEASE:
            for callback in m_Callbacks.get(EVENT_KEY_RELEASE):
                callback(key)

    @staticmethod
    def OnWindowClose(window):
        for callback in m_Callbacks.get(EVENT_WINDOW_CLOSE):
            callback()
