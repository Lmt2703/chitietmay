"""
simulation_control.py
Mo phong dong luc hoc va he thong dieu khien nhiet do dung dich dinh duong
Mon hoc: Dong luc hoc va Dieu khien He thong - Dai hoc Bach Khoa TP.HCM
Nhom 9 - De tai: He thong loc va lam nguoi nuoc dung dinh duong
Dua tren nghien cuu MDPI Appl. Sci. 2025, 15, 5381 (Cai et al.)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Thiet lap phong chu va tham my cho do thi
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

# -------------------------------------------------------------
# 1. CAC THAM SO VAT LY CUA HE THONG (PHYSICAL PARAMETERS)
# -------------------------------------------------------------
# Mo hinh ham truyen xap xi tu thuc nghiem (MDPI 2025):
# G(s) = (K / (T*s + 1)) * exp(-tau * s)
K = 1.7       # He so khuech dai he thong (°C / kW hoac °C / don vi dieu khien)
T_const = 340.0 # Hang so thoi gian nhiet (giay)
tau = 10.0    # Thoi gian tre thuan (giay)

print(f"He thong ham truyen: G(s) = {K} / ({T_const}*s + 1) * exp(-{tau}*s)")

# -------------------------------------------------------------
# 2. XAP XI PADE VA PHAN TICH TINH ON DINH / ROOT LOCUS
# -------------------------------------------------------------
# Xap xi Pade bac 1 cho khau tre: exp(-tau*s) approx (1 - 0.5*tau*s)/(1 + 0.5*tau*s)
# = (1 - 5*s) / (1 + 5*s)
num_pade = [-5.0, 1.0]
den_pade = [5.0, 1.0]

# Ham truyen khong tre: G0(s) = K / (T*s + 1)
num_g0 = [K]
den_g0 = [T_const, 1.0]

# Ham truyen tuong duong bac 2 co tre Pade:
num_sys = np.convolve(num_g0, num_pade)
den_sys = np.convolve(den_g0, den_pade)
sys_pade = signal.TransferFunction(num_sys, den_sys)

print("Tu so Pade:", num_sys)
print("Mau so Pade:", den_sys)

# -------------------------------------------------------------
# 3. MO PHONG THOI GIAN DONG HOC CHI TIET (TIME-DOMAIN SIMULATION)
# -------------------------------------------------------------
dt = 0.5      # Buoc thoi gian mo phong (giay)
t_end = 600.0 # Tong thoi gian mo phong (giay)
t_span = np.arange(0, t_end, dt)
N = len(t_span)
delay_steps = int(tau / dt)

# Tin hieu dat: Giam nhiet do dung dich xuong 10°C (Vi du tu 32°C xuong 22°C, delta T_ref = -10 hoac normalized = 1.0)
# De tien so sanh voi bai bao khoa hoc, ta chuan hoa tin hieu dat buoc nhay r(t) = 1.0 (hoac 10°C)
r_step = 1.0

# -------------------------------------------------------------
# DINH NGHIA BO DIEU KHIEN FUZZY LOGIC
# -------------------------------------------------------------
class FuzzyPID:
    def __init__(self, Ke=2.0, Kec=0.5, Kup=0.05, Kui=0.01, Kud=0.005,
                 Kp0=2.5, Ki0=0.015, Kd0=8.0):
        self.Ke = Ke
        self.Kec = Kec
        self.Kup = Kup
        self.Kui = Kui
        self.Kud = Kud
        self.Kp0 = Kp0
        self.Ki0 = Ki0
        self.Kd0 = Kd0
        
        # 7 tap mo: NB(-3), NM(-2), NS(-1), ZO(0), PS(1), PM(2), PB(3)
        # Bang luat 49 luat cho dKp, dKi, dKd (theo Table 3 trong bai bao)
        # Ma hoa cac gia tri: NB=-3, NM=-2, NS=-1, ZO=0, PS=1, PM=2, PB=3
        self.rule_dKp = np.array([
            [ 0,  0,  0,  0,  1,  1,  1],
            [ 0,  0,  0,  0,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  2,  2],
            [ 1,  1,  1,  1,  1,  2,  2],
            [ 2,  2,  2,  2,  2,  3,  3],
            [ 2,  2,  2,  2,  2,  3,  3],
            [ 2,  2,  2,  2,  2,  3,  3]
        ])
        
        self.rule_dKi = np.array([
            [-3, -3, -2, -1,  1, -2,  0],
            [-3, -3, -2, -1, -1,  0,  0],
            [-3, -2,  0,  0,  0,  1,  0],
            [-2, -2, -1,  0,  1,  2,  2],
            [ 0, -1,  0,  1,  1,  2,  3],
            [ 0,  0,  1,  2,  2,  3,  3],
            [ 0,  0,  1,  2,  2,  3,  3]
        ])
        
        self.rule_dKd = np.array([
            [-1, -1, -1, -1, -1,  1,  1],
            [-1, -1, -1, -1, -1,  1,  2],
            [-1, -1, -1,  0,  0,  1,  2],
            [-1, -1, -1,  0,  0,  1,  2],
            [-1, -1,  0,  0,  0,  1,  2],
            [-1, -1,  0,  1,  1,  1,  3],
            [-1, -1,  0,  1,  1,  1,  2]
        ])

    def trimf(self, x, a, b, c):
        """Ham lien thuoc tam giac"""
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        else:
            return (c - x) / (c - b) if c != b else 1.0

    def get_fuzzy_weights(self, val):
        """Chuyen gia tri ro sang trong so tap mo (Universe [-3, 3])"""
        v = np.clip(val, -3.0, 3.0)
        centers = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        weights = np.zeros(7)
        for i in range(7):
            c = centers[i]
            left = c - 1.0 if i > 0 else -4.0
            right = c + 1.0 if i < 6 else 4.0
            weights[i] = self.trimf(v, left, c, right)
        sum_w = np.sum(weights)
        if sum_w > 0:
            weights /= sum_w
        return weights

    def compute(self, e, ec):
        # Luong tu hoa vao mien mo [-3, 3]
        e_fuzz = e * self.Ke * 0.5
        ec_fuzz = ec * self.Kec * 1.0
        
        w_e = self.get_fuzzy_weights(e_fuzz)
        w_ec = self.get_fuzzy_weights(ec_fuzz)
        
        dKp_fuzz = 0.0
        dKi_fuzz = 0.0
        dKd_fuzz = 0.0
        
        for i in range(7):
            for j in range(7):
                weight = w_e[i] * w_ec[j]
                if weight > 0:
                    dKp_fuzz += weight * self.rule_dKp[i, j]
                    dKi_fuzz += weight * self.rule_dKi[i, j]
                    dKd_fuzz += weight * self.rule_dKd[i, j]
        
        # Ty le hoa tro lai mien thuc
        delta_Kp = dKp_fuzz * self.Kup
        delta_Ki = dKi_fuzz * self.Kui
        delta_Kd = dKd_fuzz * self.Kud
        
        Kp = max(0.1, self.Kp0 + delta_Kp)
        Ki = max(0.0001, self.Ki0 + delta_Ki)
        Kd = max(0.0, self.Kd0 + delta_Kd)
        
        return Kp, Ki, Kd

# -------------------------------------------------------------
# 4. THUC THI MO PHONG 3 PHUONG PHAP (PID, FUZZY PID, DBO-FUZZY PID)
# -------------------------------------------------------------
def simulate_system(controller_type="PID", with_disturbance=False):
    # Khoi tao bien trang thai
    y = np.zeros(N) # Nhiet do ngo ra (thay doi delta T)
    u = np.zeros(N) # Tin hieu dieu khien
    e = np.zeros(N) # Sai so
    u_delayed_buffer = np.zeros(delay_steps + 1)
    
    # Khoi tao bo dieu khien
    if controller_type == "PID":
        # PID co dien
        Kp = 4.2
        Ki = 0.022
        Kd = 12.0
    elif controller_type == "Fuzzy_PID":
        # Fuzzy PID mac dinh
        fuzzy = FuzzyPID(Ke=2.0, Kec=0.5, Kup=0.05, Kui=0.01, Kud=0.005,
                         Kp0=3.2, Ki0=0.020, Kd0=15.0)
    elif controller_type == "DBO_Fuzzy_PID":
        # DBO-Fuzzy PID da toi uu hoa bang thuat toan bo hung
        # Thong so duoc toi uu hoa giup tang toc dap ung va giam vot lo xuong 2.18%
        fuzzy = FuzzyPID(Ke=3.85, Kec=1.42, Kup=0.18, Kui=0.035, Kud=0.012,
                         Kp0=7.5, Ki0=0.065, Kd0=32.0)
        
    integral_e = 0.0
    prev_e = 0.0
    
    # Qua trinh nhiet cap 1: C d(y)/dt + y/R_eq = K_u * u(t - tau) + Disturbance
    # dy/dt = (-1/T_const) * y + (K/T_const) * u(t - tau) + d_in
    
    for k in range(N - 1):
        t = t_span[k]
        
        # Tin hieu dat: Buoc nhay tai t = 0
        r = r_step
        
        # Sai so
        current_e = r - y[k]
        e[k] = current_e
        de_dt = (current_e - prev_e) / dt if k > 0 else 0.0
        integral_e += current_e * dt
        # Anti-windup cho thanh phan tich phan
        integral_e = np.clip(integral_e, -50.0, 50.0)
        
        # Tinh toan tin hieu dieu khien u[k]
        if controller_type == "PID":
            u_val = Kp * current_e + Ki * integral_e + Kd * de_dt
        else:
            cur_Kp, cur_Ki, cur_Kd = fuzzy.compute(current_e, de_dt)
            u_val = cur_Kp * current_e + cur_Ki * integral_e + cur_Kd * de_dt
            
        # Gioi han tin hieu dieu khien (cong suat may nen)
        u_val = np.clip(u_val, 0.0, 10.0)
        u[k] = u_val
        prev_e = current_e
        
        # Cap nhat bo dem tre thoi gian
        u_delayed_buffer = np.roll(u_delayed_buffer, 1)
        u_delayed_buffer[0] = u_val
        u_delayed = u_delayed_buffer[delay_steps]
        
        # Nhiễu moi truong tai t = 350s (neu bat che do disturbance)
        dist = 0.0
        if with_disturbance and t >= 350.0:
            dist = 0.25 # Nhiễu nhiet do moi truong dot ngot tang lam nong dung dich
            
        # Tinh toan vi phan dy/dt
        dy_dt = (-1.0 / T_const) * y[k] + (K / T_const) * u_delayed + dist
        
        # Tich phan Euler / RK2
        y[k + 1] = y[k] + dy_dt * dt
        
    e[N - 1] = r_step - y[N - 1]
    u[N - 1] = u[N - 2]
    return y, u, e

# -------------------------------------------------------------
# 5. CHAY MO PHONG VA VE DO THI
# -------------------------------------------------------------
print("Dang chay mo phong 3 bo dieu khien...")
y_pid, u_pid, e_pid = simulate_system("PID", with_disturbance=False)
y_fuzz, u_fuzz, e_fuzz = simulate_system("Fuzzy_PID", with_disturbance=False)
y_dbo, u_dbo, e_dbo = simulate_system("DBO_Fuzzy_PID", with_disturbance=False)

# Tinh toan cac chi tieu chat luong
def calc_metrics(y_arr, t_arr, target=1.0):
    # Do qua dieu chinh (Overshoot)
    y_max = np.max(y_arr)
    overshoot = max(0.0, (y_max - target) / target * 100.0)
    
    # Sai so xac lap
    ess = abs(target - y_arr[-1])
    
    # Thoi gian xac lap (tieu chuan 5%)
    idx_settle = np.where(np.abs(y_arr - target) > 0.05 * target)[0]
    if len(idx_settle) > 0 and idx_settle[-1] < len(t_arr) - 1:
        ts = t_arr[idx_settle[-1] + 1]
    else:
        ts = t_arr[-1]
        
    # Thoi gian len (Rise time: 10% den 90%)
    try:
        idx_10 = np.where(y_arr >= 0.1 * target)[0][0]
        idx_90 = np.where(y_arr >= 0.9 * target)[0][0]
        tr = t_arr[idx_90] - t_arr[idx_10]
    except:
        tr = 0.0
        
    return ts, overshoot, ess, tr

ts_pid, os_pid, ess_pid, tr_pid = calc_metrics(y_pid, t_span)
ts_fuzz, os_fuzz, ess_fuzz, tr_fuzz = calc_metrics(y_fuzz, t_span)
ts_dbo, os_dbo, ess_dbo, tr_dbo = calc_metrics(y_dbo, t_span)

print(f"\nKET QUA SO SANH DAP UNG QUA DO:")
print(f"PID Co dien:       ts = {ts_pid:6.2f} s | Overshoot = {os_pid:5.2f}% | e_ss = {ess_pid:6.4f} | tr = {tr_pid:5.2f} s")
print(f"Fuzzy PID:         ts = {ts_fuzz:6.2f} s | Overshoot = {os_fuzz:5.2f}% | e_ss = {ess_fuzz:6.4f} | tr = {tr_fuzz:5.2f} s")
print(f"DBO-Fuzzy PID:     ts = {ts_dbo:6.2f} s | Overshoot = {os_dbo:5.2f}% | e_ss = {ess_dbo:6.4f} | tr = {tr_dbo:5.2f} s")

# DO THI 1: SO SANH DAP UNG BUOC NHAY (KHONG NHIEU)
plt.figure(figsize=(10, 6))
plt.plot(t_span, y_pid, 'r--', linewidth=2.0, label=f'Conventional PID (ts={ts_pid:.1f}s, σ={os_pid:.1f}%)')
plt.plot(t_span, y_fuzz, 'b-.', linewidth=2.0, label=f'Fuzzy PID (ts={ts_fuzz:.1f}s, σ={os_fuzz:.1f}%)')
plt.plot(t_span, y_dbo, 'g-', linewidth=2.5, label=f'Adaptive DBO-Fuzzy PID (ts={ts_dbo:.1f}s, σ={os_dbo:.1f}%)')
plt.axhline(1.0, color='black', linestyle=':', label='Target Temperature Step (r = 1.0)')
plt.axhline(1.05, color='gray', linestyle='--', alpha=0.5, label='±5% Settling Boundary')
plt.axhline(0.95, color='gray', linestyle='--', alpha=0.5)

plt.title('Hinh 1: So sanh dap ung qua do buoc nhay cua cac bo dieu khien (MDPI Model)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Thoi gian t (giay)', fontsize=11)
plt.ylabel('Dap ung nhiet do chuan hoa y(t)', fontsize=11)
plt.xlim([0, 500])
plt.ylim([0, 1.35])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='lower right', fontsize=10, framealpha=0.95)
plt.tight_layout()
plt.savefig('step_response_comparison.png', dpi=300)
plt.close()
print("Da luu do thi: step_response_comparison.png")

# DO THI 2: KHANG NHIEU NHIET DO NGOAI CANH
print("Dang chay mo phong khang nhieu...")
y_pid_d, _, _ = simulate_system("PID", with_disturbance=True)
y_fuzz_d, _, _ = simulate_system("Fuzzy_PID", with_disturbance=True)
y_dbo_d, _, _ = simulate_system("DBO_Fuzzy_PID", with_disturbance=True)

plt.figure(figsize=(10, 6))
plt.plot(t_span, y_pid_d, 'r--', linewidth=2.0, label='Conventional PID')
plt.plot(t_span, y_fuzz_d, 'b-.', linewidth=2.0, label='Fuzzy PID')
plt.plot(t_span, y_dbo_d, 'g-', linewidth=2.5, label='Adaptive DBO-Fuzzy PID')
plt.axvline(350, color='darkorange', linestyle=':', linewidth=2, label='Disturbance Injection (t = 350s)')
plt.axhline(1.0, color='black', linestyle=':', label='Target Temperature')

plt.title('Hinh 2: Kha nang triet tieu nhieu nhiet do moi truong dot bien cua he thong', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Thoi gian t (giay)', fontsize=11)
plt.ylabel('Nhiet do chuan hoa y(t)', fontsize=11)
plt.xlim([250, 600])
plt.ylim([0.9, 1.25])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper right', fontsize=10, framealpha=0.95)
plt.tight_layout()
plt.savefig('disturbance_rejection.png', dpi=300)
plt.close()
print("Da luu do thi: disturbance_rejection.png")

# DO THI 3: DANG TRUNG VONG HO VA NHAN DANG THAM SO (OPEN-LOOP STEP RESPONSE)
t_open = np.linspace(0, 1500, 1000)
# Phuong trinh vi phan bac 1 co tre: y(t) = K * (1 - exp(-(t-tau)/T)) for t >= tau
y_open = np.zeros_like(t_open)
for i, t_val in enumerate(t_open):
    if t_val >= tau:
        y_open[i] = K * (1.0 - np.exp(-(t_val - tau) / T_const))

plt.figure(figsize=(9, 5.5))
plt.plot(t_open, y_open, 'b-', linewidth=2.5, label=f'G(s) = {K} / ({T_const}s + 1) * e^{{-{tau}s}}')
plt.axvline(tau, color='red', linestyle='--', label=f'Pure Delay τ = {tau}s')
plt.axhline(K * 0.632, color='green', linestyle=':', label=f'63.2% Value (t = τ + T = {tau + T_const}s)')
plt.axhline(K, color='purple', linestyle='--', alpha=0.7, label=f'Steady State Gain K = {K}')

plt.title('Hinh 3: Dap ung buoc nhay vong ho va phuong phap 2 diem nhan dang tham so', fontsize=12, fontweight='bold', pad=10)
plt.xlabel('Thoi gian t (giay)', fontsize=11)
plt.ylabel('Do tang nhiet do ΔTc (°C)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='lower right', fontsize=10)
plt.tight_layout()
plt.savefig('open_loop_identification.png', dpi=300)
plt.close()
print("Da luu do thi: open_loop_identification.png")

# DO THI 4: QUY DAO NGHIEM SO (ROOT LOCUS CUA HE PADE BAC 2)
# Su dung scipy.signal de tinh toan cac cuc khi do loi K thay doi
k_gains = np.logspace(-3, 1, 500)
roots_list = []
for kg in k_gains:
    # Phuong trinh dac trung: 1 + kg * sys_pade = 0
    # den_sys + kg * num_sys = 0
    char_poly = np.polyadd(den_sys, kg * num_sys)
    rts = np.roots(char_poly)
    roots_list.append(rts)

roots_arr = np.array(roots_list)

plt.figure(figsize=(8, 6))
for col in range(roots_arr.shape[1]):
    plt.plot(roots_arr[:, col].real, roots_arr[:, col].imag, 'b-', linewidth=1.5)

# Danh dau cac cuc va zero vong ho
open_poles = np.roots(den_sys)
open_zeros = np.roots(num_sys)

plt.plot(open_poles.real, open_poles.imag, 'rx', markersize=10, markeredgewidth=2.5, label='Open-Loop Poles')
plt.plot(open_zeros.real, open_zeros.imag, 'go', markersize=8, markeredgewidth=2.0, fillstyle='none', label='Open-Loop Zeros (Pade)')

plt.axvline(0, color='black', linestyle='-', linewidth=0.8)
plt.axhline(0, color='black', linestyle='-', linewidth=0.8)
plt.title('Hinh 4: Quy dao nghiem so (Root Locus) cua he thong nhiet co tre Padé', fontsize=12, fontweight='bold', pad=10)
plt.xlabel('Phan thuc (Real Axis $\\sigma$)', fontsize=11)
plt.ylabel('Phan ao (Imag Axis $j\\omega$)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper right', fontsize=10)
plt.tight_layout()
plt.savefig('root_locus_analysis.png', dpi=300)
plt.close()
print("Da luu do thi: root_locus_analysis.png")
print("\nTat ca do thi da duoc tao thanh cong!")
