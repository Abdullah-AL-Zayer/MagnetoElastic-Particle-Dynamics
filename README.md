# MagnetoElastic-Particle-Dynamics
Interactive particle simulation with magnetic repulsion and spring-like attraction.
# MagnetoElastic Dynamics

An interactive particle simulation built with Python and Pygame.

Particles interact through two simple mechanisms:

* Short-range magnetic-like repulsion.
* Medium-range spring-like attraction through dynamic connections.

When particles come within a certain distance, a connection appears between them and an attractive force is applied. At very short distances, a repulsive force prevents particles from collapsing into each other.

## Features

* Interactive particle creation using mouse drag.
* Adjustable physical parameters.
* Dynamic connection network.
* Real-time visualization using Pygame.

## Adjustable Parameters

The simulation behavior can be modified by changing the constants at the beginning of the source code:

* "MAGNETIC_RANGE"
* "CONNECTION_RANGE"
* "SPRING_K"
* "REPULSION_STRENGTH"
* "FRICTION"

## Controls

* Drag with the mouse to create a particle and set its initial velocity.
* Press **Clear** to remove all particles.

## Technologies

* Python
* Pygame

## Purpose

This project explores emergent behavior in a simple particle system driven by attraction and repulsion forces.
