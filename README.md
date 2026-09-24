# Linear Wave Theory (Airy Wave Theory) Calculator

This repository provides a programmatic implementation of **Linear Wave Theory (Airy Wave Theory)** for regular sinusoidal propagating waves. It includes calculations for velocity potential, dispersion relations, wave profiles, dynamic pressure, particle velocities, and fluid accelerations across both **finite** and **infinite (deep water)** fluid depths.

The equations implemented are based on standard ocean engineering and fluid mechanics formulations.

## Features

Calculates key hydrodynamic properties based on input parameters (wave period \(T\), wavelength \(\lambda\), wave amplitude \(\zeta_a\), water depth \(h\), and gravity \(g\)):

- **Velocity Potential (\(\phi\))**: Solves the Laplace equation using separation of variables.
- **Dispersion Relation**: Solves the connection between wave number \(k\) and circular frequency \(\omega\) (\(\omega^2 = gk \tanh kh\)).
- **Wave Profile (\(\zeta\))**: Evaluates free-surface elevation over time and space.
- **Dynamic Pressure (\(p_D\))**: Determines pressure variations beneath the wave.
- **Kinematics (\(u, w\))**: Computes horizontal (\(x\)) and vertical (\(z\)) components of particle velocity.
- **Dynamics (\(a_x, a_z\))**: Computes horizontal (\(x\)) and vertical (\(z\)) components of fluid particle acceleration.

## Mathematical Formulations

The codebase handles two primary environments derived from the potential flow framework:

### 1. Finite Water Depth
Formulations utilize hyperbolic functions to account for seafloor boundary conditions (\(\frac{\partial \phi}{\partial z} = 0\) at \(z = -h\)):
- **Velocity Potential**: \(\phi = \frac{g \zeta_a}{\omega} \frac{\cosh k(z+h)}{\cosh kh} \cos(\omega t - kx)\)
- **Dispersion Relation**: \(\omega^2 = gk \tanh kh\)

### 2. Infinite Water Depth (Deep Water)
As depth \(h \rightarrow \infty\), the formulations simplify as the bottom boundary effect vanishes (\(e^{kh} \rightarrow \infty\)):
- **Velocity Potential**: \(\phi = \frac{g \zeta_a}{\omega} e^{kz} \cos(\omega t - kx)\)
- **Dispersion Relation**: \(\omega^2 = gk\)

## Repository Structure

```text
├── src/
│   ├── __init__.py
│   ├── core.py          # Core analytical formulas for finite and deep water
│   └── solvers.py       # Iterative solvers for wavelength / wavenumber
├── examples/
│   └── validation.py    # Sample script to generate wave kinematics profiles
├── tests/
│   └── test_theory.py   # Unit tests matching analytical text benchmarks
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+
- NumPy
- SciPy (for iterative dispersion solvers)
- Matplotlib (optional, for visualization)

### Installation
Clone the repository:
```bash
git clone https://github.com
cd linear-wave-theory
pip install -r requirements.txt
```

### Usage Example
```python
from src.core import FiniteWave

# Initialize a wave with amplitude=1m, period=8s, water depth=20m
wave = FiniteWave(amplitude=1.0, period=8.0, depth=20.0)

# Calculate horizontal velocity at x=0, z=-5m (5 meters below surface), t=0
u_velocity = wave.horizontal_velocity(x=0, z=-5, t=0)
print(f"Horizontal Velocity: {u_velocity:.2f} m/s")
```
