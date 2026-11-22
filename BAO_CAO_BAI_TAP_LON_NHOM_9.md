# CHƯƠNG 1: TỔNG QUAN HỆ THỐNG VÀ MÔ TẢ VẬT LÝ

## 1.1. Đặt vấn đề và tính cấp thiết của đề tài
Trong kỹ thuật canh tác nông nghiệp công nghệ cao hiện đại, kỹ thuật màng dinh dưỡng (Nutrient Film Technique - NFT) được ứng dụng rộng rãi nhờ hiệu quả sử dụng nước, dinh dưỡng và năng suất vượt trội. Tuy nhiên, tại các vùng khí hậu nhiệt đới hoặc mùa hè khắc nghiệt (nhiệt độ môi trường nhà màng thường xuyên vượt mức $38^\circ\text{C} - 45^\circ\text{C}$), nhiệt độ của dòng dung dịch dinh dưỡng tăng cao gây ra hiện tượng sốc nhiệt vùng rễ (root zone heat stress).

Hậu quả của nhiệt độ dung dịch vượt ngưỡng tối ưu ($22^\circ\text{C} \pm 1^\circ\text{C}$ đối với rau diếp, xà lách) bao gồm:
* Nồng độ oxy hòa tan (Dissolved Oxygen - DO) trong nước giảm mạnh.
* Rễ cây bị thâm đen, thối rễ do vi khuẩn kỵ khí phát triển.
* Cây bị cháy lá, chậm lớn, thậm chí chết hàng loạt, năng suất sụt giảm trên $60\%$.

Để giải quyết vấn đề trên, việc thiết kế một **"Hệ thống lọc và làm nguội nước dùng dinh dưỡng"** khép kín có khả năng tự động lọc cặn hữu cơ, diệt khuẩn và kiểm soát nhiệt độ dung dịch một cách chính xác, ổn định và tiết kiệm năng lượng là một bài toán cơ điện tử - nhiệt cơ học cấp thiết.

```
+-----------------------------------------------------------------------------------+
|                            QUY TRÌNH TUẦN HOÀN KÍN                                |
|                                                                                   |
|  [Giàn máng NFT] ---> [Bể thu hồi] ---> [Bơm & Lọc khử trùng] ---> [Bể trữ làm mát]|
|        ^                                                                  |       |
|        +------------------- Cấp dịch dinh dưỡng 22°C <--------------------+       |
+-----------------------------------------------------------------------------------+
```

## 1.2. Cấu tạo cơ hệ và các thành phần phần cứng
Hệ thống gồm các cụm cơ - điện - nhiệt chính được lắp đặt đồng bộ (tham chiếu mô hình thực nghiệm trong bài báo MDPI 2025):

1. **Bể chứa dung dịch dinh dưỡng (Storage Tank):**
   * Dung tích: $1.5\text{ m}^3$ ($1500\text{ lít}$), bọc lớp cách nhiệt Polyurethane bọt xốp bên ngoài nhằm hạn chế trao đổi nhiệt tự nhiên với môi trường.
   * Cụm cánh khuấy cưỡng bức (Agitator BLD10-1.5, đường kính cánh quạt $400\text{ mm}$, công suất $1.5\text{ kW}$) giúp xáo trộn dòng chảy, triệt tiêu sự phân tầng nhiệt độ, đảm bảo trường nhiệt độ đồng nhất trong bể.

2. **Cụm bơm tuần hoàn dung dịch (Circulation Pump):**
   * Model: Bơm ly tâm trục đứng đa tầng cánh 25CDL2-200.
   * Công suất động cơ: $2.2\text{ kW}$, cột áp định mức $H = 150\text{ m}$, lưu lượng $2\text{ m}^3/\text{h}$.
   * Nhiệm vụ: Đẩy dung dịch qua cụm lọc áp lực, qua thiết bị trao đổi nhiệt bay hơi và đưa lên hệ thống máng trồng.

3. **Cụm lọc và khử trùng (Mechanical & Disinfection Filter Unit):**
   * Gồm tầng lọc cơ học màng vi lọc (loại bỏ cặn lơ lửng, rễ cây đứt gãy, hạt phân chưa tan) và đèn cực tím UV diệt khuẩn.
   * Tạo ra một tổn thất áp suất $\Delta P_{filter}$ phụ thuộc vào lưu lượng dòng chảy và độ tích tụ bánh cặn.

