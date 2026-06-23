"""从 HARDWARE.md 网络表生成载板原理图骨架（ESP32-WROOM-32 2×15 + GY-87 1×8）。"""

import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# 默认写入 .gen 文件，避免覆盖 KiCad GUI 中手工维护的原理图
DST = ROOT / "hardware/kicad/SedentaryDetector.gen.kicad_sch"

ESP_NUM_PINS = 30

# DevKitC 排针编号 → 功能名（见 hardware/HARDWARE.md）
ESP_PIN_NAMES = {
    1: "3V3",
    2: "EN",
    3: "GPIO36",
    4: "GPIO39",
    5: "GPIO34",
    6: "GPIO35",
    7: "GPIO32",
    8: "GPIO33",
    9: "GPIO25",
    10: "GPIO26",
    11: "GPIO27",
    12: "GPIO14",
    13: "GPIO12",
    14: "GND",
    15: "VIN",
    16: "GPIO23",
    17: "GPIO22",
    18: "GPIO21",
    19: "GND",
    20: "GPIO19",
    21: "GPIO18",
    22: "GPIO5/SCL",
    23: "GPIO17",
    24: "GPIO16",
    25: "GPIO4/SDA",
    26: "GPIO2/INT",
    27: "GPIO15",
    28: "GND",
    29: "3V3",
    30: "30",
}

# 载板已用网络对应的 ESP 排针编号
PIN_3V3 = 1
PIN_GND_LEFT = 14
PIN_VIN = 15
PIN_GND_MID = 19
PIN_SCL = 22
PIN_SDA = 25
PIN_INT = 26
PIN_GND_RIGHT = 28

USED_ESP_PINS = {
    PIN_3V3,
    PIN_GND_LEFT,
    PIN_VIN,
    PIN_GND_MID,
    PIN_SCL,
    PIN_SDA,
    PIN_INT,
    PIN_GND_RIGHT,
}


def gen_uuid():
    return str(uuid.uuid4())


uuids = {k: gen_uuid() for k in [
    "file", "esp_sym", "mpu_sym",
    "pwr_gnd1", "pwr_gnd2", "pwr_3v3",
    "pwr_gnd1_pin", "pwr_gnd2_pin", "pwr_3v3_pin",
]}
for i in range(1, ESP_NUM_PINS + 1):
    uuids[f"esp_pin{i}"] = gen_uuid()
for i in range(1, 9):
    uuids[f"mpu_pin{i}"] = gen_uuid()
for i in range(1, 12):
    uuids[f"wire{i}"] = gen_uuid()
for i in range(1, 5):
    uuids[f"junc{i}"] = gen_uuid()
for name in ["label_gnd", "label_3v3", "label_5v", "label_sda", "label_scl", "label_int"]:
    uuids[name] = gen_uuid()
nc_idx = 0
for pin in range(1, ESP_NUM_PINS + 1):
    if pin not in USED_ESP_PINS:
        nc_idx += 1
        uuids[f"nc{nc_idx}"] = gen_uuid()
for pin in (1, 3, 7):
    uuids[f"nc_mpu{pin}"] = gen_uuid()


def conn_02x15_pin_lines(side: str, start_num: int, count: int) -> list[str]:
    lines = []
    x = -7.62 if side == "left" else 7.62
    for i in range(count):
        num = start_num + i
        y = 20.32 - i * 2.54
        name = ESP_PIN_NAMES.get(num, str(num))
        lines.append(
            f"""				(pin passive line (at {x} {y} 0) (length 2.54)
          (name "{name}" (effects (font (size 1.27 1.27))))
          (number "{num}" (effects (font (size 1.27 1.27))))
        )"""
        )
    return lines


esp_symbol_pins = conn_02x15_pin_lines("left", 1, 15) + conn_02x15_pin_lines("right", 16, 15)

esp_symbol = f"""(symbol "Conn_02x15" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
			(property "Reference" "J1" (at 0 20.32 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
			(property "Value" "ESP32_2x15" (at 0 22.86 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
			(property "Footprint" "" (at 0 -20.32 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(symbol "Conn_02x15_0_1"
        (rectangle (start -7.62 20.32) (end 7.62 -20.32)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
			(symbol "Conn_02x15_1_1"
{chr(10).join(esp_symbol_pins)}
      )
    )"""

mpu_pins = []
mpu_pin_names = {
    1: "DRDY",
    2: "INTA",
    3: "FSYNC",
    4: "SDA",
    5: "SCL",
    6: "GND",
    7: "3.3V",
    8: "VCC_IN",
}
for i in range(1, 9):
    y = 8.89 - (i - 1) * 2.54
    mpu_pins.append(
        f"""				(pin passive line (at 0 {y} 0) (length 2.54)
          (name "{mpu_pin_names[i]}" (effects (font (size 1.27 1.27))))
          (number "{i}" (effects (font (size 1.27 1.27))))
        )"""
    )

