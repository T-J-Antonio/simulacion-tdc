import matplotlib
import random

def transferencia_rl(entrada):
    # implementar algo como "sumar o restar X al estado del servidor según la entrada"
    return 42

if __name__ == "__main__":
    valor_nominal = 1000
    Kp = 3
    Kd = 4
    estado_del_servidor = 1000
    error_anterior = 0
    lecturas = []
    for i in range(10000):
        perturbacion = random.randint(-50, +50)
        estado_del_servidor += perturbacion
        # agregar perturbaciones bruscas en ciertos puntos

        valor_real = estado_del_servidor
        lecturas.append(valor_real)

        señal_error = valor_nominal - valor_real

        salida_proporcional = Kp * señal_error # en realidad habría que aplicar umbrales
        salida_derivativo = Kd * (señal_error - error_anterior)
        error_anterior = señal_error
        salida_total_controlador = salida_proporcional + salida_derivativo
        
        salida_rl = transferencia_rl(salida_total_controlador)

        estado_del_servidor += salida_rl
    # armar gráfico con lecturas