4. **Hệ thống bơm nhiệt làm lạnh nguồn không khí (Air-Source Heat Pump Unit):**
   * Model: BLD-60AH, công suất tiêu thụ điện $49.8\text{ kW}$, sử dụng môi chất lạnh thân thiện môi trường R410A.
   * Hoạt động theo chu trình Carnot ngược chiều gồm 4 phần tử chính:
     * Máy nén trục vít/xoắn ốc biến tần (Inverter Compressor): Nén hơi môi chất áp suất thấp lên áp suất cao, nhiệt độ cao.
     * Giàn ngưng tụ làm mát bằng gió (Air-Cooled Condenser): Thải nhiệt ra không khí ngoài nhà kính.
     * Van tiết lưu điện tử (Electronic Expansion Valve - EEV): Giảm áp môi chất lỏng từ áp suất ngưng tụ xuống áp suất bay hơi.
     * Thiết bị trao đổi nhiệt bay hơi dạng ống lồng hoặc tấm hàn (Evaporator): Hấp thu nhiệt từ dung dịch dinh dưỡng để làm lạnh nước.
     * Van đảo chiều 4 ngả: Cho phép vận hành hai chiều (làm lạnh vào mùa hè và gia nhiệt ấm vào mùa đông).

5. **Hệ thống điều khiển nhúng và cảm biến (Control Hardware):**
   * Vi điều khiển trung tâm: STM32F103RCT6 (ARM Cortex-M3, tần số $72\text{ MHz}$).
   * Cảm biến nhiệt độ: PT100 bạch kim (dải đo $-50^\circ\text{C} \to +150^\circ\text{C}$, độ chính xác $\pm 0.1^\circ\text{C}$).
   * Module chuyển đổi ADC chuyên dụng: MAX6675.
   * Module truyền thông không dây 4G: Air724UG kết nối đám mây giám sát từ xa.
   * Khởi động từ (AC Contactor LC1N50) và rơ le nhiệt (LRN357N) đóng cắt các bơm, quạt và cánh khuấy.


# CHƯƠNG 2: THIẾT LẬP PHƯƠNG TRÌNH ĐỘNG HỌC VÀ ĐỘNG LỰC HỌC CƠ HỆ

Theo quy trình chuẩn 6 bước trong môn học *Động lực học và Điều khiển Hệ thống*, việc thiết lập mô hình toán học bắt đầu từ các định luật vật lý cơ bản: Định luật II Newton cho cơ hệ chuyển động, phương trình Navier-Stokes/Bernoulli cho dòng chất lỏng, và Định luật I Nhiệt động lực học cho quá trình trao đổi nhiệt.

```
+-----------------------------------------------------------------------------------------+
|                  SƠ ĐỒ CƠ HỆ ĐA MIỀN (MULTIDOMAIN DYNAMIC SYSTEM)                       |
|                                                                                         |
|  [ĐIỆN - CƠ]       [THỦY LỰC DÒNG CHẢY]       [NHIỆT ĐỘNG LỰC HỌC]                      |
|  Động cơ bơm  ---> Bơm ly tâm & Lọc màng ---> Bể trộn & Giàn lạnh  ---> Nhiệt độ rễ cây|
|  (Armature Eq)     (Fluid Momentum Eq)        (Thermal Energy Eq)       (Tc = 22°C)     |
+-----------------------------------------------------------------------------------------+
```

## 2.1. Động lực học phân hệ bơm tuần hoàn và dòng chảy qua bộ lọc áp lực

### a) Động học và Động lực học Cơ - Điện của Động cơ bơm
Động cơ điện dẫn động bơm tuần hoàn (quy đổi về động cơ điện một chiều hoặc động cơ không đồng bộ điều khiển vector):
* Phương trình mạch điện phần ứng:
$$V_a(t) = R_a i_a(t) + L_a \frac{di_a(t)}{dt} + e_b(t)$$
trong đó $e_b(t) = K_b \omega_p(t)$ là sức phản điện động, $\omega_p(t)$ là vận tốc góc của trục bơm.

