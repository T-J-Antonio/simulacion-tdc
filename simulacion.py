import matplotlib.pyplot as plt
import random


def transferencia_rl(entrada):
    # implementar algo como "sumar o restar X al estado del servidor según la entrada"
    return 42

lecturas = []
if __name__ == "__main__":
    valor_nominal = 1000
    Kp = 3
    Kd = 4
    estado_del_servidor = 1000
    error_anterior = 0
    for i in range(10000):
        perturbacion = random.randint(-50, +50)
        estado_del_servidor += perturbacion
        # agregar perturbaciones bruscas en ciertos puntos

        valor_real = estado_del_servidor
        lecturas.append(valor_real)

        señal_error = valor_nominal - valor_real

        # en realidad habría que aplicar umbrales
        salida_proporcional = Kp * señal_error
        salida_derivativo = Kd * (señal_error - error_anterior)
        error_anterior = señal_error
        salida_total_controlador = salida_proporcional + salida_derivativo

        salida_rl = transferencia_rl(salida_total_controlador)

        estado_del_servidor += salida_rl
    # armar gráfico con lecturas

plt.figure(figsize=(15, 10))

# Gráfico de temperatura
plt.subplot(3, 1, 1)
plt.plot(lecturas, label='% CPU en Volts')
plt.axhline(y=35, color='y', linestyle='--', label='Umbral 3')
plt.axhline(y=40, color='g', linestyle='--', label='Umbral 2')
plt.axhline(y=45, color='b', linestyle='--', label='Umbral 1')
plt.axhline(y=50, color='b', linestyle='--', label='')
plt.axhline(y=60, color='r', linestyle='--', label='% CPU deseado')
plt.axhline(y=70, color='b', linestyle='--', label='')
plt.axhline(y=75, color='b', linestyle='--', label='')
plt.axhline(y=80, color='g', linestyle='--', label='')
plt.axhline(y=85, color='y', linestyle='--', label='')
plt.xlabel('Tiempo (seg)')
plt.ylabel('% CPU (V)')
plt.title('Simulación de control de CPU')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(lecturas, label='cant CPU')
plt.xlabel('Tiempo (seg)')
plt.ylabel('cant CPU')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(lecturas, label='cant requests')
plt.xlabel('Tiempo (seg)')
plt.ylabel('cant requests')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('simulacion.png')
plt.show()