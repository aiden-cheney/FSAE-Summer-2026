# tire_model.py

import numpy as np
import matplotlib.pyplot as plt

# Cornering stiffness — typical FSAE tire value
C_alpha = 800  # N/deg

# Slip angle range
alpha = np.linspace(0, 10, 200)  # degrees

# Linear tire model
F_lateral = C_alpha * alpha

plt.figure(figsize=(8, 5))
plt.plot(alpha, F_lateral, color='darkorange', linewidth=2.5, label='Linear model')
plt.axvline(x=3, color='gray', linestyle='--', alpha=0.6, label='Linear limit (~3°)')
plt.xlabel('Slip Angle (degrees)', fontsize=12)
plt.ylabel('Lateral Force (N)', fontsize=12)
plt.title('Lateral Force vs Slip Angle — Linear Tire Model', fontsize=13)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('tire_model_linear.png', dpi=150)
plt.show()