* Phương trình động lực học quay của trục rotor bơm (Định luật II Newton cho chuyển động quay):
$$J_p \frac{d\omega_p(t)}{dt} + B_p \omega_p(t) = T_e(t) - T_L(t)$$
trong đó:
* $J_p$: Mô men quán tính tương đương của rotor và cánh bơm ($\text{kg}\cdot\text{m}^2$).
* $B_p$: Hệ số ma sát nhớt ổ bi ($\text{N}\cdot\text{m}\cdot\text{s}/\text{rad}$).
* $T_e(t) = K_t i_a(t)$: Mô men điện từ sinh ra bởi động cơ.
* $T_L(t)$: Mô men cản thủy động lực học do dung dịch lỏng tác dụng lên cánh bơm:
$$T_L(t) = k_{pump} \cdot Q(t) \cdot \omega_p(t)$$
với $Q(t)$ là lưu lượng dòng chảy dung dịch qua bơm ($\text{m}^3/\text{s}$).

### b) Động lực học dòng chảy trong đường ống và qua bộ lọc khử trùng
Áp dụng phương trình bảo toàn động lượng cho dòng chất lỏng không nén được trong đường ống kín chiều dài $L_{pipe}$, tiết diện $A_{pipe}$:
$$I_h \frac{dQ(t)}{dt} = \Delta P_{pump}(t) - \Delta P_{pipe}(t) - \Delta P_{filter}(t) - \rho g \Delta H$$
trong đó:
* $I_h = \frac{\rho L_{pipe}}{A_{pipe}}$: Quán tính thủy lực của cột chất lỏng ($\text{kg}/\text{m}^4$).
* Cột áp do bơm ly tâm tạo ra: $\Delta P_{pump}(t) = a_0 \omega_p^2(t) - a_1 \omega_p(t) Q(t)$.
* Tổn thất áp suất ma sát dọc đường ống (Darcy-Weisbach):
$$\Delta P_{pipe}(t) = R_{pipe} Q(t) = \left( \lambda \frac{L_{pipe}}{D_{pipe}} \frac{\rho}{2 A_{pipe}^2} Q_0 \right) Q(t)$$
* Tổn thất áp lực qua lớp màng lọc cặn và khử trùng (Định luật Darcy mở rộng và Carmen-Kozeny):
$$\Delta P_{filter}(t) = R_m \mu \frac{Q(t)}{A_{filter}} + r_c \mu \frac{m_c(t)}{A_{filter}^2} Q(t)$$
với $R_m$ là trở lực ban đầu của màng lọc, $r_c$ là trở lực riêng của lớp bánh cặn tích tụ, $m_c(t)$ là khối lượng cặn giữ lại theo thời gian, $\mu$ là độ nhớt động lực học của dung dịch.

Phương trình vi phân động lực học dòng chảy chất lỏng rút gọn:
$$I_h \frac{dQ(t)}{dt} + R_{hydraulic} Q(t) = a_0 \omega_p^2(t) - a_1 \omega_p(t) Q(t) - \rho g \Delta H$$

---

## 2.2. Động lực học phân hệ cơ học cánh khuấy trộn trong bể
Để tránh sự phân tầng nhiệt độ (nước lạnh chìm xuống đáy, nước ấm nổi lên bề mặt), cánh khuấy liên tục tạo dòng chảy cuộn xoáy cưỡng bức.

Phương trình chuyển động quay của trục cánh khuấy:
$$J_a \frac{d\omega_a(t)}{dt} + B_a \omega_a(t) = T_{motor\_a}(t) - T_{drag}(\omega_a)$$
trong đó mô men cản thủy động học của cánh khuấy bán kính $R_{imp}$, đường kính $D = 400\text{ mm}$ quay trong dung dịch có khối lượng riêng $\rho$:
$$T_{drag}(\omega_a) = \frac{1}{2} C_D \rho \omega_a^2 \int_0^{R_{imp}} r^3 dr = K_{drag} \omega_a^2(t)$$

Tuyến tính hóa quanh điểm làm việc vận tốc góc định mức $\omega_{a0}$:
$$T_{drag}(\omega_a) \approx T_{drag}(\omega_{a0}) + 2 K_{drag} \omega_{a0} \cdot \Delta\omega_a(t)$$
Hệ thống khuấy đảm bảo hệ số truyền nhiệt đối lưu cưỡng bức $h$ tại thành giàn bay hơi và thành bể đạt giá trị cực đại và đồng đều:
$$h = h_0 \cdot \left( 1 + \alpha_m \omega_a \right)^{0.8}$$

---