mpu_symbol = f"""(symbol "CarrierBoard:GY87_1x8" (pin_numbers hide) (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
			(property "Reference" "J2" (at 0 -11.43 0)
        (effects (font (size 1.27 1.27)) (justify top))
      )
			(property "Value" "GY-87_1x8" (at 0 -13.97 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Footprint" "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (at 0 12.7 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(symbol "GY87_1x8_0_1"
        (rectangle (start -5.08 -11.43) (end 5.08 11.43)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
			(symbol "GY87_1x8_1_1"
{chr(10).join(mpu_pins)}
      )
    )"""

lib_symbols = f"""  (lib_symbols
{esp_symbol}
{mpu_symbol}
		(symbol "power:GND" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
			(property "Reference" "#PWR" (at 0 -6.35 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Value" "GND" (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)))
      )
			(property "Footprint" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(symbol "GND_0_1"
        (polyline
          (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) hide
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )
		(symbol "power:VCC" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Value" "+3V3" (at 0 3.81 0)
        (effects (font (size 1.27 1.27)))
      )
			(property "Footprint" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(symbol "+3V3_0_1"
        (polyline
          (pts (xy -1.27 1.27) (xy 0 2.54) (xy 1.27 1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0 0) (xy 0 2.54))
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
			(symbol "+3V3_1_1"
				(pin power_in line (at 0 0 90) (length 0) hide
          (name "+3V3" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )
  )"""

esp_at_x, esp_at_y = 50, 100
mpu_at_x, mpu_at_y = 170, 80


def esp_pin_abs(pin_num: int) -> tuple[float, float]:
    if pin_num <= 15:
        px = esp_at_x - 7.62
        py = esp_at_y + (20.32 - (pin_num - 1) * 2.54)
    else:
        px = esp_at_x + 7.62
        py = esp_at_y + (20.32 - (pin_num - 16) * 2.54)
    return (px, py)


def mpu_pin_abs(pin_num: int) -> tuple[float, float]:
    px = mpu_at_x
    py = mpu_at_y + (8.89 - (pin_num - 1) * 2.54)
    return (px, py)


content = f"""(kicad_sch (version 20250114) (generator eeschema)

  (uuid {uuids["file"]})

  (paper "A3")
  (title_block
    (title "Sedentary Detector - Carrier Board")
    (date "2026-06-22")
    (rev "0.3")
    (company "Personal Project")
    (comment 1 "ESP32-WROOM-32 DevKitC 2x15 + GY-87")
  )

{lib_symbols}
"""

nc_idx = 0
for pin in range(1, ESP_NUM_PINS + 1):
    if pin not in USED_ESP_PINS:
        nc_idx += 1
        px, py = esp_pin_abs(pin)
        content += f"""  (no_connect (at {px} {py}) (uuid {uuids[f"nc{nc_idx}"]}))
"""
for pin in (1, 3, 7):
    px, py = mpu_pin_abs(pin)
    content += f"""  (no_connect (at {px} {py}) (uuid {uuids[f"nc_mpu{pin}"]}))
"""

# 3V3: ESP pin1 → GY-87 pin8 (VCC_IN)
p3v3 = esp_pin_abs(PIN_3V3)
p_mpu_vcc = mpu_pin_abs(8)
content += f"""  (wire (pts (xy {p3v3[0]} {p3v3[1]}) (xy 40 {p3v3[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire1"]}))
  (wire (pts (xy 40 {p3v3[1]}) (xy 40 {p_mpu_vcc[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire2"]}))
  (wire (pts (xy 40 {p_mpu_vcc[1]}) (xy {p_mpu_vcc[0]} {p_mpu_vcc[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire3"]}))
  (junction (at 40 {p3v3[1]}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc1"]}))
  (junction (at 40 {p_mpu_vcc[1]}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc2"]}))
"""

vcc_pin = 40, p3v3[1]
content += f"""  (symbol (lib_id "power:VCC") (at {vcc_pin[0]} {vcc_pin[1]-3.81} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {uuids["pwr_3v3"]})
    (property "Reference" "#PWR" (at {vcc_pin[0]} {vcc_pin[1]-10.16} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "+3V3" (at {vcc_pin[0]} {vcc_pin[1]-1.27} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {vcc_pin[0]} {vcc_pin[1]-3.81} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {vcc_pin[0]} {vcc_pin[1]-3.81} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {uuids["pwr_3v3_pin"]}))
  )"""

content += f"""  (label "3V3" (at 40 {p3v3[1]+2.54} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_3v3"]}))
"""

# I2C_SDA: ESP pin25 → GY-87 pin4
p_sda = esp_pin_abs(PIN_SDA)
p_mpu_sda = mpu_pin_abs(4)
content += f"""  (wire (pts (xy {p_sda[0]} {p_sda[1]}) (xy {p_mpu_sda[0]} {p_mpu_sda[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire4"]}))
  (label "I2C_SDA" (at 100 {p_sda[1]} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_sda"]}))
"""

