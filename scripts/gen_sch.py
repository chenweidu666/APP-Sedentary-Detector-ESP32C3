import uuid

def gen_uuid():
    return str(uuid.uuid4())

uuids = {k: gen_uuid() for k in [
    "file", "esp_sym", "mpu_sym",
    "gnd1", "gnd2", "gnd3", "gnd4",
    "vcc3v3",
]}
for i in range(1, 19):
    uuids[f"esp_pin{i}"] = gen_uuid()
for i in range(1, 9):
    uuids[f"mpu_pin{i}"] = gen_uuid()
for i in range(1, 11):
    uuids[f"wire{i}"] = gen_uuid()
for i in range(1, 5):
    uuids[f"junc{i}"] = gen_uuid()
for name in ["label_gnd", "label_3v3", "label_5v", "label_sda", "label_scl", "label_int"]:
    uuids[name] = gen_uuid()
for i in range(1, 14):
    uuids[f"nc{i}"] = gen_uuid()
for name in ["esp_ref", "mpu_ref", "pwr_gnd1", "pwr_gnd2", "pwr_gnd3", "pwr_gnd4", "pwr_3v3"]:
    uuids[name] = gen_uuid()

# ============================================================
# lib_symbols
# ============================================================
esp_pins = []
for i in range(1, 10):
    y = 10.16 - (i-1) * 2.54
    esp_pins.append(f"""				(pin passive line (at -2.54 {y} 0) (length 2.54)
          (name "{i}" (effects (font (size 1.27 1.27))))
          (number "{i}" (effects (font (size 1.27 1.27))))
        )""")
for i in range(10, 19):
    y = 10.16 - (i-10) * 2.54
    esp_pins.append(f"""				(pin passive line (at 2.54 {y} 0) (length 2.54)
          (name "{i}" (effects (font (size 1.27 1.27))))
          (number "{i}" (effects (font (size 1.27 1.27))))
        )""")

esp_symbol = f"""(symbol "CarrierBoard:ESP32_C3_Mini_2x9" (pin_numbers hide) (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
			(property "Reference" "ESP" (at 0 -10.16 0)
        (effects (font (size 1.27 1.27)) (justify top))
      )
			(property "Value" "ESP32-C3_Mini_2x9" (at 0 -12.7 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Footprint" "CarrierBoard:ESP32_C3_Mini_2x9" (at 0 13.97 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(symbol "ESP32_C3_Mini_2x9_0_1"
        (rectangle (start -5.08 -12.7) (end 5.08 12.7)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
			(symbol "ESP32_C3_Mini_2x9_1_1"
{chr(10).join(esp_pins)}
      )
    )"""

mpu_pins = []
mpu_pin_names = {1: "VCC", 2: "GND", 3: "SCL", 4: "SDA", 5: "XDA", 6: "XCL", 7: "AD0", 8: "INT"}
for i in range(1, 9):
    y = 8.89 - (i-1) * 2.54
    mpu_pins.append(f"""				(pin passive line (at 0 {y} 0) (length 2.54)
          (name "{mpu_pin_names[i]}" (effects (font (size 1.27 1.27))))
          (number "{i}" (effects (font (size 1.27 1.27))))
        )""")

