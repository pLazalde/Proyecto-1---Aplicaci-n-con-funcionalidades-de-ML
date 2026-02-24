import joblib
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# 1. Cargar el pipeline
try:
    pipeline = joblib.load('model.pkl')
    print("Modelo cargado correctamente")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

# 2. Configuración principal de la ventana
root = tk.Tk()
root.title("EduPredict: Sistema de Análisis de Rendimiento")
root.geometry("850x600")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use('clam') 

vars_dict = {}

main_frame = ttk.Frame(root, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)

frame_acad = ttk.LabelFrame(main_frame, text=" Métrica Académica y Hábitos ", padding="10")
frame_acad.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

campos_num = [
    ("Horas estudiadas (0 - 44)", 'Hours_Studied', 20),
    ("Asistencia % (60 - 100)", 'Attendance', 80),
    ("Horas de sueño Diarias(0 - 10)", 'Sleep_Hours', 7),
    ("Calificaciones previas (50 - 100)", 'Previous_Scores', 75),
    ("Sesiones de tutoría (0 - 8)", 'Tutoring_Sessions', 1),
    ("Días act. física (0 - 6)", 'Physical_Activity', 3)
]

# Diccionario interno de límites para la validación lógica
limites_num = {
    'Hours_Studied': (0, 44),
    'Attendance': (60, 100),
    'Sleep_Hours': (0, 10),
    'Previous_Scores': (50, 100),
    'Tutoring_Sessions': (0, 8),
    'Physical_Activity': (0, 6)
}

for idx, (label, key, default) in enumerate(campos_num):
    ttk.Label(frame_acad, text=label, font=("Helvetica", 9, "bold")).grid(row=idx, column=0, pady=8, sticky="w")
    vars_dict[key] = tk.StringVar(value=str(default))
    ttk.Entry(frame_acad, textvariable=vars_dict[key], width=12).grid(row=idx, column=1, pady=8, padx=10)

campos_bin_acad = [
    ("Actividades extra.", 'Extracurricular_Activities', ['No', 'Yes'], 'Yes'),
    ("Discap. aprendizaje", 'Learning_Disabilities', ['No', 'Yes'], 'No'),
]

for idx, (label, key, opciones, default) in enumerate(campos_bin_acad, start=len(campos_num)):
    ttk.Label(frame_acad, text=label).grid(row=idx, column=0, pady=8, sticky="w")
    vars_dict[key] = tk.StringVar(value=default)
    cb = ttk.Combobox(frame_acad, textvariable=vars_dict[key], values=opciones, state="readonly", width=10)
    cb.grid(row=idx, column=1, pady=8, padx=10)

frame_socio = ttk.LabelFrame(main_frame, text=" Contexto Familiar y Social ", padding="10")
frame_socio.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

campos_cat = [
    ("Involucramiento padres", 'Parental_Involvement', ['Low', 'Medium', 'High'], 'Medium'),
    ("Acceso a recursos", 'Access_to_Resources', ['Low', 'Medium', 'High'], 'Medium'),
    ("Nivel motivación", 'Motivation_Level', ['Low', 'Medium', 'High'], 'Medium'),
    ("Calidad profesor", 'Teacher_Quality', ['Low', 'Medium', 'High'], 'Medium'),
    ("Ingreso familiar", 'Family_Income', ['Low', 'Medium', 'High'], 'Medium'),
    ("Distancia hogar", 'Distance_from_Home', ['Near', 'Moderate', 'Far'], 'Near'),
    ("Educación padres", 'Parental_Education_Level', ['High School', 'College', 'Postgraduate'], 'College'),
    ("Acceso a internet", 'Internet_Access', ['No', 'Yes'], 'Yes'),
    ("Género", 'Gender', ['Male', 'Female'], 'Male'),
    ("Tipo escuela", 'School_Type', ['Public', 'Private'], 'Public'),
    ("Influencia de compañeros", 'Peer_Influence', ['Negative', 'Neutral', 'Positive'], 'Neutral')
]

for idx, (label, key, opciones, default) in enumerate(campos_cat):
    ttk.Label(frame_socio, text=label).grid(row=idx, column=0, pady=6, sticky="w")
    vars_dict[key] = tk.StringVar(value=default)
    cb = ttk.Combobox(frame_socio, textvariable=vars_dict[key], values=opciones, state="readonly", width=14)
    cb.grid(row=idx, column=1, pady=6, padx=10)

# FUNCIÓN DE PREDICCIÓN Y VALIDACIÓN
def predecir():
    try:
        data = {key: var.get() for key, var in vars_dict.items()}
        
        # 1. Validación estricta de numéricos y sus límites
        for k in limites_num.keys():
            # Verificar si es un número válido
            if not data[k].strip().replace('.', '', 1).isdigit():
                raise ValueError(f"El campo '{k}' debe ser un número válido.")
            
            valor_num = float(data[k])
            min_val, max_val = limites_num[k]
            
            # Verificar si está dentro del rango permitido
            if not (min_val <= valor_num <= max_val):
                raise ValueError(f"Valor fuera de límite.\n\nEl campo '{k}' debe estar entre {min_val} y {max_val}.\nIngresaste: {valor_num}")
                
            data[k] = valor_num
            
        # 2. Predicción
        df_input = pd.DataFrame([data])
        nota = pipeline.predict(df_input)[0]
        
        # Limitamos la nota visualmente a 100 si el modelo se excede un poco
        nota_final = min(nota, 100.0)
        
        messagebox.showinfo("Proyección Exitosa", f"🎯 La nota estimada del estudiante es:\n\n {nota_final:.2f} / 100")
        
    except ValueError as ve:
        messagebox.showwarning("Dato Inválido", str(ve))
    except Exception as e:
        messagebox.showerror("Error de Sistema", f"Ocurrió un error al procesar la predicción:\n{e}")

# Frame para el botón
frame_btn = ttk.Frame(root)
frame_btn.pack(pady=15)

btn_predict = tk.Button(frame_btn, text="CALCULAR RENDIMIENTO", command=predecir, 
                        bg="#2c3e50", fg="white", font=("Helvetica", 12, "bold"), 
                        padx=20, pady=10, relief="flat", cursor="hand2")
btn_predict.pack()

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

root.mainloop()