## 2.3. Động lực học nhiệt - Quá trình trao đổi nhiệt và làm nguội dung dịch
Đây là **phân hệ cốt lõi** quyết định chất lượng của toàn bộ hệ thống. Xét bể chứa dung dịch dinh dưỡng như một phần tử nhiệt đơn dung tích (Single-Capacity Thermal Process) với các giả thiết kỹ thuật:
1. Chiều dài đường ống ngắn và được bọc cách nhiệt, bỏ qua tổn thất nhiệt trên đường ống dẫn giữa máy lạnh và bể.
2. Nhờ cánh khuấy cưỡng bức, nhiệt độ dung dịch bên trong bể phân bố đồng đều tại mọi điểm, nhiệt độ dung dịch ra khỏi bể bằng nhiệt độ trung bình trong bể: $T_{out}(t) = T_c(t)$.

```
                     Nhiệt môi trường ngoài T0(t)
                                 |
                                 v  Truyền nhiệt qua thành bể: h*A*(Tc - T0)
+----------------------------------------------------------------------+
| BỂ CHỨA DUNG DỊCH DINH DƯỠNG (Dung tích V_tank, Nhiệt dung C)       |
|                                                                      |
| Dòng hồi lưu vào:           Dung dịch trộn đều:       Dòng cấp ra:   |
| Ti(t), lưu lượng V          Nhiệt độ dung dịch Tc(t)  Tc(t)          |
| Nhiệt lượng vào:            C*(dTc/dt)                Nhiệt ra:      |
| rho*c*V*Ti                                            rho*c*V*Tc     |
|                                                                      |
|           ^                                                          |
|           | Công suất làm lạnh Qi(t) từ giàn bay hơi Bơm nhiệt       |
+-----------+----------------------------------------------------------+
```

### Phương trình Cân bằng Năng lượng (Định luật I Nhiệt động lực học):
Tốc độ tích lũy nhiệt lượng trong bể = Dòng nhiệt cung cấp (làm lạnh) + Dòng nhiệt mang vào bởi dung dịch hồi lưu - Dòng nhiệt mang ra bởi dung dịch cấp đi - Nhiệt lượng trao đổi với không khí môi trường qua vách bể.

$$C \frac{dT_c(t)}{dt} = Q_i(t) + \rho c V T_i(t) - \rho c V T_c(t) - h A [T_c(t) - T_0(t)]$$

**Ý nghĩa vật lý và thứ nguyên của các đại lượng:**
* $T_c(t)$: Nhiệt độ của dung dịch dinh dưỡng trong bể tại thời điểm $t$ ($^\circ\text{C}$ hoặc $\text{K}$).
* $Q_i(t)$: Công suất nhiệt trao đổi của bơm nhiệt với dung dịch ($\text{W}$). Trong chế độ làm lạnh (cooling mode), nhiệt lượng bị lấy đi khỏi bể nên $Q_i(t) < 0$.
* $\rho$: Khối lượng riêng của dung dịch dinh dưỡng ($\approx 1000\text{ kg}/\text{m}^3$).
* $c$: Nhiệt dung riêng của dung dịch ($\approx 4186\text{ J}/(\text{kg}\cdot\text{K})$).
* $V$: Lưu lượng thể tích của dung dịch tuần hoàn qua bể ($\text{m}^3/\text{s}$).
* $T_i(t)$: Nhiệt độ của dòng dung dịch dinh dưỡng hồi lưu từ các máng NFT trở về bể ($^\circ\text{C}$).
* $T_0(t)$: Nhiệt độ không khí môi trường xung quanh nhà kính ($^\circ\text{C}$).
* $h$: Hệ số truyền nhiệt tổng hợp giữa thành bể và môi trường không khí ($\text{W}/(\text{m}^2\cdot\text{K})$).
* $A$: Diện tích bề mặt tiếp xúc truyền nhiệt của bể ($\text{m}^2$).
* $C$: Nhiệt dung tổng cộng của toàn bộ khối dung dịch trong bể:
$$C = m_{tank} \cdot c = \rho \cdot V_{tank} \cdot c \quad (\text{J}/\text{K})$$
heheh
### Tuyến tính hóa và Dạng số gia (Incremental Deviation Form):
Gọi điểm làm việc tĩnh danh định (Operating Point) là $(T_{c0}, Q_{i0}, T_{i0}, T_{00})$.
Tại trạng thái xác lập:
$$0 = Q_{i0} + \rho c V (T_{i0} - T_{c0}) - h A (T_{c0} - T_{00})$$

