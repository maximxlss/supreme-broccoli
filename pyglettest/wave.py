# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import GL_POINTS
from pyglet.window import key
import pyshaders
import numpy as np
from collections import Counter
import time
    
    
frag = """
#version 330 core
in vec3 out_color;
uniform float time;
out vec4 color_frag;
void main()
{
  color_frag = vec4(out_color.xy, sin(time)+1./2+0.1, 1.0);
}
"""

vert = """
#version 330 core
uniform float time;
uniform float coffee = 50;
uniform float coffe = 10;
out vec3 out_color;
layout(location = 0)in vec2 vert;
void main()
{
  float co = sin(vert.x*10+time);
  vec4 pos = vec4(vert.x-co/coffee, vert.y+co/coffe, 1, 1);
  while(pos.x > 1){pos.x -= 2;}
  while(pos.x < -1){pos.x += 2;}
  while(pos.y > 1){pos.y -= 2;}
  while(pos.y < -1){pos.y += 2;}
  gl_Position = pos;
  out_color = vec3(clamp(co, 0., 1.), abs(clamp(co, -1., 0.)), 1.);
}
"""
    
start = time.time()
    
# Window creation
window = pyglet.window.Window(visible=True, width=300, height=300, resizable=True)


#Shader creation
shader = pyshaders.from_string(vert, frag)
shader.use()

N_Points = 1000000

a = np.random.random_sample((N_Points*2,))*2-1.

tris = pyglet.graphics.vertex_list(N_Points,
    ('v2f', a),
)

@window.event
def on_draw():
    window.clear()
    tris.draw(GL_POINTS)
    #tris.vertices = np.random.random_sample((N_Points*2,))*2-1.
    
def update(_):
    shader.uniforms.time = time.time() - start

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.S:
        shader.uniforms.coffe *= 2
    if symbol == key.W:
        shader.uniforms.coffe /= 2
    if symbol == key.D:
        shader.uniforms.coffee *= 2
    if symbol == key.A:
        shader.uniforms.coffee /= 2


pyglet.clock.schedule_interval(update, 1/120.0)

pyglet.app.run()
