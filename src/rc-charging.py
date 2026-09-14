import numpy as np
import matplotlib.pyplot as plt

V0 = 5.0
VIH = 0.7 * V0

# Use the R and C you specified for YOUR application in Part A,
# and a tolerance you can justify from a real datasheet (do not
# reuse the tutorial's 83 kOhm / 100 nF +-10% demonstration values).
R_nominal = 100e3      # 100 kOhm resistor for the HD55 POR circuit
C_nominal = 0.1e-6     # 0.1 uF capacitor
R_tolerance = 0.05     # +-5%, typical metal-film resistor datasheet
C_tolerance = 0.20     # +-20%, typical X7R ceramic capacitor datasheet

# Fastest-case and slowest-case R, C combinations this tolerance permits.
# Since t_release = -RC*ln(1 - VIH/V0) increases monotonically with the
# RC product, the shortest t_release comes from the smallest R and
# smallest C together, and the longest from the largest R and largest C.
R_fast = R_nominal * (1 - R_tolerance)
C_fast = C_nominal * (1 - C_tolerance)
R_slow = R_nominal * (1 + R_tolerance)
C_slow = C_nominal * (1 + C_tolerance)

def t_release(R, C):
    return -R * C * np.log(1 - VIH / V0)

t_nominal = t_release(R_nominal, C_nominal)
t_fast = t_release(R_fast, C_fast)
t_slow = t_release(R_slow, C_slow)

def charging(t, R, C):
    tau = R * C
    return V0 * (1 - np.exp(-t / tau))

tau_max = R_slow * C_slow
t = np.linspace(0, 5 * tau_max, 500)

styles = ["--", (0, (3, 1, 1, 1, 1, 1))]

fig, ax = plt.subplots()
ax.plot(t, charging(t, R_nominal, C_nominal), color="black", linewidth=2.5,
        label=f"R = {R_nominal/1e3:.0f}k$\\Omega$, C = {C_nominal*1e6:.1f}$\\mu$F (nominal)")
ax.plot(t, charging(t, R_fast, C_fast), color="black", linestyle=styles[0], linewidth=1.3,
        label=f"R = {R_fast/1e3:.0f}k$\\Omega$, C = {C_fast*1e6:.2f}$\\mu$F (fastest)")
ax.plot(t, charging(t, R_slow, C_slow), color="black", linestyle=styles[1], linewidth=1.3,
        label=f"R = {R_slow/1e3:.0f}k$\\Omega$, C = {C_slow*1e6:.2f}$\\mu$F (slowest)")

ax.axhline(VIH, linestyle=":", color="0.4")
ax.grid(False)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.set_title("Capacitor charging under R (\u00b15%) and C (\u00b120%) tolerance")
ax.legend()
fig.savefig(r"C:\Users\andre\PycharmProjects\rc-charging-poc\figures\generated\rc_tolerance.pdf")