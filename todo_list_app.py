import tkinter
import random
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="usbw",
    database="todo_list_db"
)
cursor = db.cursor()

# Create tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL
)
""")

root = tkinter.Tk()

root.configure(bg='lightyellow')
root.title('To-Do List App')
root.geometry('350x350')

# Fetch tasks from the database
def fetch_tasks():
    cursor.execute("SELECT task_name FROM tasks")
    return [row[0] for row in cursor.fetchall()]

# Update the ListBox
def update_listbox():
    clear_listbox()
    for task in fetch_tasks():
        lb_tasks.insert("end", task)

def clear_listbox():
    lb_tasks.delete(0, "end")

def add_task():
    task = txt_input.get()
    if task != '':
        cursor.execute("INSERT INTO tasks (task_name) VALUES (%s)", (task,))
        db.commit()
        update_listbox()
        display['text'] = "Task added successfully!"
    else:
        display['text'] = "Please enter a task!"
    txt_input.delete(0, 'end')

def delete():
    task = lb_tasks.get('active')
    if task:
        cursor.execute("DELETE FROM tasks WHERE task_name = %s", (task,))
        db.commit()
        update_listbox()
        display['text'] = "Task deleted!"

def delete_all():
    cursor.execute("DELETE FROM tasks")
    db.commit()
    update_listbox()
    display['text'] = "All tasks deleted!"

def choose_random():
    tasks = fetch_tasks()
    if tasks:
        task = random.choice(tasks)
        display['text'] = f"Random Task: {task}"
    else:
        display['text'] = "No tasks available!"

def number_of_task():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    display['text'] = f"Number of tasks: {count}"

def exit_app():
    db.close()
    root.quit()

# Title
title = tkinter.Label(root, text="To-Do List App", font=("Arial", 16, "bold"), bg='lightyellow', pady=10)
title.pack()

# Input and Display
input_frame = tkinter.Frame(root, bg='lightyellow')
input_frame.pack(pady=10)

txt_input = tkinter.Entry(input_frame, width=25, font=("Arial", 12))
txt_input.grid(row=0, column=0, padx=5)

btn_add_task = tkinter.Button(input_frame, text="Add Task", width=10, bg='lightblue', fg='black', font=("Arial", 10), command=add_task)
btn_add_task.grid(row=0, column=1, padx=5)

display = tkinter.Label(root, text="", bg='lightyellow', font=("Arial", 10))
display.pack(pady=5)

# Listbox with Scrollbar
listbox_frame = tkinter.Frame(root, bg='lightyellow')
listbox_frame.pack(pady=10)

lb_tasks = tkinter.Listbox(listbox_frame, width=35, height=10, font=("Arial", 12), selectbackground="lightblue")
lb_tasks.pack(side="left", padx=(0, 10))

scrollbar = tkinter.Scrollbar(listbox_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

lb_tasks.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lb_tasks.yview)

# Buttons
btn_frame = tkinter.Frame(root, bg='lightyellow')
btn_frame.pack(pady=10)

btn_delete = tkinter.Button(btn_frame, text="Delete Task", width=15, bg='salmon', fg='black', font=("Arial", 10), command=delete)
btn_delete.grid(row=0, column=0, padx=5, pady=5)

btn_delete_all = tkinter.Button(btn_frame, text="Delete All", width=15, bg='red', fg='white', font=("Arial", 10), command=delete_all)
btn_delete_all.grid(row=0, column=1, padx=5, pady=5)

btn_choose_random = tkinter.Button(btn_frame, text="Choose Random", width=15, bg='lightgreen', fg='black', font=("Arial", 10), command=choose_random)
btn_choose_random.grid(row=1, column=0, padx=5, pady=5)

btn_number_of_task = tkinter.Button(btn_frame, text="Number of Tasks", width=15, bg='yellow', fg='black', font=("Arial", 10), command=number_of_task)
btn_number_of_task.grid(row=1, column=1, padx=5, pady=5)

btn_close = tkinter.Button(root, text="Exit", width=20, bg='gray', fg='white', font=("Arial", 10), command=exit_app)
btn_close.pack(pady=10)

# Initialize the ListBox
update_listbox()

root.mainloop()
