#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def drawRectangle(x, y, a, b, d=0.0):
    random.seed(x+y+a+b+d)
    color = [random.random(), random.random(), random.random()]
    color1 = [random.random(), random.random(), random.random()]
    color2 = [random.random(), random.random(), random.random()]

    glBegin(GL_TRIANGLES)
    glColor(color)
    glVertex2f(x-((a+d)/2), y-((b+d)/2))
    glColor(color1)
    glVertex2f(x-((a+d)/2), y+((b+d)/2))
    glColor(color2)
    glVertex2f(x+((a+d)/2), y+((b+d)/2))
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor(color)
    glVertex2f(x-((a+d)/2), y-((b+d)/2))
    glColor(color1)
    glVertex2f(x+((a+d)/2), y-((b+d)/2))
    glColor(color2)
    glVertex2f(x+((a+d)/2), y+((b+d)/2))
    glEnd()

def render(time, rand_value):
    glClear(GL_COLOR_BUFFER_BIT)

    x = float(sys.argv[1])
    y = float(sys.argv[2])
    a = float(sys.argv[3])
    b = float(sys.argv[4])

    drawRectangle(x,y,a,b, rand_value)

    glFlush()


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    rand_value = random.random()
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), rand_value)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