Định nghĩa các biến số gia độ lệch:
$$\Delta T_c(t) = T_c(t) - T_{c0}, \quad \Delta Q_i(t) = Q_i(t) - Q_{i0}$$
$$\Delta T_i(t) = T_i(t) - T_{i0}, \quad \Delta T_0(t) = T_0(t) - T_{00}$$

Trừ hai phương trình trên, ta thu được phương trình vi phân sai lệch tuyến tính:
$$C \frac{d\Delta T_c(t)}{dt} = \Delta Q_i(t) + \rho c V \Delta T_i(t) - \rho c V \Delta T_c(t) - h A [\Delta T_c(t) - \Delta T_0(t)]$$

Đặt:
* $K_0 = \rho c V$ : Hệ số lưu lượng nhiệt của dòng dung dịch ($\text{W}/\text{K}$).
* $R = \frac{1}{h A}$ : Nhiệt trở tương đương của vách bể chứa ($\text{K}/\text{W}$).

Viết lại phương trình động lực học:
$$C \frac{d\Delta T_c(t)}{dt} + K_0 \Delta T_c(t) + \frac{\Delta T_c(t)}{R} = \Delta Q_i(t) + K_0 \Delta T_i(t) + \frac{\Delta T_0(t)}{R}$$

Nhân cả hai vế với $R$:
$$R C \frac{d\Delta T_c(t)}{dt} + (R K_0 + 1) \Delta T_c(t) = R \Delta Q_i(t) + R K_0 \Delta T_i(t) + \Delta T_0(t)$$

Chia cả hai vế cho $(R K_0 + 1)$:
$$\frac{R C}{R K_0 + 1} \frac{d\Delta T_c(t)}{dt} + \Delta T_c(t) = \frac{R}{R K_0 + 1} \Delta Q_i(t) + \frac{R K_0}{R K_0 + 1} \Delta T_i(t) + \frac{1}{R K_0 + 1} \Delta T_0(t)$$

Đây chính là **phương trình vi phân động lực học cấp 1 cơ bản** mô tả động thái nhiệt của dung dịch dinh dưỡng trong bể!


## 2.4. Động lực học phân hệ máy lạnh bơm nhiệt nguồn khí
Công suất nhiệt làm lạnh $Q_i(t)$ do thiết bị bay hơi sinh ra phụ thuộc trực tiếp vào lưu lượng môi chất lạnh tuần hoàn $\dot{m}_r(t)$, vốn được điều khiển bởi tốc độ quay của máy nén trục xoắn $\omega_{comp}(t)$ (hoặc tần số biến tần $f_{inv}$):
$$\Delta Q_i(t) = K_{comp} \cdot \Delta f_{inv}(t - \tau_{chiller})$$
trong đó:
* $\tau_{chiller}$: Thời gian trễ hình thành chu trình sôi môi chất trong giàn bay hơi.
* Kết hợp với thời gian trễ vận chuyển của chất lỏng trong đường ống từ giàn lạnh về bể, tổng thời gian trễ thuần của hệ thống được ký hiệu là $\tau$.


# CHƯƠNG 3: XÂY DỰNG HÀM TRUYỀN VÀ MÔ HÌNH KHÔNG GIAN TRẠNG THÁI

## 3.1. Biến đổi Laplace và thiết lập hàm truyền đạt
Áp dụng phép biến đổi Laplace hai vế phương trình vi phân với điều kiện đầu triệt tiêu ($\Delta T_c(0) = 0$):

$$\left[ \frac{R C}{R K_0 + 1} s + 1 \right] \Delta T_c(s) = \frac{R}{R K_0 + 1} \Delta Q_i(s) + \frac{R K_0}{R K_0 + 1} \Delta T_i(s) + \frac{1}{R K_0 + 1} \Delta T_0(s)$$

Suy ra:
$$\Delta T_c(s) = \frac{\frac{R}{R K_0 + 1}}{\frac{R C}{R K_0 + 1} s + 1} \Delta Q_i(s) + \frac{\frac{R K_0}{R K_0 + 1}}{\frac{R C}{R K_0 + 1} s + 1} \Delta T_i(s) + \frac{\frac{1}{R K_0 + 1}}{\frac{R C}{R K_0 + 1} s + 1} \Delta T_0(s)$$

