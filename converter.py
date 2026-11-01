import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        
        # Categories
        self.categories = {
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Distance": ["Meters", "Kilometers", "Miles", "Feet", "Inches"],
            "Weight": ["Grams", "Kilograms", "Pounds", "Ounces"],
            "Time": ["Seconds", "Minutes", "Hours", "Days"]
        }
        
        # Conversion factors/methods
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Unit Converter", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Category selection
        category_frame = tk.Frame(self.root)
        category_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(category_frame, text="Category:", font=("Arial", 10)).pack(anchor="w")
        self.category_var = tk.StringVar(value="Temperature")
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, 
                                          values=list(self.categories.keys()), state="readonly")
        self.category_combo.pack(fill="x", pady=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.update_units)
        
        # From unit
        from_frame = tk.Frame(self.root)
        from_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(from_frame, text="From:", font=("Arial", 10)).pack(anchor="w")
        input_frame = tk.Frame(from_frame)
        input_frame.pack(fill="x", pady=5)
        
        self.from_var = tk.StringVar()
        self.from_entry = tk.Entry(input_frame, textvariable=self.from_var, font=("Arial", 12))
        self.from_entry.pack(side="left", fill="x", expand=True)
        
        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(input_frame, textvariable=self.from_unit_var, 
                                           width=15, state="readonly")
        self.from_unit_combo.pack(side="right", padx=(5,0))
        
        # To unit
        to_frame = tk.Frame(self.root)
        to_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(to_frame, text="To:", font=("Arial", 10)).pack(anchor="w")
        output_frame = tk.Frame(to_frame)
        output_frame.pack(fill="x", pady=5)
        
        self.to_var = tk.StringVar()
        self.to_entry = tk.Entry(output_frame, textvariable=self.to_var, font=("Arial", 12), state="readonly")
        self.to_entry.pack(side="left", fill="x", expand=True)
        
        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(output_frame, textvariable=self.to_unit_var, 
                                         width=15, state="readonly")
        self.to_unit_combo.pack(side="right", padx=(5,0))
        
        # Convert button
        convert_btn = tk.Button(self.root, text="Convert", command=self.convert, 
                               font=("Arial", 12), bg="#4CAF50", fg="white", 
                               padx=20, pady=5)
        convert_btn.pack(pady=20)
        
        # Clear button
        clear_btn = tk.Button(self.root, text="Clear", command=self.clear, 
                             font=("Arial", 12), bg="#f44336", fg="white", 
                             padx=20, pady=5)
        clear_btn.pack()
        
        # Initialize units
        self.update_units()
    
    def update_units(self, event=None):
        category = self.category_var.get()
        units = self.categories[category]
        
        self.from_unit_combo['values'] = units
        self.to_unit_combo['values'] = units
        
        if units:
            self.from_unit_var.set(units[0])
            self.to_unit_var.set(units[1] if len(units) > 1 else units[0])
    
    def convert(self):
        try:
            input_value = float(self.from_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        category = self.category_var.get()
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()
        
        result = self.convert_units(category, input_value, from_unit, to_unit)
        self.to_var.set(f"{result:.6g}")
    
    def convert_units(self, category, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
        
        if category == "Temperature":
            # Convert to Celsius first
            if from_unit == "Fahrenheit":
                celsius = (value - 32) * 5/9
            elif from_unit == "Kelvin":
                celsius = value - 273.15
            else:  # Celsius
                celsius = value
            
            # Convert from Celsius to target
            if to_unit == "Fahrenheit":
                return celsius * 9/5 + 32
            elif to_unit == "Kelvin":
                return celsius + 273.15
            else:  # Celsius
                return celsius
        
        elif category == "Distance":
            # Convert to meters first
            to_meters = {
                "Meters": 1,
                "Kilometers": 1000,
                "Miles": 1609.344,
                "Feet": 0.3048,
                "Inches": 0.0254
            }
            meters = value * to_meters[from_unit]
            return meters / to_meters[to_unit]
        
        elif category == "Weight":
            # Convert to grams first
            to_grams = {
                "Grams": 1,
                "Kilograms": 1000,
                "Pounds": 453.592,
                "Ounces": 28.3495
            }
            grams = value * to_grams[from_unit]
            return grams / to_grams[to_unit]
        
        elif category == "Time":
            # Convert to seconds first
            to_seconds = {
                "Seconds": 1,
                "Minutes": 60,
                "Hours": 3600,
                "Days": 86400
            }
            seconds = value * to_seconds[from_unit]
            return seconds / to_seconds[to_unit]
        
        return value
    
    def clear(self):
        self.from_var.set("")
        self.to_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop()
