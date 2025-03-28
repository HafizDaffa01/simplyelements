import tkinter as tk
import random
import json
from tkinter import messagebox

timer_enabled = True 
shop_enabled = True   
timer_duration = 10   

def load_periodic_table(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["elements"]

def generate_question():
    global current_element, question_type, timer
    current_element = random.choice(elements)
    
    question_type = random.choice(difficulty_questions[difficulty.get()])

    if question_type == "symbol":
        question_label.config(text=f"What is the symbol for {current_element['name']}?")
    elif question_type == "atomic_number":
        question_label.config(text=f"What is the atomic number for {current_element['name']}?")
    elif question_type == "atomic_mass":
        question_label.config(text=f"What is the atomic mass of {current_element['name']}?")
    elif question_type == "group":
        question_label.config(text=f"In which group is {current_element['name']} located?")

    answer_entry.delete(0, tk.END)

    if timer_enabled: 
        global timer
        timer = timer_duration
        timer_label.config(text=f"Time: {timer} seconds")
        countdown()
    
    if score == -5:
        random_messages = [
            "Maybe next time?",
            "Keep trying, you'll get it!",
            "Almost there, don't give up!",
            "Good effort, keep it up!",
            "You're doing great, just a bit more!",
            "Not this time, but stay positive!",
            "You're on the right track, keep going!",
            "Every mistake is a step towards success!",
            "Don't worry, every expert was once a beginner!"
        ]
        messagebox.showinfo("SimplyElements", random.choice(random_messages))

def countdown():
    global timer, score
    if timer > 0:
        timer -= 1
        timer_label.config(text=f"Time: {timer} seconds")
        window.after(1000, countdown)
    else:
        feedback_label.config(text=f"Time's up! The correct answer was {current_element[question_type]}.", fg="red")
        score -= 5
        generate_question()

def check_answer():
    global money, score
    user_answer = answer_entry.get().strip()
    correct_answer = current_element[question_type]
    
    if question_type in ["atomic_number", "atomic_mass", "group"]:
        correct_answer = str(correct_answer)

    if user_answer.lower() == str(correct_answer).lower():
        feedback_label.config(text="Correct!", fg="green")
        update_score(5)
        money += 1 
        money_label.config(text=f"Money: {money}")
    else:
        feedback_label.config(text=f"Incorrect! The correct answer is {correct_answer}.", fg="red")
        update_score(-5) 

    answer_entry.delete(0, tk.END) 
    generate_question() 

def update_score(points):
    global score
    score += points
    score_label.config(text=f"Score: {score}")

def show_score_window():
    score_window = tk.Toplevel(window)
    score_window.title("Score")
    
    score_label_display = tk.Label(score_window, text=f"Your Score: {score}\nMoney: {money}", font=("Arial", 16))
    score_label_display.pack(pady=20)
    
    close_button = tk.Button(score_window, text="Close", command=score_window.destroy)
    close_button.pack(pady=10)

def show_shop():
    shop_window = tk.Toplevel(window)
    shop_window.title("Shop")
    
    shop_label = tk.Label(shop_window, text="Welcome to the Shop! Choose an item to buy:", font=("Arial", 14))
    shop_label.pack(pady=10)
    
    def buy_item(cost, item_type=None):
        global money
        if money >= cost:
            money -= cost
            money_label.config(text=f"Money: {money}")
            messagebox.showinfo("Purchase Successful", f"You bought the {item_type if item_type else 'item'}!")
            if item_type == "Skip Level":
                generate_question()
        else:
            messagebox.showwarning("Not Enough Money", "You don't have enough money to buy this item.")
    
    item2_button = tk.Button(shop_window, text="Extra Time (Cost: 3)", command=lambda: buy_item(3, "Extra Time"))
    item2_button.pack(pady=5)
    
    skip_level_button = tk.Button(shop_window, text="Skip Level (Cost: 5)", command=lambda: buy_item(5, "Skip Level"))
    skip_level_button.pack(pady=5)

def open_settings():
    settings_window = tk.Toplevel(title_screen) 
    settings_window.title("Settings")

    def toggle_timer():
        global timer_enabled
        timer_enabled = not timer_enabled
        timer_status.set("Enabled" if timer_enabled else "Disabled")

    def toggle_shop():
        global shop_enabled
        shop_enabled = not shop_enabled
        shop_status.set("Enabled" if shop_enabled else "Disabled")

    def set_timer_duration():
        global timer_duration
        try:
            timer_duration = int(timer_duration_entry.get())
            timer_duration_label.config(text=f"Current Timer Duration: {timer_duration} seconds")
            messagebox.showinfo("Timer Duration Set", f"Timer duration set to {timer_duration} seconds.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number for the timer duration.")

    timer_status = tk.StringVar(value="Enabled" if timer_enabled else "Disabled")
    timer_duration_label = tk.Label(settings_window, text=f"Current Timer Duration: {timer_duration} seconds", font=("Arial", 14))
    timer_duration_label.pack(pady=5)

    timer_duration_entry = tk.Entry(settings_window, font=("Arial", 14))
    timer_duration_entry.pack(pady=5)
    
    set_timer_button = tk.Button(settings_window, text="Set Timer Duration", font=("Arial", 14), command=set_timer_duration)
    set_timer_button.pack(pady=5)

    shop_status = tk.StringVar(value="Enabled" if shop_enabled else "Disabled")
    tk.Label(settings_window, text="Timer:", font=("Arial", 14)).pack(pady=5)
    tk.Button(settings_window, textvariable=timer_status, command=toggle_timer).pack(pady=5)

    tk.Label(settings_window, text="Shop:", font=("Arial", 14)).pack(pady=5)
    tk.Button(settings_window, textvariable=shop_status, command=toggle_shop).pack(pady=5)

def start_game():
    global window, money
    global question_label, answer_entry, feedback_label, score_label, timer_label, money_label
    
    title_screen.destroy()
    
    window = tk.Tk()
    window.title("SimplyElements")

    global score
    money = 0
    score = 0 

    question_label = tk.Label(window, text="", font=("Consolas", 16))
    question_label.pack(pady=20)

    answer_entry = tk.Entry(window, font=("Consolas", 14))
    answer_entry.pack(pady=10)

    submit_button = tk.Button(window, text="Submit", font=("Consolas", 14), command=check_answer)
    submit_button.pack(pady=10)

    feedback_label = tk.Label(window, text="", font=("Consolas", 14))
    feedback_label.pack(pady=20)

    score_label = tk.Label(window, text=f"Score: {score}", font=("Consolas", 14))
    score_label.pack(pady=10)

    money_label = tk.Label(window, text=f"Money: {money}", font=("Consolas", 14))
    money_label.pack(pady=10)

    timer_label = tk.Label(window, text="Time: 10 seconds", font=("Consolas", 14))
    timer_label.pack(pady=10)

    score_button = tk.Button(window, text="Show Score", font=("Consolas", 14), command=show_score_window)
    score_button.pack(pady=10)

    if shop_enabled: 
        shop_button = tk.Button(window, text="Shop", font=("Consolas", 14), command=show_shop)
        shop_button.pack(pady=10)

    generate_question()
    window.mainloop()

def set_difficulty(value):
    difficulty.set(value)

title_screen = tk.Tk()
title_screen.title("SimplyElements - Title Screen")

title_label = tk.Label(title_screen, text="SimplyElements", font=("Consolas", 24, "bold"))
title_label.pack(pady=20)

instruction_label = tk.Label(title_screen, text="Choose your difficulty:", font=("Consolas", 14))
instruction_label.pack(pady=10)

difficulty = tk.StringVar(value="Easy")

difficulty_frame = tk.Frame(title_screen)
difficulty_frame.pack(pady=10)

easy_button = tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty, value="Easy", font=("Consolas", 14), command=lambda: set_difficulty("Easy"))
easy_button.pack(side=tk.LEFT, padx=5)

medium_button = tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty, value="Medium", font=("Consolas", 14), command=lambda: set_difficulty("Medium"))
medium_button.pack(side=tk.LEFT, padx=5)

hard_button = tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty, value="Hard", font=("Consolas", 14), command=lambda: set_difficulty("Hard"))
hard_button.pack(side=tk.LEFT, padx=5)

start_button = tk.Button(title_screen, text="Start Game", font=("Consolas", 14), command=start_game)
start_button.pack(pady=20)

settings_button = tk.Button(title_screen, text="Settings", font=("Consolas", 14), command=open_settings)
settings_button.pack(pady=10)

elements = load_periodic_table("elements.json")

difficulty_questions = {
    "Easy": ["symbol"],
    "Medium": ["atomic_number", "symbol"],
    "Hard": ["atomic_mass", "group", "atomic_number", "symbol"]
}

title_screen.mainloop()
