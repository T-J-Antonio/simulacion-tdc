import matplotlib.pyplot as plt
import random


perturbaciones = {1750: -800, 3150: 1250, 4500: 1000}


def generate_perturbacion(t):
    return perturbaciones[t] if t in perturbaciones else 0


def umbrales(error):
    abs_error = abs(error)
    if abs_error < 10:
        return 0
    elif 10 <= abs_error < 20:
        return -5 if error > 0 else 5
    elif 20 <= abs_error < 30:
        return -10 if error > 0 else 10
    elif 30 <= abs_error < 40:
        return -15 if error > 0 else 15
    else:
        return -50 if error > 0 else 50


estados_sv = []
porcentajes_estado_sv = []
tiempos = []

# Entrada
valor_nominal = 1500

Kd = 0.4
if __name__ == "__main__":
    estado_del_servidor = 0
    error_anterior = 0
    for i in range(10000):
        tiempos.append(i)
        # Medidor de tráfico
        variacion = random.randint(-50, +50)
        estado_del_servidor += variacion

        # Señal f
        valor_real = estado_del_servidor

        # Señal e = f + entrada
        señal_error = valor_nominal - valor_real

        # Kp
        salida_proporcional = umbrales(señal_error) * -1

        # Kd
        salida_derivativo = Kd * (señal_error - error_anterior)
        error_anterior = señal_error

        # Controlador total = Kp + Kd        
        salida_total_controlador = salida_proporcional + salida_derivativo
        estados_sv.append(estado_del_servidor)
        porcentajes_estado_sv.append(
            round(estado_del_servidor/valor_nominal*100, 2))
        salida_rl = salida_total_controlador

        # Perturbación
        perturbacion = generate_perturbacion(i)

        # Salida
        estado_del_servidor += salida_rl + perturbacion


plt.figure(figsize=(15, 10))

plt.subplot(2, 1, 1)
plt.plot(tiempos, estados_sv, label='Requests por minuto')
plt.axhline(y=1540, color='y', linestyle='--', label='Umbral 3')
plt.axhline(y=1530, color='g', linestyle='--', label='Umbral 2')
plt.axhline(y=1520, color='b', linestyle='--', label='Umbral 1')
plt.axhline(y=1460, color='y', linestyle='--')
plt.axhline(y=1470, color='g', linestyle='--')
plt.axhline(y=1480, color='b', linestyle='--')
plt.axhline(y=1500, color='r', linestyle='--', label='Valor nominal')
plt.xlabel('Tiempo (min)')
plt.ylabel('Requests/min')
plt.title('Simulación de control de Rate Limiter')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(tiempos, porcentajes_estado_sv,
         label='Porcentaje sobre valor nominal')
plt.axhline(y=130, color='y', linestyle='--', label='Umbral 3')
plt.axhline(y=120, color='g', linestyle='--', label='Umbral 2')
plt.axhline(y=110, color='b', linestyle='--', label='Umbral 1')
plt.axhline(y=70, color='y', linestyle='--')
plt.axhline(y=80, color='g', linestyle='--')
plt.axhline(y=90, color='b', linestyle='--')
plt.axhline(y=100, color='r', linestyle='--', label='Valor nominal')
plt.xlabel('Tiempo (min)')
plt.ylabel('Porcentaje de requests')
plt.legend()
plt.grid(True)


plt.tight_layout()
# plt.savefig('simulacion.png')
plt.show()
