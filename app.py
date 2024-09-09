import tkinter as tk
import ttkbootstrap as ttk
from main import agent
from tools import update_chat_history
def query():
    prompt = prompt_string.get()
    result = agent.query(prompt)
    update_chat_history("QUERY: "+ prompt)
    update_chat_history("ANSWER: " + str(result))
    result_string.set(result)


window = ttk.Window(themename='flatly')
window.title('F1 Chatbot')
window.geometry('800x400')

title_label = ttk.Label(master = window, text = "F1 Chatbot", font = 'Times 24')
title_label.pack()

input_frame = ttk.Frame(master=window)
prompt_string = tk.StringVar()
prompt_field = ttk.Entry(master = input_frame, textvariable = prompt_string, width = 100)
submit_button = ttk.Button(master = input_frame, text = 'Submit', command = query)

prompt_field.pack(side = 'left', padx = 10)
submit_button.pack(side = 'left')
input_frame.pack(pady=10)

result_string = tk.StringVar()
result_label = ttk.Label(master = window, textvariable = result_string, font='Calibri 16')
result_label.pack(pady=100)

window.mainloop()