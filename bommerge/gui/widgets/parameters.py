try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


class Parameters(tk.LabelFrame):
    def __init__(self, parent, parameters):
        tk.LabelFrame.__init__(self, parent, text="Parameters")
        self.variable = []
        self.label = []
        self.update(parameters)


    def _add_parameter(self):
        self.variable.append(tk.StringVar())
        self.label.append(tk.Label(self, textvariable=self.variable[-1]))


    def update(self, parameters):
        for i in range(len(parameters) - len(self.label)):
            self._add_parameter()

        for i, parameter in enumerate(parameters):
            if parameters[parameter] is not None:
                self.variable[i].set(parameter + ': ' + parameters[parameter])

        for i, label in enumerate(self.label):
            if i < len(parameters):
                label.grid(row=i, sticky=tk.W, padx=10)
            else:
                label.grid_forget()


def test():
    root = tk.Tk()
    root.title("BOM Merger")
    parameters = {
        "Capacitance": "10uF",
        "Capacitors series": "GRM",
        "Case - inch": "0805",
        "Case - mm": "2012",
        "Dielectric": "X7R",
        "Kind of capacitor": "MLCC",
        "Manufacturer": "MURATA",
        "Manufacturer Part Number": "GRM21BR71A106KE51L",
        "Mounting": "SMD",
        "Operating temperature": "-55...125\u00b0C",
        "Operating voltage": "10V",
        "Tolerance": "10",
        "Type of capacitor": "ceramic"
    }
    order = Parameters(root, parameters)
    order.pack()
    root.mainloop()


if __name__ == "__main__":
    test()
