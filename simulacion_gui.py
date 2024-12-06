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
    valores_f = []

    estado_del_servidor = 0
    error_anterior = 0
    Kd = 0.4
    valor_nominal = initial_nominal

    for i in range(1000):
        # Update `valor_nominal` based on time if there are changes
        if i in nominal_changes:
            valor_nominal = nominal_changes[i]

        tiempos.append(i)
        variacion = random.randint(-50, +50)
        estado_del_servidor += variacion

        valor_real = estado_del_servidor
        valores_f.append(variacion)

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

    plt.figure(figsize=(20, 12))

    plt.subplot(3, 2, 1)
    plt.plot(tiempos, estados_sv, label='Requests por minuto')
    plt.axhline(y=initial_nominal, color='r', linestyle='--', label='Initial valor_nominal')
    for time, new_value in nominal_changes.items():
        plt.axvline(x=time, color='g', linestyle='--', label=f'Change at t={time}')
        plt.axhline(y=new_value, color='b', linestyle='--', label=f'New valor_nominal={new_value}')
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Requests/min')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 2, 2)
    plt.plot(tiempos, porcentajes_estado_sv, label='Porcentaje sobre valor nominal')
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Porcentaje de requests')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 2, 3)
    plt.plot(tiempos, perturbaciones_list)
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Perturbaciones')
    plt.grid(True)

    plt.subplot(3, 2, 4)
    plt.plot(tiempos, valores_e)
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Errores')
    plt.grid(True)

    plt.subplot(3, 2, 5)
    plt.plot(tiempos, valores_f)
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Mediciones')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    while True:
        root = tk.Tk()
        root.withdraw()

        initial_nominal = simpledialog.askinteger("Input", "Enter initial valor_nominal:", minvalue=1)
        if initial_nominal is None:
            break

        nominal_changes = {}
        while True:
            change_time = simpledialog.askinteger("Input", "Enter time to change valor_nominal (or -1 to finish):", minvalue=-1)
            if change_time == -1 or change_time is None:
                break
            new_value = simpledialog.askinteger("Input", f"Enter new valor_nominal at time={change_time}:")
            nominal_changes[change_time] = new_value

        perturbaciones = {}
        while True:
            perturb_time = simpledialog.askinteger("Input", "Enter perturbation time (or -1 to finish):", minvalue=-1)
            if perturb_time == -1 or perturb_time is None:
                break
            perturb_value = simpledialog.askinteger("Input", "Enter perturbation value:")
            perturbaciones[perturb_time] = perturb_value

        run_simulation(initial_nominal, nominal_changes, perturbaciones)

        if not messagebox.askyesno("Continue", "Do you want to run another simulation?"):
            break

if __name__ == "__main__":
    main()
