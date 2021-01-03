#!/usr/bin/env python3
import sys
import math
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

##DEFINED

visible_walls = 4
images = [None, None]
N = 10

def startup():
    global images

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    images[0] = Image.open("kowal.tga")
    images[1] = Image.open("grzesiek.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, images[0].size[0], images[0].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, images[0].tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def generate_egg_vertices(offset):
    
    distance = 1.0/(N-1)
    vertices = np.zeros((N, N, 3))

    for i in range(0, N):
        for j in range(0, N):
            u = distance*i
            v = distance*j
            vertices[i][j][0] = (-90*pow(u,5) + 225*pow(u,4) - 270*pow(u,3) + 180*pow(u,2) - 45*u) * math.cos(math.pi * v) + offset[0]
            vertices[i][j][1] = 160 * pow(u,4) - 320 * pow(u,3) + 160 * pow(u,2) + offset[1]
            vertices[i][j][2] = (-90*pow(u,5) + 225*pow(u,4) - 270*pow(u,3) + 180*pow(u,2) - 45*u) * math.sin(math.pi * v) + offset[2]
    
    return vertices


def draw_egg_triangles(vertices):
    glBegin(GL_TRIANGLES)
    distance = 1.0/(N-1)
    for i in range(0, N-1):
        if i < (N-1)/2:
            for j in range(0, N-1):
                u = (distance*i)*2
                v = distance*j

                glTexCoord2f(v,u)
                glVertex(vertices[i][j])
                glTexCoord2f(v,u+distance*2)
                glVertex(vertices[i+1][j])
                glTexCoord2f(v+distance,u)
                glVertex(vertices[i][j+1])
                glTexCoord2f(v+distance,u+distance*2)
                glVertex(vertices[i+1][j+1])
                glTexCoord2f(v+distance,u)
                glVertex(vertices[i][j+1])
                glTexCoord2f(v,u+distance*2)
                glVertex(vertices[i+1][j])
        else:
            for j in range(0, N-1):
                u = (distance*i)*2
                v = distance*j

                glTexCoord2f(v,1.0-(u+distance*2))
                glVertex(vertices[i+1][j])
                glTexCoord2f(v,1.0-u)
                glVertex(vertices[i][j])
                glTexCoord2f(v+distance,1.0-u)
                glVertex(vertices[i][j+1])

                glTexCoord2f(v,1.0-(u+distance*2))
                glVertex(vertices[i+1][j])
                glTexCoord2f(v+distance,1.0-u)
                glVertex(vertices[i][j+1])
                glTexCoord2f(v+distance,1.0-(u+distance*2))
                glVertex(vertices[i+1][j+1])
                
    glEnd()

def render(time, vertices):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    draw_egg_triangles(vertices)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global visible_walls
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_Q and action == GLFW_PRESS:
        visible_walls = (visible_walls+1)%5
    elif key == GLFW_KEY_1 and action == GLFW_PRESS:
        glTexImage2D(
        GL_TEXTURE_2D, 0, 3, images[0].size[0], images[0].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, images[0].tobytes("raw", "RGB", 0, -1)
        )
    elif key == GLFW_KEY_2 and action == GLFW_PRESS:
        glTexImage2D(
        GL_TEXTURE_2D, 0, 3, images[1].size[0], images[1].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, images[1].tobytes("raw", "RGB", 0, -1)
        )



def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    vertices = generate_egg_vertices([0, -4.5, 0])
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), vertices)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
