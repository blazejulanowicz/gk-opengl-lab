#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewport_width = 400
viewport_height = 400

def startup():
    update_viewport(None, viewport_width, viewport_height)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def mandelbrota(x, y):
    c = complex(x,y)
    prev_z = complex(0,0)

    for i in range(1,25):
        prev_z = prev_z*prev_z + c
        if abs(prev_z) >= 2:
            return False
    return True

def drawSet(offset_x, offset_y, scale):
    glBegin(GL_POINTS)
    for x in range(-viewport_width,viewport_width):
        for y in range(-viewport_height, viewport_height):
            if mandelbrota(offset_x+(x/(scale*viewport_width)), offset_y+(y/(scale*viewport_height)) ):
                glColor(1.0, 1.0, 0.0)
            else:
                glColor(0.0, 0.0, 0.5)
            glVertex2f(x,y)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    drawSet(-0.7, 0, 0.8)
    glFlush()


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    glOrtho(-viewport_width, viewport_width, -viewport_height, viewport_height,-1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    render(glfwGetTime())


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(viewport_width, viewport_height, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