# I2C_SCL: ESP pin22 → GY-87 pin5
p_scl = esp_pin_abs(PIN_SCL)
p_mpu_scl = mpu_pin_abs(5)
content += f"""  (wire (pts (xy {p_scl[0]} {p_scl[1]}) (xy {p_mpu_scl[0]} {p_mpu_scl[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire5"]}))
  (label "I2C_SCL" (at 100 {p_scl[1]} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_scl"]}))
"""

# MPU_INT: ESP pin26 → GY-87 pin2 INTA
p_int = esp_pin_abs(PIN_INT)
p_mpu_int = mpu_pin_abs(2)
content += f"""  (wire (pts (xy {p_int[0]} {p_int[1]}) (xy {p_mpu_int[0]} {p_mpu_int[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire6"]}))
  (label "MPU_INT" (at 100 {p_int[1]-3.81} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_int"]}))
"""

# GND bus: ESP 14/19/28 + MPU GND
gnd_y = 130
gnd_pins = [esp_pin_abs(PIN_GND_LEFT), esp_pin_abs(PIN_GND_MID), esp_pin_abs(PIN_GND_RIGHT)]
mpu_gnd = mpu_pin_abs(6)

content += f"""  (wire (pts (xy {gnd_pins[0][0]} {gnd_pins[0][1]}) (xy {gnd_pins[0][0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire7"]}))
  (wire (pts (xy {gnd_pins[1][0]} {gnd_pins[1][1]}) (xy {gnd_pins[1][0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire8"]}))
  (wire (pts (xy {gnd_pins[2][0]} {gnd_pins[2][1]}) (xy {gnd_pins[2][0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire9"]}))
  (wire (pts (xy {mpu_gnd[0]} {mpu_gnd[1]}) (xy {mpu_gnd[0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire10"]}))
  (wire (pts (xy {gnd_pins[0][0]} {gnd_y}) (xy {gnd_pins[2][0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire11"]}))
  (junction (at {gnd_pins[0][0]} {gnd_y}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc3"]}))
  (junction (at {mpu_gnd[0]} {gnd_y}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc4"]}))
"""

for gx, guid, guid_pin in [
    (gnd_pins[0][0], uuids["pwr_gnd1"], uuids["pwr_gnd1_pin"]),
    (mpu_gnd[0], uuids["pwr_gnd2"], uuids["pwr_gnd2_pin"]),
]:
    content += f"""  (symbol (lib_id "power:GND") (at {gx} {gnd_y} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {guid})
    (property "Reference" "#PWR" (at {gx} {gnd_y+6.35} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at {gx} {gnd_y+3.81} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {gx} {gnd_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {gx} {gnd_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {guid_pin}))
  )"""

content += f"""  (label "GND" (at {gnd_pins[0][0]} {gnd_y-2.54} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_gnd"]}))
"""

# 5V_PM11 at VIN (pin15)
p_vin = esp_pin_abs(PIN_VIN)
content += f"""  (label "5V_PM11" (at {p_vin[0]+5.08} {p_vin[1]} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_5v"]}))
"""

esp_pin_uuids = "\n".join(
    [f'    (pin "{i}" (uuid {uuids[f"esp_pin{i}"]}))' for i in range(1, ESP_NUM_PINS + 1)]
)
content += f"""
  (symbol (lib_id "Conn_02x15") (at {esp_at_x} {esp_at_y} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {uuids["esp_sym"]})
    (property "Reference" "J1" (at {esp_at_x} {esp_at_y+20.32} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Value" "ESP32_2x15" (at {esp_at_x} {esp_at_y+22.86} 0)
      (effects (font (size 1.27 1.27)) (justify left))
    )
    (property "Footprint" "Connector_PinSocket_2.54mm:PinSocket_2x15_P2.54mm_Vertical" (at {esp_at_x} {esp_at_y-20.32} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {esp_at_x} {esp_at_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
{esp_pin_uuids}
  )"""

mpu_pin_uuids = "\n".join([f'    (pin "{i}" (uuid {uuids[f"mpu_pin{i}"]}))' for i in range(1, 9)])
content += f"""
  (symbol (lib_id "CarrierBoard:GY87_1x8") (at {mpu_at_x} {mpu_at_y} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {uuids["mpu_sym"]})
    (property "Reference" "J2" (at {mpu_at_x} {mpu_at_y-15.24} 0)
      (effects (font (size 1.27 1.27)) (justify top))
    )
    (property "Value" "GY-87_1x8" (at {mpu_at_x} {mpu_at_y-17.78} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Footprint" "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (at {mpu_at_x} {mpu_at_y+15.24} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {mpu_at_x} {mpu_at_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
{mpu_pin_uuids}
  )"""

content += """

  (sheet_instances
    (path "/" (page "1"))
  )
)"""

DST.write_text(content)
print("OK: Schematic written successfully")
print(f"Output: {DST}")
print(f"ESP32-WROOM-32 J1 at ({esp_at_x}, {esp_at_y})")
print(f"GY-87 J2 at ({mpu_at_x}, {mpu_at_y})")