Đặt:
* **Hệ số khuếch đại tĩnh của hệ thống (Static Gain):**
$$K = \frac{R}{R K_0 + 1}$$
* **Hằng số thời gian quán tính nhiệt (Thermal Time Constant):**
$$T = \frac{R C}{R K_0 + 1}$$

Khi coi nhiệt độ môi trường $\Delta T_0(s)$ và nhiệt độ hồi lưu $\Delta T_i(s)$ là các tín hiệu nhiễu đầu vào ($Disturbances$), hàm truyền đạt giữa tác động điều khiển công suất lạnh $\Delta Q_i(s)$ và nhiệt độ dung dịch $\Delta T_c(s)$ có dạng khâu quán tính bậc 1:
$$G_0(s) = \frac{\Delta T_c(s)}{\Delta Q_i(s)} = \frac{K}{T s + 1}$$

Bổ sung khâu trễ thời gian thuần $\tau$ phát sinh do sự pha trộn chất lỏng và trễ truyền nhiệt đối lưu:
$$G_p(s) = \frac{\Delta T_c(s)}{\Delta Q_i(s)} = \frac{K}{T s + 1} e^{-\tau s}$$

---

## 3.2. Nhận dạng tham số thực nghiệm theo phương pháp hai điểm
Để xác định chính xác các tham số $K, T, \tau$ trong điều kiện thực tế, các tác giả trong nghiên cứu MDPI 2025 đã thực hiện thí nghiệm đáp ứng bước nhảy vòng hở (Open-Loop Step Response):
* Tắt bơm phía máng trồng, bọc cách nhiệt bể chứa, tác động tín hiệu bước nhảy công suất làm lạnh và ghi nhận nhiệt độ dung dịch cứ mỗi $60\text{ s}$.
* Dữ liệu nhiệt độ được khớp nối phi tuyến (đạt hệ số tương quan $R^2 = 0.991$).
* Áp dụng phương pháp hai điểm đặc trưng (Two-point Method) tại các mốc đáp ứng $28.3\%$ và $63.2\%$ giá trị xác lập:
  * $t_1$ ứng với $y(t_1) = 0.283 y_{ss} \implies t_1 = \tau + \frac{T}{3}$
  * $t_2$ ứng với $y(t_2) = 0.632 y_{ss} \implies t_2 = \tau + T$
* Kết quả nhận dạng chính xác thu được:
$$\begin{cases} K = 1.7 \\ T = 340\text{ s} \\ \tau = 10\text{ s} \end{cases}$$

Hàm truyền thực nghiệm của đối tượng điều khiển:
$$G_p(s) = \frac{1.7}{340 s + 1} e^{-10 s}$$


## 3.3. Xấp xỉ trễ Padé
Khâu trễ phi tuyến $e^{-\tau s} = e^{-10 s}$ không thể phân tích trực tiếp bằng đa thức đại số trong miền $s$. Do đó, ta sử dụng **xấp xỉ Padé bậc 1** (Padé Approximation, Ch.02 & Ch.08):
$$e^{-\tau s} \approx \frac{1 - \frac{\tau}{2} s}{1 + \frac{\tau}{2} s} = \frac{1 - 5 s}{1 + 5 s}$$

Hàm truyền tương đương của đối tượng:
$$G_{pade}(s) = \frac{1.7}{340 s + 1} \cdot \frac{1 - 5 s}{1 + 5 s} = \frac{-8.5 s + 1.7}{1700 s^2 + 345 s + 1}$$

**Nhận xét:** Hàm truyền tương đương có 2 cực nằm bên trái trục ảo ($s_1 = -1/340 \approx -0.00294$, $s_2 = -1/5 = -0.2$) và 1 điểm **Zero pha không cực tiểu** (Non-Minimum Phase Zero) nằm bên phải trục ảo tại $s_z = +1/5 = +0.2$. Zero này sinh ra hiện tượng đáp ứng ngược chiều ban đầu (undershoot) đặc trưng của các hệ thống nhiệt động có trễ.


## 3.4. Mô hình Không gian trạng thái toàn phần (State-Space Model)
Áp dụng kiến thức Chương 3 (*Modeling in Time Domain*), ta mô tả toàn bộ cơ hệ đa biến dưới dạng phương trình trạng thái ma trận:

