import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

class CarbonCleanupGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Cleanup Mini Game")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#222")

        try:
            self.font = tkFont.Font(family="Delius", size=14)
        except:
            self.font = ("Arial", 14)

        self.stage = 1
        self.tasks_completed = 0
        self.TASKS_PER_STAGE = 2

        self.canvas = tk.Canvas(root, width=800, height=360, bg="#222", highlightthickness=0)
        self.canvas.pack()

        self.status_label = tk.Label(root, text="", font=self.font, fg="white", bg="#222")
        self.status_label.pack(pady=10)

        self.task_frame = tk.Frame(root, bg="#222")
        self.task_frame.pack(pady=10)

        self.draw_car()
        self.load_tasks()

    def draw_car(self):
        self.canvas.delete("all")

        if self.stage == 1:
            car_color = "#444"
            status = "The car is heavily polluted"
        elif self.stage == 2:
            car_color = "#777"
            status = "The car is getting cleaner"
        elif self.stage == 3:
            car_color = "#aaa"
            status = "The car is almost clean"
        else:
            car_color = "green"
            status = "The car is fully clean"

        self.canvas.create_rectangle(250, 180, 550, 250, fill=car_color)
        self.canvas.create_rectangle(320, 150, 480, 180, fill=car_color)
        self.canvas.create_oval(280, 250, 330, 300, fill="black")
        self.canvas.create_oval(470, 250, 520, 300, fill="black")

        if self.stage <= 2:
            self.canvas.create_oval(380, 210, 420, 235, outline="black", width=3)
        if self.stage == 1:
            self.canvas.create_line(300, 215, 350, 225, width=3)

        self.status_label.config(text=status)

    def complete_task(self, button):
        button.config(state="disabled", text="Completed")
        self.tasks_completed += 1

        if self.tasks_completed >= self.TASKS_PER_STAGE:
            self.tasks_completed = 0
            self.stage += 1
            self.load_tasks()
            self.draw_car()

    def load_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        if self.stage == 1:
            tasks = ["Use Public Transport", "Walk or Cycle"]
        elif self.stage == 2:
            tasks = ["Save Electricity", "Use LED Lights"]
        elif self.stage == 3:
            tasks = ["Plant Trees", "Recycle Waste"]
        else:
            tk.Label(
                self.task_frame,
                text="All tasks completed 🎉",
                font=self.font,
                fg="lightgreen",
                bg="#222"
            ).pack()
            return

        for task in tasks:
            btn = tk.Button(self.task_frame, text=task, font=self.font, width=30)
            btn.config(command=lambda b=btn: self.complete_task(b))
            btn.pack(pady=5)

root = tk.Tk()
root.title("Carbon Calculator: Enter weekly value")
root.geometry("420x650")
root.config(bg="dark red")

def open_game():
    root.destroy()
    game_root = tk.Tk()
    CarbonCleanupGame(game_root)
    game_root.mainloop()

def make_label(text):
    lbl = tk.Label(
        root,
        text=text,
        bg="dark orange",
        fg="white",
        font=("Times New Roman", 16),
        width=30,
        pady=15
    )
    lbl.pack(pady=(20, 5))

make_label("How many days do you use your car?")
fuel_entry = tk.Entry(root, font=("Times New Roman", 14), width=25)
fuel_entry.pack(pady=10)

make_label("What is your diet preference?")
diet_var = tk.StringVar(value="Vegetarian")

veg_radio = tk.Radiobutton(
    root, text="Vegetarian", variable=diet_var, value="Vegetarian",
    bg="dark red", fg="white", font=("Times New Roman", 14)
)
veg_radio.pack(pady=5)

nonveg_radio = tk.Radiobutton(
    root, text="Non-Vegetarian", variable=diet_var, value="Non-Vegetarian",
    bg="dark red", fg="white", font=("Times New Roman", 14)
)
nonveg_radio.pack(pady=5)

make_label("How many people are in the household?")
household_entry = tk.Entry(root, font=("Times New Roman", 14), width=25)
household_entry.pack(pady=10)

make_label("How many trashbags are used per week?")
trashbags_entry = tk.Entry(root, font=("Times New Roman", 14), width=25)
trashbags_entry.pack(pady=10)

def button_clicked():
    try:
        car_days = float(fuel_entry.get())
        household_size = float(household_entry.get())
        trashbags = float(trashbags_entry.get())
        diet_choice = diet_var.get()

        if car_days < 0 or car_days > 7:
            messagebox.showerror("Invalid Input", "Enter car usage between 0 and 7 days.")
            return

        if household_size <= 0:
            messagebox.showerror("Invalid Input", "Household size must be greater than 0.")
            return

        if trashbags < 0:
            messagebox.showerror("Invalid Input", "Trashbags cannot be negative.")
            return

        car_emission = car_days * 12.6
        waste_emission = trashbags * 0.18

        if diet_choice == "Vegetarian":
            diet_emission = 2.5
        else:
            diet_emission = 7.0

        total_emission = car_emission + waste_emission + diet_emission

        messagebox.showinfo(
            "Carbon Footprint Result",
            f"Weekly Carbon Footprint\n{total_emission:.2f} kg CO₂e"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

tk.Button(
    root,
    text="Calculate Carbon Footprint",
    bg="orange",
    fg="dark red",
    font=("Times New Roman", 16),
    width=25,
    pady=10,
    command=button_clicked
).pack(pady=20)

tk.Button(
    root,
    text="Go to Carbon Cleanup Game 🌱",
    bg="green",
    fg="white",
    font=("Times New Roman", 16),
    width=25,
    pady=10,
    command=open_game
).pack(pady=10)

root.mainloop()
