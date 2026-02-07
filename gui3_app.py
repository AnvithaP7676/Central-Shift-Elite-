import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Carbon Calculator")
root.geometry("420x650")
root.config(bg="dark red")

text_var1 = tk.StringVar()
text_var1.set("Fuel emission rate (kWh)")

label1 = tk.Label(
    root,
    textvariable=text_var1,
    anchor=tk.CENTER,
    bg="orange",
    height=1,
    width=30,
    bd=2,
    font=("Times New Roman", 16),
    cursor="hand2",
    fg="white",
    padx=15,
    pady=15,
    justify=tk.CENTER,
    relief=tk.RAISED,
    underline=0,
    wraplength=250
)
label1.pack(pady=(20, 5))

fuel_entry = tk.Entry(
    root,
    font=("Times New Roman", 14),
    width=25
)
fuel_entry.pack(pady=10)

text_var2 = tk.StringVar()
text_var2.set("Dietary Choice (Veg / Non-Veg)")

label2 = tk.Label(
    root,
    textvariable=text_var2,
    anchor=tk.CENTER,
    bg="orange",
    height=1,
    width=30,
    bd=2,
    font=("Times New Roman", 16),
    cursor="hand2",
    fg="white",
    padx=15,
    pady=15,
    justify=tk.CENTER,
    relief=tk.RAISED,
    underline=0,
    wraplength=250
)
label2.pack(pady=(20, 5))

diet_entry = tk.Entry(
    root,
    font=("Times New Roman", 14),
    width=25
)
diet_entry.pack(pady=10)

text_var3 = tk.StringVar()
text_var3.set("Volume of Waste (kg)")

label3 = tk.Label(
    root,
    textvariable=text_var3,
    anchor=tk.CENTER,
    bg="orange",
    height=1,
    width=30,
    bd=2,
    font=("Times New Roman", 16),
    cursor="hand2",
    fg="white",
    padx=15,
    pady=15,
    justify=tk.CENTER,
    relief=tk.RAISED,
    underline=0,
    wraplength=250
)
label3.pack(pady=(20, 5))

waste_entry = tk.Entry(
    root,
    font=("Times New Roman", 14),
    width=25
)
waste_entry.pack(pady=10)

def button_clicked():
    try:
        fuel = float(fuel_entry.get())
        waste = float(waste_entry.get())
        diet = diet_entry.get().lower()

        fuel_emission = fuel * 0.82
        waste_emission = waste * 0.5

        if diet == "veg":
            diet_emission = 1700
        elif diet == "non-veg" or diet == "non veg":
            diet_emission = 2500
        else:
            messagebox.showerror(
                "Invalid Input",
                "Please enter diet as Veg or Non-Veg"
            )
            return

        total_emission = fuel_emission + waste_emission + diet_emission

        if fuel_emission >= waste_emission and fuel_emission >= diet_emission:
            insight = (
                "SustainX Insight\n\n"
                "Your energy consumption is the largest contributor.\n"
                "Reducing electricity use and switching to efficient appliances can help."
            )
        elif waste_emission >= fuel_emission and waste_emission >= diet_emission:
            insight = (
                "SustainX Insight\n\n"
                "Waste generation has a major impact.\n"
                "Reducing, recycling, and composting can lower emissions."
            )
        else:
            insight = (
                "SustainX Insight\n\n"
                "Dietary habits contribute significantly.\n"
                "Choosing more plant-based meals can reduce your footprint."
            )

        messagebox.showinfo(
            "Carbon Footprint Result",
            f"Total Carbon Footprint\n"
            f"{total_emission:.2f} kg CO₂\n\n"
            f"{insight}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numeric values."
        )

button = tk.Button(
    root,
    text="Calculate Carbon Footprint",
    bg="orange",
    fg="dark red",
    font=("Times New Roman", 16),
    width=25,
    pady=10,
    command=button_clicked
)
button.pack(pady=30)

root.mainloop()