Chọn vectơ biến trạng thái gồm 3 biến vật lý quan trọng:
$$\mathbf{x}(t) = \begin{bmatrix} x_1(t) \\ x_2(t) \\ x_3(t) \end{bmatrix} = \begin{bmatrix} \Delta T_c(t) & \text{(Nhiệt độ dung dịch dinh dưỡng)} \\ \Delta Q(t) & \text{(Lưu lượng dung dịch qua bộ lọc)} \\ \Delta \omega_a(t) & \text{(Vận tốc góc cánh khuấy trộn)} \end{bmatrix}$$

Vectơ tín hiệu điều khiển:
$$\mathbf{u}(t) = \begin{bmatrix} u_1(t) \\ u_2(t) \\ u_3(t) \end{bmatrix} = \begin{bmatrix} \Delta Q_i(t) & \text{(Công suất máy lạnh làm mát)} \\ \Delta V_p(t) & \text{(Điện áp cấp động cơ bơm tuần hoàn)} \\ \Delta V_a(t) & \text{(Điện áp cấp động cơ cánh khuấy)} \end{bmatrix}$$

Vectơ tín hiệu nhiễu môi trường:
$$\mathbf{d}(t) = \begin{bmatrix} \Delta T_0(t) & \text{(Nhiệt độ không khí mùa hè trong nhà màng)} \\ \Delta T_i(t) & \text{(Nhiệt độ dung dịch hồi lưu từ rễ cây)} \end{bmatrix}$$

Hệ phương trình trạng thái liên tục:
$$\dot{\mathbf{x}}(t) = \mathbf{A} \mathbf{x}(t) + \mathbf{B} \mathbf{u}(t) + \mathbf{E} \mathbf{d}(t)$$
$$\mathbf{y}(t) = \mathbf{C} \mathbf{x}(t) + \mathbf{D} \mathbf{u}(t)$$

Trong đó các ma trận hệ thống có dạng:
$$\mathbf{A} = \begin{bmatrix} -\frac{1}{T} & -\frac{c(T_{c0} - T_{i0})}{C} & 0 \\ 0 & -\frac{R_{hydraulic}}{I_h} & 0 \\ 0 & 0 & -\frac{B_a + 2 K_{drag} \omega_{a0}}{J_a} \end{bmatrix}$$

$$\mathbf{B} = \begin{bmatrix} \frac{K}{T} & 0 & 0 \\ 0 & \frac{K_{pump\_V}}{I_h} & 0 \\ 0 & 0 & \frac{K_m}{J_a} \end{bmatrix}, \quad \mathbf{E} = \begin{bmatrix} \frac{1}{R C} & \frac{K_0}{C} \\ 0 & 0 \\ 0 & 0 \end{bmatrix}$$

$$\mathbf{C} = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}, \quad \mathbf{D} = [0]$$

Kiểm tra định thức ma trận điều khiển được Kalman: $\mathcal{C} = [\mathbf{B} \quad \mathbf{A}\mathbf{B} \quad \mathbf{A}^2\mathbf{B}]$, $\text{rank}(\mathcal{C}) = 3$ (Hệ thống điều khiển được hoàn toàn).



# TÀI LIỆU THAM KHẢO

1. **Nguyễn Tấn Tiến**, *Slide bài giảng môn Động lực học và Điều khiển Hệ thống*, Khoa Cơ khí, Trường Đại học Bách Khoa - ĐHQG TP. Hồ Chí Minh, 2023.
2. **Norman S. Nise**, *Control Systems Engineering*, 7th Edition, John Wiley & Sons, 2015.
3. **Yuliang Cai, Zelan Zhao, Wenzhong Guo, Hailing Xu, Yunfei Teng, Xiaobei Han, Qian Zhao, and Lichun Wang**, *"Smart Nutrient Solution Temperature Control System for Oversummering Lettuce Cultivation Based on Adaptive Dung Beetle Optimizer-Fuzzy PID"*, *Applied Sciences* (MDPI), Vol. 15, Issue 10, Art. No. 5381, 2025. DOI: [10.3390/app15105381](https://doi.org/10.3390/app15105381).
4. **Katsuhiko Ogata**, *Modern Control Engineering*, 5th Edition, Prentice Hall, 2010.
5. **Jianhua Shen et al.**, *"Dung Beetle Optimizer: A novel nature-inspired meta-heuristic algorithm"*, *The Journal of Supercomputing*, 2023.
