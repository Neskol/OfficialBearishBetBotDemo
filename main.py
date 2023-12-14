import tkinter as tk
from tkinter import font, ttk, scrolledtext
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import webbrowser
from Alpaca.Trades import get_buying_power
import pygame
from Alpaca.MakeTrade import make_trade_decision
from elasticsearch import Elasticsearch
from ElasticSearchSequence.query import query_posts_for_stock, es_iterate_all_documents

def submit():
    es = Elasticsearch(hosts=["http://localhost:9200"])
    input_str = entry.get()
    response = process_input(input_str)
    result_label.config(text=response)
    output_log(f"Input: {input_str}")
    status_label.config(text="Processing")
    # make_trade_decision(50, .8, 'NEG', 'GME', .99, callback=output_log) #EXAMPLE!!! we will need to pass this callback in to post updates to the gui log
    query_posts_for_stock(es, input_str, callback=output_log)
    status_label.config(text="Task Completed")

def process_input(input_str):
    print(f"Ticker: {input_str}")
    return f"Ticker: {input_str}"

def button_log(btn_name):
    output_log(f"Button {btn_name} was pressed.")
    status_label.config(text="Idle")

### USE THIS TO ADD OTHER STUFF TO LOG
def output_log(text):
    log_text.config(state='normal')
    log_text.insert(tk.END, text + "\n")
    log_text.config(state='disabled')
    log_text.see(tk.END)

def open_alpaca():
    output_log('Opening Alpaca...')
    webbrowser.open("https://app.alpaca.markets/paper/dashboard/overview")
    status_label.config(text="Idle")

def view_buying_power():
    output_log(f'Fetching buying power...')
    buying_power = get_buying_power(callback=output_log)
    output_log(f'Sup brokey, you only got ${buying_power:,.2f} in buying power')
    status_label.config(text="Idle")

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("./assets/money.wav")  # Replace with the path to your sound file
    pygame.mixer.music.play()
    output_log('KA-CHING')

# Create the root window with a dark theme
root = ThemedTk(theme="equilux")

root.title('Official Bear-ish-Bets-Bot')
root.geometry('700x500')

# Create a font for widgets
widget_font = font.Font(family="Comic Sans MS", size=15, weight=font.BOLD)
status_font = font.Font(family="Comic Sans MS", size=10, weight=font.BOLD)

frame = ttk.Frame(root, padding="10")
frame.pack(fill='both', expand=True)

frame.columnconfigure(0, weight=1)  # left frame (inputs and buttons)
frame.columnconfigure(1, weight=1)  # right frame (gif)
frame.rowconfigure(0, weight=1)  # top frame
frame.rowconfigure(1, weight=3)  # bottom frame (log)

# Input and Buttons
input_button_frame = ttk.Frame(frame)
input_button_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

title_label = ttk.Label(input_button_frame, text="Make ur money number go up:", font=widget_font)
title_label.pack(side='top')

entry = ttk.Entry(input_button_frame, font=widget_font)
entry.pack(side='top')

submit_button = ttk.Button(input_button_frame, text='Submit', command=submit)
submit_button.pack(side='top')

result_label = ttk.Label(input_button_frame, text="", font=widget_font)
result_label.pack(side='bottom')

# Create a new style
style = ttk.Style()
style.configure("Link.TButton",
                foreground="#ADD8E6", 
                font=("Helvetica", 10, "underline"))

# 4 buttons
button_frame = ttk.Frame(frame)
button_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

button1 = ttk.Button(button_frame, text='Buying Power', command=lambda: view_buying_power())
button1.pack(side='left')
button2 = ttk.Button(button_frame, text='Button 2', command=lambda: play_sound())
button2.pack(side='left')
button4 = ttk.Button(button_frame, text='View Gains!!!\n@ALPACA', style="Link.TButton", command=lambda: open_alpaca())
button4.pack(side='left')

# List of GIF paths
gif_paths = ['./assets/wsb1.gif', './assets/wsb2.gif', './assets/wsb3.gif','./assets/wsb4.gif','./assets/wsb5.gif','./assets/wsb6.gif','./assets/wsb7.gif','./assets/wsb8.gif','./assets/wsb9.gif']

# Load the GIFs
gif_data = []
for gif_path in gif_paths:
    image = Image.open(gif_path)
    frames = []
    try:
        while True:
            resized = image.copy().convert('RGBA').resize((300, 200))  # change the dimensions as needed
            photo = ImageTk.PhotoImage(resized)
            frames.append(photo)
            image.seek(image.tell() + 1)
    except EOFError:
        pass
    gif_data.append(frames)

# Add the GIF to a label
gif_frame = ttk.Frame(frame)
gif_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=10, pady=10)

gif_label = tk.Label(gif_frame)
gif_label.pack()

def update_image():
    current_frames = gif_data[update_image.current_gif]
    update_image.current_frame = (update_image.current_frame + 1) % len(current_frames)
    gif_label.config(image=current_frames[update_image.current_frame])
    # Move to the next GIF after the current one finishes
    if update_image.current_frame == 0:
        update_image.current_gif = (update_image.current_gif + 1) % len(gif_data)
    root.after(100, update_image)
update_image.current_frame = 0
update_image.current_gif = 0
root.after(100, update_image)

# Add a log section
log_text = scrolledtext.ScrolledText(frame, width=40, height=10)
log_text.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
log_text.config(state='disabled')

status_label = ttk.Label(root, text="Status: Idle", font=status_font, anchor="w")
status_label.pack(fill='x', side='bottom', ipady=2)

root.mainloop()




