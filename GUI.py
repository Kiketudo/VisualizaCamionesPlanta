import tkinter as tk
import control as cont 
from tkinter import ttk
from datetime import datetime, timedelta

class TruckManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Información de Camiones")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()//2}+0+{self.winfo_screenheight()//2}")
        #self.geometry(f"1650x800+0+{self.winfo_screenheight() - 400}")
        self.attributes('-transparentcolor', 'red')
        self.configure(bg='red')
        self.attributes('-alpha', 0.8)  # Ajusta la transparencia (0.0 a 1.0)
        self.attributes('-topmost', True)  # Siempre en la parte superior
        self.overrideredirect(True)  # Sin bordes ni barra de título
        self.filas = None
        self.filas_tabla = None
        self.n_cmaiones_puerta = None

        self.create_widgets()
        self.update_data()

    def make_click_through(self, hwnd):
        import ctypes
        styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x80000 | 0x20)  

    def update_data(self):
        filas = cont.obten_datos_basc()
        self.filas_tabla , self.n_cmaiones_puerta = cont.datos_tabla()
        self.filas = filas
        self.update_widgets()
        self.after(50000, self.update_data)
        

    def create_widgets(self):
        max_estancia = None
        ocupacion = None
        '''for fila in self.filas:
            hora_fila = datetime.strptime(fila.HORA_E, '%H:%M:%S')
            hora_actual= datetime.now().time()
            estancia = datetime.combine(datetime.today(), hora_actual) - datetime.combine(datetime.today(), hora_fila.time())
            if(max_estancia is None or estancia > max_estancia):
                max_estancia = estancia
        total_hours = (datetime(1, 1, 1) + max_estancia).strftime("%H:%M:%S")
        max_estancia = max_estancia.total_seconds() / 3600'''


        main_frame = tk.Frame(self, bg='red')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame para las barras de progreso
        progress_frame = tk.Frame(main_frame, bg='red')
        progress_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Barra de progreso vertical 1
        self.progress_label1 = ttk.Label(progress_frame, text="Ocupación de la Fábrica: " + str(ocupacion))
        self.progress_label1.pack(pady=5)
        self.progress_bar1 = ttk.Progressbar(progress_frame, orient="vertical", length=100, mode="determinate", style="blue.Vertical.TProgressbar")
        self.progress_bar1.pack(pady=5)

        # Barra de progreso vertical 2
        self.progress_label2 = ttk.Label(progress_frame, text="Máxima estancia: " + str(max_estancia) )
        self.progress_label2.pack(pady=5)
        self.progress_bar2 = ttk.Progressbar(progress_frame, orient="vertical", length=100, mode="determinate", style="blue.Vertical.TProgressbar")
        self.progress_bar2.pack(pady=5)

        # Botón para ampliar información de las barras
        self.expand_bars_button = ttk.Button(progress_frame, text="Ampliar", command=self.show_bars_info)
        self.expand_bars_button.pack(pady=10)
        # Frame para la tabla
        table_frame = tk.Frame(main_frame, bg='red', width=100)
        table_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=10, pady=10)

        # Tabla de camiones en la fábrica
        factory_columns = ("Puerta", "Nº")
        self.factory_tree = ttk.Treeview(table_frame, columns=factory_columns,height = 15, show='headings')
        self.factory_tree.heading(factory_columns[0], text=factory_columns[0])
        self.factory_tree.column(factory_columns[0], width=70)
        self.factory_tree.heading(factory_columns[1], text=factory_columns[1])
        self.factory_tree.column(factory_columns[1], width=15)
        self.factory_tree.pack(fill=tk.BOTH, expand=False)

        # Botón para ampliar información de la tabla
        self.expand_table_button = ttk.Button(table_frame, text="Ampliar", command=self.show_table_info)
        self.expand_table_button.pack(pady=10)

        # Datos de ejemplo
        self.load_data()


    def update_widgets(self):
        max_estancia = None
        ocupacion = len(self.filas)
        for fila in self.filas:
            hora_fila = datetime.strptime(fila.HORA_E, '%H:%M:%S')
            hora_actual = datetime.now().time()
            estancia = datetime.combine(datetime.today(), hora_actual) - datetime.combine(datetime.today(), hora_fila.time())
            if max_estancia is None or estancia > max_estancia:
                max_estancia = estancia
        total_hours = (datetime(1, 1, 1) + max_estancia).strftime("%H:%M:%S")
        max_estancia = max_estancia.total_seconds() / 3600

        self.progress_label1.config(text="Ocupación de la Fábrica: " + str(ocupacion))
        self.progress_label2.config(text="Máxima estancia: " + str(total_hours))

        self.update_progress(ocupacion, max_estancia)

        for row in self.factory_tree.get_children():
            self.factory_tree.delete(row)
        
        for a, b in zip(self.n_cmaiones_puerta['Denom.'], self.n_cmaiones_puerta['counts']):
            self.factory_tree.insert("", tk.END, values=(a,b))

    
    def update_progress(self, num_factory_trucks, maxima_estancia):
        max_trucks = 30
        progress1 = (num_factory_trucks / max_trucks) * 100
        self.progress_bar1['value'] = progress1

        progress2 = (maxima_estancia/6) *100
        self.progress_bar2['value'] = progress2

        # Cambiar color de la barra de progreso 1
        if progress1 <= 25:
            style1 = "green.Vertical.TProgressbar"
        elif progress1 <= 50:
            style1 = "blue.Vertical.TProgressbar"
        elif progress1 <= 75:
            style1 = "yellow.Vertical.TProgressbar"
        else:
            style1 = "red.Vertical.TProgressbar"
        self.progress_bar1.configure(style=style1)

        # Cambiar color de la barra de progreso 2
        if progress2 <= 25:
            style2 = "green.Vertical.TProgressbar"
        elif progress2 <= 50:
            style2 = "blue.Vertical.TProgressbar"
        elif progress2 <= 75:
            style2 = "yellow.Vertical.TProgressbar"
        else:
            style2 = "red.Vertical.TProgressbar"
        self.progress_bar2.configure(style=style2)

    def show_bars_info(self):
        # Crear una nueva ventana para mostrar más información sobre las barras
        bars_info_window = tk.Toplevel(self)
        bars_info_window.title("Información de Barras")
        bars_info_window.geometry("800x600")
        bars_info_window.attributes('-topmost', True)

        # Tabla de información de barras
        bars_columns = ("Camión", "hora entrada","estancia", "transportista")
        bars_tree = ttk.Treeview(bars_info_window, columns=bars_columns, show='headings')
        for col in bars_columns:
            bars_tree.heading(col, text=col)
        bars_tree.pack(fill=tk.BOTH, expand=True)
        hora_actual= datetime.now().time()
        filas = self.filas
        for fila in filas:
            hora_fila = datetime.strptime(fila.HORA_E, '%H:%M:%S')
            estancia = datetime.combine(datetime.today(), hora_actual) - datetime.combine(datetime.today(), hora_fila.time())
            bars_tree.insert("", tk.END, values=(fila.Matricula_Camion_R, fila.HORA_E, estancia, fila.Descripcion_Transp_T))

    def show_table_info(self):
        # Crear una nueva ventana para mostrar más información sobre la tabla
        table_info_window = tk.Toplevel(self)
        table_info_window.title("Información de Tabla")
        table_info_window.geometry("800x400")
        table_info_window.attributes('-topmost', True)

        # Tabla de información detallada
        detailed_columns = ("Puerta", "Camión", "Orden de carga", "Lotes")
        detailed_tree = ttk.Treeview(table_info_window, columns=detailed_columns, show='headings')
        for col in detailed_columns:
            detailed_tree.heading(col, text=col)
        detailed_tree.pack(fill=tk.BOTH, expand=True)

        # Datos de ejemplo para la tabla de información detallada

        for a, b, c, d in zip(self.filas_tabla['Denom.'], self.filas_tabla['Matricula_Camion_R'], self.filas_tabla['NumTrnsprt'],  self.filas_tabla['counts']):
            detailed_tree.insert("", tk.END, values=(a, b, c, d))

if __name__ == "__main__":
    while True:
        app = TruckManagementApp()
        style = ttk.Style(app)
        style.theme_use('default')
        style.configure("green.Vertical.TProgressbar", troughcolor='white', background='green')
        style.configure("blue.Vertical.TProgressbar", troughcolor='white', background='blue')
        style.configure("yellow.Vertical.TProgressbar", troughcolor='white', background='yellow')
        style.configure("red.Vertical.TProgressbar", troughcolor='white', background='orange')
        style.configure("Custom.TFrame", background='red')  # Cambia 'lightgray' por el color que prefieras
        app.mainloop()