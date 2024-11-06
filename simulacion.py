import matplotlib.pyplot as plt
import random


def transferencia_rl(entrada):
    # implementar algo como "sumar o restar X al estado del servidor según la entrada"
    return entrada


perturbaciones = {136: 2250, 151: 2250, 166: 2250}


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
        return -20 if error > 0 else 20


lecturas = []
estados_sv = []
tiempos = []
valor_nominal = 1000
if __name__ == "__main__":
    Kd = 0
    estado_del_servidor = 1000
    error_anterior = 0
    for i in range(10000):
        tiempos.append(i)
        variacion = random.randint(-50, +50)
        estado_del_servidor += variacion
        # agregar perturbaciones bruscas en ciertos puntos
        perturbacion = generate_perturbacion(i)

        valor_real = estado_del_servidor
        lecturas.append(valor_real)

        señal_error = valor_nominal - valor_real

        salida_proporcional = umbrales(señal_error) * -1
        salida_derivativo = Kd * (señal_error - error_anterior)
        error_anterior = señal_error
        salida_total_controlador = salida_proporcional + salida_derivativo
        estados_sv.append(estado_del_servidor)

        salida_rl = transferencia_rl(salida_total_controlador)

        estado_del_servidor += salida_rl
    # armar gráfico con lecturas


plt.figure(figsize=(15, 10))

# Gráfico de temperatura
plt.subplot(3, 1, 1)
plt.plot(tiempos, estados_sv, label='Requests por minuto')
plt.axhline(y=1300, color='y', linestyle='--', label='Umbral 3')
plt.axhline(y=1200, color='g', linestyle='--', label='Umbral 2')
plt.axhline(y=1100, color='b', linestyle='--', label='Umbral 1')
# plt.axhline(y=50, color='b', linestyle='--', label='')
plt.axhline(y=1000, color='r', linestyle='--', label='% CPU deseado')
# plt.axhline(y=70, color='b', linestyle='--', label='')
# plt.axhline(y=75, color='b', linestyle='--', label='')
# plt.axhline(y=80, color='g', linestyle='--', label='')
# plt.axhline(y=85, color='y', linestyle='--', label='')
plt.xlabel('Tiempo')
plt.ylabel('Requests')
plt.title('Simulación de control de Rate Limiter')
plt.legend()
plt.grid(True)

# plt.subplot(3, 1, 2)
# plt.plot(lecturas, label='cant CPU')
# plt.xlabel('Tiempo (seg)')
# plt.ylabel('cant CPU')
# plt.legend()
# plt.grid(True)

# plt.subplot(3, 1, 3)
# plt.plot(lecturas, label='cant requests')
# plt.xlabel('Tiempo (seg)')
# plt.ylabel('cant requests')
# plt.legend()
# plt.grid(True)

plt.tight_layout()
# plt.savefig('simulacion.png')
plt.show()
