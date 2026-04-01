# Import library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Deklarasi Variabel
# Suhu: rentang 0 - 40 °C
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
# Kelembapan: rentang 0 - 100 %
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
# Kecepatan: rentang 0 - 100
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

# Himpunan Fuzzy
# Himpunan untuk Suhu
suhu['Dingin'] = fuzz.trapmf(suhu.universe, [0, 0, 15, 25])
suhu['Sedang'] = fuzz.trimf(suhu.universe, [15, 25, 35])
suhu['Panas']  = fuzz.trapmf(suhu.universe, [25, 35, 40, 40])

# Himpunan untuk Kelembapan
kelembapan['Kering'] = fuzz.trapmf(kelembapan.universe, [0, 0, 30, 50])
kelembapan['Normal'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['Lembap'] = fuzz.trapmf(kelembapan.universe, [50, 70, 100, 100])

# Himpunan untuk Kecepatan Kipas
kecepatan['Lambat'] = fuzz.trapmf(kecepatan.universe, [0, 0, 20, 50])
kecepatan['Sedang'] = fuzz.trimf(kecepatan.universe, [30, 50, 70])
kecepatan['Cepat']  = fuzz.trapmf(kecepatan.universe, [50, 80, 100, 100])

# Aturan Fuzzy (IF-THEN)
# IF Suhu Dingin THEN Kecepatan Lambat
rule1 = ctrl.Rule(suhu['Dingin'], kecepatan['Lambat'])
# IF Suhu Sedang AND Kelembapan Kering THEN Kecepatan Sedang
rule2 = ctrl.Rule(suhu['Sedang'] & kelembapan['Kering'], kecepatan['Sedang'])
# IF Suhu Sedang AND Kelembapan Lembap THEN Kecepatan Cepat
rule3 = ctrl.Rule(suhu['Sedang'] & kelembapan['Lembap'], kecepatan['Cepat'])
# IF Suhu Panas THEN Kecepatan Cepat
rule4 = ctrl.Rule(suhu['Panas'], kecepatan['Cepat'])

# Membuat kontrol sistem dan simulasi perhitungan
kecepatan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
sistem_kipas = ctrl.ControlSystemSimulation(kecepatan_ctrl)

# Output
print("--- Simulasi Kecepatan Kipas Angin ---")
# Input nilai suhu dan kelembapan
input_suhu = float(input("Input Suhu: "))
input_kelembapan = float(input("Input Kelembapan: "))

# Input masuk ke sistem
sistem_kipas.input['suhu'] = input_suhu
sistem_kipas.input['kelembapan'] = input_kelembapan

# Komputasi sistem
sistem_kipas.compute()

# Hasil
print(f"Output Kecepatan : {sistem_kipas.output['kecepatan']:.2f}")
kecepatan.view(sim=sistem_kipas)
