# Description: This script demonstrates the Euler angle rotations in 3D space.
# Author: Ronen Aniti
# Date: Aug. 11, 2024
# Python Version: 3.7
# Dependencies: numpy, matplotlib
# Usage: python euler_rotations.py
# Reference: https://en.wikipedia.org/wiki/Euler_angles

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class Frame:
    def __init__(self):
        self.origin = np.array([0.0, 0.0, 0.0])  # Initialize with floating-point values
        self.R = np.eye(3)

    def translate(self, d):
        """
        Translate the frame by a vector, d. 
        """
        self.origin += d

    def rotate(self, phi, theta, psi):
        """
        Rotate the frame with an Euler angle sequence (phi, theta, psi).
        """
        Rz = np.array([
            [np.cos(psi), -np.sin(psi), 0],
            [np.sin(psi), np.cos(psi), 0],
            [0, 0, 1]
        ])
        
        Ry = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(phi), -np.sin(phi)],
            [0, np.sin(phi), np.cos(phi)]
        ])

        self.R = Rz @ self.R
        self.R = Ry @ self.R
        self.R = Rx @ self.R

    def plot(self, ax, label):
        """
        Plot the frame on the given axes.
        """
        ax.quiver(*self.origin, *self.R[0], color='r', label=f'{label} X')
        ax.quiver(*self.origin, *self.R[1], color='g', label=f'{label} Y')
        ax.quiver(*self.origin, *self.R[2], color='b', label=f'{label} Z')

def plot_frames(world, body, ax, path):
    """
    Plot the world and body frames and the path.
    """
    ax.clear()
    world.plot(ax, 'World Frame')
    body.plot(ax, 'Body Frame')
    ax.plot(path[:, 0], path[:, 1], path[:, 2], 'k--', label='Path')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

def action(body, dx, dy, dz, dphi, dtheta, dpsi):
    """
    Apply a sequence of actions (translation and rotation) to the body frame.
    """
    body.translate(np.array([dx, dy, dz]))
    body.rotate(dphi, dtheta, dpsi)

def update(frame, world, body, ax, trajectory, path):
    """
    Update function for the animation.
    """
    t, dx, dy, dz, dphi, dtheta, dpsi = trajectory[frame]
    action(body, dx, dy, dz, 0, 0, dpsi)  # Apply psi rotation
    path.append(body.origin.copy())
    plot_frames(world, body, ax, np.array(path))
    action(body, 0, 0, 0, 0, dtheta, 0)  # Apply theta rotation
    path.append(body.origin.copy())
    plot_frames(world, body, ax, np.array(path))
    action(body, 0, 0, 0, dphi, 0, 0)  # Apply phi rotation
    path.append(body.origin.copy())
    plot_frames(world, body, ax, np.array(path))

if __name__ == "__main__":
    # Create a World Frame
    world = Frame()

    # Create a Body Frame
    body = Frame()

    # Define a smooth trajectory function
    def trajectory_function(t):
        dx = 0.01 * np.sin(t)
        dy = 0.01 * np.cos(t)
        dz = 0.01 * t / 10
        dphi = 0.01 * np.sin(t / 2)
        dtheta = 0.01 * np.cos(t / 2)
        dpsi = 0.01 * np.sin(t / 3)
        return dx, dy, dz, dphi, dtheta, dpsi

    # Generate trajectory data with small timesteps
    timesteps = np.arange(0, 10, 0.01)
    trajectory = [(t, *trajectory_function(t)) for t in timesteps]

    # Create a figure and axis for the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # List to store the path of the body frame's origin
    path = []

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(trajectory), fargs=(world, body, ax, trajectory, path), interval=10)

    plt.show()