mpu_symbol = f"""(symbol "CarrierBoard:GY521_MPU6050_1x8" (pin_numbers hide) (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
			(property "Reference" "MPU" (at 0 -11.43 0)
        (effects (font (size 1.27 1.27)) (justify top))
      )
			(property "Value" "GY-521_MPU6050_1x8" (at 0 -13.97 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Footprint" "CarrierBoard:GY521_MPU6050_1x8" (at 0 12.7 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(property "Datasheet" "" (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
			(symbol "GY521_MPU6050_1x8_0_1"
        (rectangle (start -5.08 -11.43) (end 5.08 11.43)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
      )
			(symbol "GY521_MPU6050_1x8_1_1"
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

# ============================================================
# Pin coordinates
# ============================================================
esp_at_x, esp_at_y = 50, 80
mpu_at_x, mpu_at_y = 170, 80

def esp_pin_abs(pin_num):
    if pin_num <= 9:
        px = esp_at_x - 2.54
        py = esp_at_y + (10.16 - (pin_num-1) * 2.54)
    else:
        px = esp_at_x + 2.54
        py = esp_at_y + (10.16 - (pin_num-10) * 2.54)
    return (px, py)

def mpu_pin_abs(pin_num):
    px = mpu_at_x
    py = mpu_at_y + (8.89 - (pin_num-1) * 2.54)
    return (px, py)

# ============================================================
# Begin schematic
# ============================================================
content = f"""(kicad_sch (version 20250114) (generator eeschema)

  (uuid {uuids["file"]})

  (paper "A3")
  (title_block
    (title "Sedentary Detector - Carrier Board")
    (date "2026-06-20")
    (rev "0.2")
    (company "Personal Project")
  )

{lib_symbols}

  (no_connect (at {esp_pin_abs(3)[0]} {esp_pin_abs(3)[1]}) (uuid {uuids["nc1"]}))
  (no_connect (at {esp_pin_abs(4)[0]} {esp_pin_abs(4)[1]}) (uuid {uuids["nc2"]}))
  (no_connect (at {esp_pin_abs(6)[0]} {esp_pin_abs(6)[1]}) (uuid {uuids["nc3"]}))
  (no_connect (at {esp_pin_abs(12)[0]} {esp_pin_abs(12)[1]}) (uuid {uuids["nc4"]}))
  (no_connect (at {esp_pin_abs(13)[0]} {esp_pin_abs(13)[1]}) (uuid {uuids["nc5"]}))
  (no_connect (at {esp_pin_abs(14)[0]} {esp_pin_abs(14)[1]}) (uuid {uuids["nc6"]}))
  (no_connect (at {esp_pin_abs(15)[0]} {esp_pin_abs(15)[1]}) (uuid {uuids["nc7"]}))
  (no_connect (at {esp_pin_abs(16)[0]} {esp_pin_abs(16)[1]}) (uuid {uuids["nc8"]}))
  (no_connect (at {esp_pin_abs(17)[0]} {esp_pin_abs(17)[1]}) (uuid {uuids["nc9"]}))
  (no_connect (at {esp_pin_abs(18)[0]} {esp_pin_abs(18)[1]}) (uuid {uuids["nc10"]}))
  (no_connect (at {mpu_pin_abs(5)[0]} {mpu_pin_abs(5)[1]}) (uuid {uuids["nc11"]}))
  (no_connect (at {mpu_pin_abs(6)[0]} {mpu_pin_abs(6)[1]}) (uuid {uuids["nc12"]}))
  (no_connect (at {mpu_pin_abs(7)[0]} {mpu_pin_abs(7)[1]}) (uuid {uuids["nc13"]}))
"""

# 3V3: ESP pin2 → MPU pin1
p2 = esp_pin_abs(2)
p1m = mpu_pin_abs(1)
content += f"""  (wire (pts (xy {p2[0]} {p2[1]}) (xy 40 {p2[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire1"]}))
  (wire (pts (xy 40 {p2[1]}) (xy 40 {p1m[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire2"]}))
  (wire (pts (xy 40 {p1m[1]}) (xy {p1m[0]} {p1m[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire3"]}))
  (junction (at 40 {p2[1]}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc1"]}))
  (junction (at 40 {p1m[1]}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc2"]}))
"""

vcc_pin = 40, p2[1]
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
    (pin "1" (uuid {uuids["pwr_3v3"]}_pin))
  )"""

content += f"""  (label "3V3" (at 40 {p2[1]+2.54} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_3v3"]}))
"""

# I2C_SDA: ESP pin7 → MPU pin4
p7 = esp_pin_abs(7)
p4m = mpu_pin_abs(4)
content += f"""  (wire (pts (xy {p7[0]} {p7[1]}) (xy {p4m[0]} {p4m[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire4"]}))
  (label "I2C_SDA" (at 100 {p7[1]} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_sda"]}))
"""

# I2C_SCL: ESP pin8 → MPU pin3
p8 = esp_pin_abs(8)
p3m = mpu_pin_abs(3)
content += f"""  (wire (pts (xy {p8[0]} {p8[1]}) (xy {p3m[0]} {p3m[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire5"]}))
  (label "I2C_SCL" (at 100 {p8[1]} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_scl"]}))
"""

# MPU_INT: ESP pin5 → MPU pin8
p5 = esp_pin_abs(5)
p8m = mpu_pin_abs(8)
content += f"""  (wire (pts (xy {p5[0]} {p5[1]}) (xy {p8m[0]} {p8m[1]}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire6"]}))
  (label "MPU_INT" (at 100 {p5[1]-3.81} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_int"]}))
"""

# GND
gnd_y = 106
esp_p1 = esp_pin_abs(1)
esp_p9 = esp_pin_abs(9)
mpu_p2 = mpu_pin_abs(2)

content += f"""  (wire (pts (xy {esp_p1[0]} {esp_p1[1]}) (xy {esp_p1[0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire7"]}))
  (wire (pts (xy {esp_p9[0]} {esp_p9[1]}) (xy {esp_p9[0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire8"]}))
  (wire (pts (xy {mpu_p2[0]} {mpu_p2[1]}) (xy {mpu_p2[0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire9"]}))
  (wire (pts (xy {esp_p1[0]} {gnd_y}) (xy {mpu_p2[0]} {gnd_y}))
    (stroke (width 0) (type default))
    (uuid {uuids["wire10"]}))
  (junction (at {esp_p1[0]} {gnd_y}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc3"]}))
  (junction (at {mpu_p2[0]} {gnd_y}) (diameter 0) (color 0 0 0 0)
    (uuid {uuids["junc4"]}))
"""

for gx, guid in [(esp_p1[0], uuids["pwr_gnd1"]), (mpu_p2[0], uuids["pwr_gnd2"])]:
    gy = gnd_y
    content += f"""  (symbol (lib_id "power:GND") (at {gx} {gy} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {guid})
    (property "Reference" "#PWR" (at {gx} {gy+6.35} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "GND" (at {gx} {gy+3.81} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {gx} {gy} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {gx} {gy} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid {guid}_pin))
  )"""

content += f"""  (label "GND" (at {esp_p1[0]} {gnd_y-2.54} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_gnd"]}))
"""

# 5V_PM11 label at ESP pin11
p11 = esp_pin_abs(11)
content += f"""  (label "5V_PM11" (at {p11[0]+5.08} {p11[1]} 0) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid {uuids["label_5v"]}))
"""

# ESP32 Symbol instance
esp_pin_uuids = "\n".join([f'    (pin "{i}" (uuid {uuids[f"esp_pin{i}"]}))' for i in range(1, 19)])
content += f"""
  (symbol (lib_id "CarrierBoard:ESP32_C3_Mini_2x9") (at {esp_at_x} {esp_at_y} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {uuids["esp_sym"]})
    (property "Reference" "ESP" (at {esp_at_x} {esp_at_y-15.24} 0)
      (effects (font (size 1.27 1.27)) (justify top))
    )
    (property "Value" "ESP32-C3_Mini_2x9" (at {esp_at_x} {esp_at_y-17.78} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Footprint" "CarrierBoard:ESP32_C3_Mini_2x9" (at {esp_at_x} {esp_at_y+17.78} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {esp_at_x} {esp_at_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
{esp_pin_uuids}
  )"""

# MPU6050 Symbol instance
mpu_pin_uuids = "\n".join([f'    (pin "{i}" (uuid {uuids[f"mpu_pin{i}"]}))' for i in range(1, 9)])
content += f"""
  (symbol (lib_id "CarrierBoard:GY521_MPU6050_1x8") (at {mpu_at_x} {mpu_at_y} 0) (unit 1)
    (in_bom yes) (on_board yes) (fields_autoplaced)
    (uuid {uuids["mpu_sym"]})
    (property "Reference" "MPU" (at {mpu_at_x} {mpu_at_y-15.24} 0)
      (effects (font (size 1.27 1.27)) (justify top))
    )
    (property "Value" "GY-521_MPU6050_1x8" (at {mpu_at_x} {mpu_at_y-17.78} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Footprint" "CarrierBoard:GY521_MPU6050_1x8" (at {mpu_at_x} {mpu_at_y+15.24} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {mpu_at_x} {mpu_at_y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
{mpu_pin_uuids}
  )"""

# symbol_instances
content += f"""


  (sheet_instances
    (path "/" (page "1"))
  )
)"""

dst = "/home/chenwei/Workspace/05-Foundation/04-Embedded-Projects/Projects/02-APP-Sedentary-Detector-ESP32C3/hardware/kicad/SedentaryDetector.kicad_sch"
with open(dst, "w") as f:
    f.write(content)

print("OK: Schematic written successfully")
print(f"ESP32 placed at ({esp_at_x}, {esp_at_y})")
print(f"MPU6050 placed at ({mpu_at_x}, {mpu_at_y})")
