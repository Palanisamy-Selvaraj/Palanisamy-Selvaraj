import numpy as np

class DigitalTwinEngine:
    def __init__(self, sigma=0.1):
        # System Matrices (Example: A simple mass-spring-damper)
        self.A = np.array([[1.0, 0.1], [-0.01, 1.0]])
        self.B = np.array([[0], [0.1]])
        self.K = np.array([[0.1, 0.5]]) # Control Gain
        self.sigma = sigma
        self.x_physical = np.array([[1.0], [0.0]])
        self.x_twin = np.array([[1.0], [0.0]])
        self.u = np.zeros((1, 1))

    def update_step(self):
        # 1. Calculate Error
        error = np.linalg.norm(self.x_physical - self.x_twin)
        triggered = False

        # 2. Event-Triggered Logic
        if error > self.sigma:
            self.x_twin = self.x_physical.copy() # Sync Twin to Physical
            self.u = -self.K @ self.x_twin       # Update Control
            triggered = True

        # 3. Simulate Physical Evolution
        self.x_physical = self.A @ self.x_physical + self.B @ self.u
        return self.x_physical, self.x_twin, triggered
