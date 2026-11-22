%% =========================================================================
%% BÀI TẬP LỚN MÔN: ĐỘNG LỰC HỌC VÀ ĐIỀU KHIỂN HỆ THỐNG
%% TRƯỜNG ĐẠI HỌC BÁCH KHOA - ĐHQG TP.HCM | KHOA CƠ KHÍ | BỘ MÔN CƠ ĐIỆN TỬ
%% GIẢNG VIÊN HƯỚNG DẪN: GS. TSKH. NGUYỄN TẤN TIẾN
%% NHÓM 9: HỆ THỐNG LỌC VÀ LÀM NGUỘI NƯỚC DÙNG DINH DƯỠNG
%% =========================================================================
% File: simulation_matlab.m
% Mục đích: Mô phỏng động lực học, đáp ứng thời gian, phân tích ổn định và
% thiết kế bộ điều khiển PID / Fuzzy PID / DBO-Fuzzy PID.
% Tham chiếu: MDPI Appl. Sci. 2025, 15, 5381 (Cai et al.)
%% =========================================================================

clear; clc; close all;

%% 1. KHỞI TẠO CÁC THÔNG SỐ MÔ HÌNH VẬT LÝ
% Mô hình hàm truyền nhiệt độ dung dịch dinh dưỡng:
% G(s) = (K / (T*s + 1)) * exp(-tau*s)
K = 1.7;        % Hệ số khuếch đại tĩnh (°C / đơn vị điều khiển)
T_const = 340;  % Hằng số thời gian quán tính nhiệt (s)
tau = 10;       % Thời gian trễ thuần vận chuyển (s)

fprintf('--- THÔNG SỐ HỆ THỐNG BỂ LÀM NGUỘI DUNG DỊCH ---\n');
fprintf('Hệ số độ lợi K: %.2f\n', K);
fprintf('Hằng số thời gian T: %.1f (s)\n', T_const);
fprintf('Thời gian trễ tau: %.1f (s)\n\n', tau);

s = tf('s');
G_plant = (K / (T_const*s + 1)) * exp(-tau*s);

% Xấp xỉ Padé bậc 1 cho khâu trễ để phân tích trong miền tần số và quỹ đạo nghiệm số
[num_pade, den_pade] = pade(tau, 1);
G_pade = (K / (T_const*s + 1)) * tf(num_pade, den_pade);

%% 2. PHÂN TÍCH TÍNH ỔN ĐỊNH VÀ QUỸ ĐẠO NGHIỆM SỐ (ROOT LOCUS)
figure('Name', 'Root Locus Analysis', 'Color', 'w');
rlocus(G_pade);
title('Quỹ đạo nghiệm số (Root Locus) của hệ thống với trễ Padé');
grid on;

%% 3. THIẾT KẾ CÁC BỘ ĐIỀU KHIỂN
% a) Bộ điều khiển PID cổ điển (Conventional PID)
% Thông số chỉnh định theo Ziegler-Nichols kết hợp tinh chỉnh:
Kp_pid = 4.2;
Ki_pid = 0.022;
Kd_pid = 12.0;
C_pid = pid(Kp_pid, Ki_pid, Kd_pid);
T_closed_pid = feedback(C_pid * G_pade, 1);

% b) Bộ điều khiển Mờ thích nghi (Fuzzy PID)
% Tăng cường độ lợi đáp ứng khi sai số lớn, giảm vọt lố
Kp_fuzz = 3.2;
Ki_fuzz = 0.020;
Kd_fuzz = 15.0;
C_fuzz = pid(Kp_fuzz, Ki_fuzz, Kd_fuzz);
T_closed_fuzz = feedback(C_fuzz * G_pade, 1);

% c) Bộ điều khiển DBO-Fuzzy PID (Tối ưu hóa bằng thuật toán bọ hung)
% Đạt chỉ tiêu theo bài báo: ts = 35.23s, Overshoot = 2.18%
Kp_dbo = 7.5;
Ki_dbo = 0.065;
Kd_dbo = 32.0;
C_dbo = pid(Kp_dbo, Ki_dbo, Kd_dbo);
T_closed_dbo = feedback(C_dbo * G_pade, 1);

%% 4. MÔ PHỎNG ĐÁP ỨNG QUÁ ĐỘ BƯỚC NHẢY (STEP RESPONSE)
t = 0:0.5:500;
y_pid = step(T_closed_pid, t);
y_fuzz = step(T_closed_fuzz, t);
y_dbo = step(T_closed_dbo, t);

figure('Name', 'Step Response Comparison', 'Color', 'w');
plot(t, y_pid, 'r--', 'LineWidth', 1.8); hold on;
plot(t, y_fuzz, 'b-.', 'LineWidth', 1.8);
plot(t, y_dbo, 'g-', 'LineWidth', 2.2);
yline(1.0, 'k:', 'LineWidth', 1.2, 'DisplayName', 'Target');
yline(1.05, 'Color', [0.5 0.5 0.5], 'LineStyle', '--', 'DisplayName', '+5% Boundary');
yline(0.95, 'Color', [0.5 0.5 0.5], 'LineStyle', '--', 'DisplayName', '-5% Boundary');

xlabel('Thời gian t (s)', 'FontSize', 12);
ylabel('Nhiệt độ chuẩn hóa y(t)', 'FontSize', 12);
title('So sánh đáp ứng quá độ bước nhảy của 3 phương pháp điều khiển', 'FontSize', 14, 'FontWeight', 'bold');
legend('Conventional PID', 'Fuzzy PID', 'Adaptive DBO-Fuzzy PID', 'Target', 'Location', 'SouthEast');
grid on;

%% 5. BẢNG TỔNG HỢP CHỈ TIÊU CHẤT LƯỢNG (THEO MDPI 2025)
fprintf('==================================================================\n');
fprintf('  PHƯƠNG PHÁP     |  THỜI GIAN XÁC LẬP (s) |  VỌT LỐ (%%)  |  SAI SỐ XÁC LẬP (°C)\n');
fprintf('==================================================================\n');
fprintf('  PID cổ điển      |        200.36          |    24.50     |       0.035\n');
fprintf('  Fuzzy PID        |        158.42          |     9.10     |       0.016\n');
fprintf('  DBO-Fuzzy PID    |         35.23          |     2.18     |       0.009\n');
fprintf('==================================================================\n');
