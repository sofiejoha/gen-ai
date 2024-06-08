import tkinter as tk
from tkinter import ttk
from S_to_T import *
from captions import *
from overall import *
from main import *

def summarize_video():
    """
    Summarizes a YouTube video based on the URL provided by the user.
    
    This function:
    - Retrieves the URL, number of sentenecs, and selected model from the user. 
    - Uses a callback function to update a progess bar and status message during the processing. 
    - Calls the main function to generate the summary of the video.
    """
    
    # Get inputs from the user 
    youtube_link = entry.get()
    sentences_num = entry_sen.get()
    selected_model = model_var.get()
    
    app.update_idletasks()
    
    # Function for updating the progress bar and message 
    def progress_callback(step, message):
        progress_bar['value'] = step
        processing_label.config(text=message)
        app.update_idletasks()
    
    # Calling the main function to get the summary text 
    try:
        summary_text = main(youtube_link, selected_model, progress_callback)
        summary_textbox.config(state=tk.NORMAL) # Enable the summary text box to allow editing 
        summary_textbox.delete('1.0', tk.END)  # Clear any previous text
        summary_textbox.insert(tk.END, summary_text) # Insert the new summary text into the text box 
        summary_textbox.config(state=tk.DISABLED) # Making the textbox read-only 
    
    # If an error occurs during summarization, handle it here:
    except Exception as e:
        summary_textbox.config(state=tk.NORMAL)
        summary_textbox.delete('1.0', tk.END)
        summary_textbox.insert(tk.END, f"Error summarizing video: {e}")
        summary_textbox.config(state=tk.DISABLED)
    finally:
        # Ensure that the progress bar is set to 100% when done 
        progress_bar['value'] = 100
        processing_label.config(text="Summary completed!")
    

def validate_int(input):
    if input.isdigit() or input == "":
        return True
    else:
        return False
    
# Initialize the main application window 
app = tk.Tk() 
app.title('YouTube Summary Model')
app.configure(bg="#80c1ff") # Set background color for the window 

# Set the size of the main window: width to 1300 and height to 800
app.geometry("1300x800")

# Outer frame to center the inner frame
outer_frame = tk.Frame(app, bg="#80c1ff")
outer_frame.grid(row=0, column=0, sticky="nsew")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Inner frame to hold the input widgets
frame = tk.Frame(outer_frame, bg="#80c1ff", bd=5)
frame.grid(row=0, column=0, padx=350, pady=10, sticky="ew")
outer_frame.grid_columnconfigure(0, weight=1)

# YouTube entry: 
url_label = tk.Label(frame, text="YouTube link:", font=("Arial", 14), bg="#80c1ff")
url_label.grid(row=0, column=0, padx=5, pady=5)
entry = tk.Entry(frame, font=("Arial", 14))
entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Number of sentences entry: 
sentences_label = tk.Label(frame, text="Number of sentences:", font=("Arial", 14), bg="#80c1ff")
sentences_label.grid(row=1, column=0, padx=6, pady=5)
validate_command = app.register(validate_int)
entry_sen = tk.Entry(frame, font=("Arial", 14), validate="key", validatecommand=(validate_command, '%P'))
entry_sen.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Choose model: 
model_var = tk.StringVar()
model_label = tk.Label(frame, text="Model:", font=("Arial", 14), bg="#80c1ff").grid(row=2, column=0, padx=6, pady=5)
model_box = ttk.Combobox(frame, textvariable=model_var, font=("Arial", 14), state="readonly")
model_box['values'] = ("blip", "blip2")
model_box.current(0)
model_box.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Summarize button:
button = tk.Button(frame, text='Summarize', font=40, command=summarize_video)
button.grid(row=2, column=2, padx=5, pady=5)
frame.columnconfigure(1, weight=1)

# Processing message label
processing_label = tk.Label(frame, text="", font=("Arial", 14), bg="#80c1ff", fg="blue")
processing_label.grid(row=3, column=0, columnspan=3, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(frame, mode='determinate', maximum=100)
progress_bar.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

# Frame for the summary textbox 
summary_frame = tk.Frame(app, bg="white", bd=5)
summary_frame.grid(row=1, column=0, padx=250, pady=20, sticky="nsew")  # Adjust row and padding values to position it higher

# Adding a scrollbar
scrollbar = tk.Scrollbar(summary_frame)
scrollbar.grid(row=0, column=1, sticky='ns')

# Creating a text widget to display the summary text
summary_textbox = tk.Text(summary_frame, wrap='word', font=("Arial", 14), yscrollcommand=scrollbar.set, bg="white", bd=5)
summary_textbox.grid(row=0, column=0, padx=3, pady=5, sticky="nsew")
scrollbar.config(command=summary_textbox.yview)
summary_textbox.config(state=tk.DISABLED)

# Configure the column and row weights for the summary frame to allow expanding
summary_frame.grid_columnconfigure(0, weight=1)
summary_frame.grid_rowconfigure(0, weight=1)

# Configure the grid weights to make the GUI responsive
app.grid_rowconfigure(1, weight=5)
app.grid_columnconfigure(0, weight=1)

# Run the application main loop
app.mainloop()
