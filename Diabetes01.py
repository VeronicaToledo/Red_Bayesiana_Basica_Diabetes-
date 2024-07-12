from tkinter import *
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Función para realizar la inferencia
def realizar_inferencia():
    # Obtener los valores de las casillas de verificación
    glucosa_value = glucosa_var.get()
    presion_value = presion_var.get()
    
    # Crear el diccionario de evidencia
    evidence = {'Glucosa': glucosa_value, 'PresionArterial': presion_value}
    
    # Realizar la inferencia
    result = infer.query(variables=['Diabetes'], evidence=evidence)
    
    # Mostrar el resultado en la etiqueta de resultado
    resultado_label.config(text=f"Resultado de la inferencia:\n{result}")

# Función para configurar la geometría de la ventana
def configurar_ventana():
    root.geometry('500x250')  # Tamaño de la ventana

# Crear la ventana principal de la interfaz
root = Tk()
root.title("Inferencia en Red Bayesiana")

# Configurar la geometría de la ventana
configurar_ventana()

# Definición de la estructura del modelo de la red bayesiana
model = BayesianNetwork([('Glucosa', 'Diabetes'), ('PresionArterial', 'Diabetes')])

# CPD para Glucosa
cpd_glucosa = TabularCPD(variable='Glucosa', variable_card=2,
                         values=[[0.8], [0.2]])

# CPD para PresionArterial
cpd_presion = TabularCPD(variable='PresionArterial', variable_card=2,
                         values=[[0.7], [0.3]])

# CPD para Diabetes dado Glucosa y PresionArterial
cpd_diabetes = TabularCPD(variable='Diabetes', variable_card=2,
                          values=[[0.9, 0.6, 0.7, 0.1], [0.1, 0.4, 0.3, 0.9]],
                          evidence=['Glucosa', 'PresionArterial'],
                          evidence_card=[2, 2])

# Añadir los CPDs al modelo
model.add_cpds(cpd_glucosa, cpd_presion, cpd_diabetes)

# Comprobar si el modelo es correcto
assert model.check_model()

# Crear un objeto de inferencia usando Variable Elimination
infer = VariableElimination(model)

# Variables para almacenar el estado de las casillas de verificación
glucosa_var = IntVar()
presion_var = IntVar()

# Crear etiquetas y casillas de verificación para Glucosa
Label(root, text="Valor de Glucosa:").grid(row=0, column=0, padx=10, pady=10)
Checkbutton(root, text="Sí", variable=glucosa_var, onvalue=1, offvalue=0).grid(row=0, column=1, padx=10, pady=10)
Checkbutton(root, text="No", variable=glucosa_var, onvalue=0, offvalue=1).grid(row=0, column=2, padx=10, pady=10)

# Crear etiquetas y casillas de verificación para PresionArterial
Label(root, text="Valor de PresionArterial:").grid(row=1, column=0, padx=10, pady=10)
Checkbutton(root, text="Sí", variable=presion_var, onvalue=1, offvalue=0).grid(row=1, column=1, padx=10, pady=10)
Checkbutton(root, text="No", variable=presion_var, onvalue=0, offvalue=1).grid(row=1, column=2, padx=10, pady=10)

# Botón para realizar la inferencia
inferencia_button = Button(root, text="Realizar Inferencia", command=realizar_inferencia)
inferencia_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Etiqueta para mostrar el resultado
resultado_label = Label(root, text="Resultado de la inferencia:")
resultado_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Ejecutar la ventana principal
root.mainloop()
