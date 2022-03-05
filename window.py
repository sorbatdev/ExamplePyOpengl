from glfw.GLFW import *

EVENT_KEY_PRESS   = 0
EVENT_KEY_RELEASE = 1
EVENT_KEY_REPEAT  = 2

EVENT_WINDOW_RESIZE         = 3
EVENT_WINDOW_FBUFFER_RESIZE = 4
EVENT_WINDOW_CLOSE          = 5

EVENT_MOUSE_MOVE    = 6
EVENT_MOUSE_PRESS  = 7
EVENT_MOUSE_RELEASE = 8

# this can probably be a normal list
m_Callbacks = {
    EVENT_KEY_PRESS   : [],
    EVENT_KEY_RELEASE : [],
    EVENT_KEY_REPEAT  : [],
    EVENT_WINDOW_RESIZE : [],
    EVENT_WINDOW_FBUFFER_RESIZE: [],
    EVENT_WINDOW_CLOSE : [],
    EVENT_MOUSE_MOVE : [],
    EVENT_MOUSE_PRESS : [],
    EVENT_MOUSE_RELEASE : []
}

def AddToCallback(cb_type : int, callback_function):
    """
    Examples of callbacks are below:\n

    ==          cb_type         ||         Callback body     ==\n
    \n
    EVENT_KEY_PRESS             ->     def OnKeyPressed(key) \n
    EVENT_KEY_RELEASE           ->     def OnKeyReleased(key)\n
    EVENT_WINDOW_RESIZE         ->     def OnWindowResize(width, height)\n
    EVENT_WINDOW_FBUFFER_RESIZE ->     def OnFramebufferResize(width, height)\n
    EVENT_WINDOW_CLOSE          ->     def OnWindowClose()\n
    EVENT_MOUSE_MOVE            ->     def OnMouseMoved(mouse_x, mouse_y)\n
    EVENT_MOUSE_PRESS           ->     def OnMouseButtonPress(mouse_x, mouse_y, mouse_button)\n
    EVENT_MOUSE_RELEASE         ->     def OnMouseButtonsRelease(mouse_x, mouse_y, mouse_button)\n
    """
    m_Callbacks.get(cb_type).append(callback_function)


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
        
        self.m_Window = glfwCreateWindow(self.width, self.height, self.title, None, None)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, self.version_major)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, self.version_minor)
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

        glfwMakeContextCurrent(self.m_Window)

        glfwSetKeyCallback(self.m_Window, Window.OnKeyEvent)

        glfwSetWindowSizeCallback(self.m_Window, Window.OnWindowResize)
        glfwSetFramebufferSizeCallback(self.m_Window, Window.OnWindowFramebufferResize)
        glfwSetWindowCloseCallback(self.m_Window, Window.OnWindowClose)

        glfwSetCursorPosCallback(self.m_Window, Window.OnMouseMove)
        glfwSetMouseButtonCallback(self.m_Window, Window.OnMouseButton)

        return self.m_Window # returns the _GLFWwindow, but this is optional

    def Update(self):
        glfwSwapBuffers(self.m_Window)
        glfwPollEvents()

    def ShouldClose(self):
        return glfwWindowShouldClose(self.m_Window)

    def Terminate(self):
        glfwDestroyWindow(self.m_Window)
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
    def OnWindowResize(_, width, height):
        for callback in m_Callbacks.get(EVENT_WINDOW_RESIZE):
            callback()

    @staticmethod
    def OnWindowFramebufferResize(_, width, height):
        for callback in m_Callbacks.get(EVENT_WINDOW_FBUFFER_RESIZE):
            callback()

    @staticmethod
    def OnWindowClose(_):
        for callback in m_Callbacks.get(EVENT_WINDOW_CLOSE):
            callback()

    @staticmethod
    def OnMouseMove(_, x, y):
        for callback in m_Callbacks.get(EVENT_WINDOW_CLOSE):
            callback(x, y)

    @staticmethod
    def OnMouseButton(window, button, action, mods):
        x, y = glfwGetCursorPos(window)
        if action == GLFW_PRESS:
            for callback in m_Callbacks.get(EVENT_MOUSE_PRESS):
                callback(x, y, button)
        elif action == GLFW_RELEASE:
            for callback in m_Callbacks.get(EVENT_MOUSE_RELEASE):
                callback(x, y, button)