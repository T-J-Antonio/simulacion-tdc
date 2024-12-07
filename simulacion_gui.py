import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import random


def run_simulation(initial_nominal, nominal_changes, perturbaciones):
    def generate_perturbacion(t):
        return perturbaciones[t] if t in perturbaciones else 0

    def umbrales(error):
        abs_error = abs(error)
        correction = 0
        if abs_error < 10:
            correction = 0
        elif 10 <= abs_error < 20:
            correction = 5
        elif 20 <= abs_error < 30:
            correction = 10
        elif 30 <= abs_error < 40:
            correction = 15
        else:
            correction = 50
        return -correction if error > 0 else correction

    estados_sv = []
    porcentajes_estado_sv = []
    tiempos = []
    perturbaciones_list = []
    valores_e = []
    valores_nominales = []

    estado_del_servidor = 0
    error_anterior = 0
    Kd = 0.4
    valor_nominal = initial_nominal
    for i in range(1000):
        if i in nominal_changes:
            valor_nominal = nominal_changes[i]

        valores_nominales.append(valor_nominal)
        tiempos.append(i)
        variacion = random.randint(-50, +50)
        estado_del_servidor += variacion

        valor_real = estado_del_servidor

        señal_error = valor_nominal - valor_real
        valores_e.append(señal_error)

        salida_proporcional = umbrales(señal_error) * -1
        salida_derivativo = Kd * (señal_error - error_anterior)
        error_anterior = señal_error

        salida_total_controlador = salida_proporcional + salida_derivativo
        estados_sv.append(estado_del_servidor)
        porcentajes_estado_sv.append(
            round(estado_del_servidor / valor_nominal * 100, 2))
        salida_rl = salida_total_controlador

        perturbacion = generate_perturbacion(i)
        perturbaciones_list.append(perturbacion)

        estado_del_servidor += salida_rl + perturbacion

    valores_nominales[0] = 0  # so that the graph starts at 0
    plt.figure(figsize=(20, 12))

    plt.subplot(3, 2, 1)
    plt.plot(tiempos, estados_sv, label='Requests por minuto')
    plt.axhline(y=initial_nominal, color='r', linestyle='--',
                label='Valor nominal inicial')
    for time, new_value in nominal_changes.items():
        plt.axvline(x=time, color='g', linestyle='--',
                    label=f'Cambio en t={time}')
        plt.axhline(y=new_value, color='b', linestyle='--',
                    label=f'Nuevo valor_nominal={new_value}')
    plt.xlabel('Tiempo [min]')
    plt.ylabel('f [Req]')
    plt.legend()
    plt.grid(True)

    # This graph does not include t = 0, VN[0] = 0, as it makes it kinda ugly
    plt.subplot(3, 2, 2)
    plt.plot(tiempos, porcentajes_estado_sv,
             label='Porcentaje sobre valor nominal')
    plt.plot(
        tiempos[1:],
        list(map(lambda vn: (vn + 20) * 100 / vn, valores_nominales[1:])),
        color='b',
        linestyle='--',
        label='Umbral 1'
    )
    plt.plot(
        tiempos[1:],
        list(map(lambda vn: (vn + 40) * 100 / vn, valores_nominales[1:])),
        color='g',
        linestyle='--',
        label='Umbral 2'
    )
    plt.plot(
        tiempos[1:],
        list(map(lambda vn: (vn + 60) * 100 / vn, valores_nominales[1:])),
        color='y',
        linestyle='--',
        label='Umbral 3'
    )
    plt.plot(
        tiempos[1:],
        list(map(lambda vn: (vn - 20) * 100 / vn, valores_nominales[1:])),
        color='b',
        linestyle='--'
    )
    plt.plot(
        tiempos[1:],
        list(map(lambda vn: (vn - 40) * 100 / vn, valores_nominales[1:])),
        color='g',
        linestyle='--'
    )
    plt.plot(
        tiempos[1:],
        list(map(lambda vn: (vn - 60) * 100 / vn, valores_nominales[1:])),
        color='y',
        linestyle='--'
    )
    # plt.axhline(y=106, color='y', linestyle='--', label='Umbral 3')
    # plt.axhline(y=104, color='g', linestyle='--', label='Umbral 2')
    # plt.axhline(y=102, color='b', linestyle='--', label='Umbral 1')
    plt.axhline(y=100, color='r', linestyle='--', label='Valor nominal')
    # plt.axhline(y=98, color='b', linestyle='--')
    # plt.axhline(y=96, color='g', linestyle='--')
    # plt.axhline(y=94, color='y', linestyle='--')
    plt.xlabel('Tiempo [min]')
    plt.ylabel('Porcentaje de requests')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 2, 3)
    plt.plot(tiempos, perturbaciones_list)
    plt.xlabel('Tiempo [min]')
    plt.ylabel('Perturbaciones [Req]')
    plt.grid(True)

    plt.subplot(3, 2, 4)
    plt.plot(tiempos, valores_e)
    plt.xlabel('Tiempo [min]')
    plt.ylabel('Señal de error (e=f+θi)')
    plt.grid(True)

    plt.subplot(3, 2, 5)
    plt.plot(tiempos, valores_nominales)
    plt.xlabel('Tiempo [min]')
    plt.ylabel('Entrada (θi)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    while True:
        root = tk.Tk()
        root.withdraw()

        messagebox.showinfo(
            "Simulación", "Bienvenido a la simulación de un Rate Limiter.\nSe le solicitará ingresar los valores nominales y las perturbaciones a continuación.")

        initial_nominal = simpledialog.askinteger(
            "Input", "Ingrese valor nominal inicial:", minvalue=1)
        if initial_nominal is None:
            break

        nominal_changes = {}
        while True:
            change_time = simpledialog.askinteger(
                "Input", "Ingrese tiempo para cambiar valor nominal (o -1 para finalizar):", minvalue=-1)
            if change_time == -1 or change_time is None:
                break
            new_value = simpledialog.askinteger(
                "Input", f"Ingrese valor nominal para tiempo={change_time}:")
            nominal_changes[change_time] = new_value

        perturbaciones = {}
        while True:
            perturb_time = simpledialog.askinteger(
                "Input", "Ingrese tiempo de perturbación (o -1 para finalizar):", minvalue=-1)
            if perturb_time == -1 or perturb_time is None:
                break
            perturb_value = simpledialog.askinteger(
                "Input", "Ingrese valor de perturbación:")
            perturbaciones[perturb_time] = perturb_value

        run_simulation(initial_nominal, nominal_changes, perturbaciones)

        if not messagebox.askyesno("Continuar", "¿Desea realizar otra simulación?"):
            messagebox.showinfo(
                "Fin", "Gracias por utilizar el sistema de simulación.")
            break


if __name__ == "__main__":
    main()
