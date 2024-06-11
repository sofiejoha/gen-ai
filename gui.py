import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from S_to_T import *
from captions import *
from overall import *
from main import *

def summarize_video():
    """
    Summarizes a YouTube video based on the URL provided by the user.
    
    This function:
    - Retrieves the URL, number of sentences, selected model, and personality from the user.
    - Uses a callback function to update a progress bar and status message during the processing.
    - Calls the main function to generate the summary of the video.
    """
    
    # Get inputs from the user 
    youtube_link = entry.get()
    selected_model = model_var.get()
    personality = personality_var.get()
    
    app.update()  # Force immediate update
    
    # Function for updating the progress bar and message 
    def progress_callback(step, message):
        progress_bar['value'] = step
        processing_label.config(text=message)
        app.update()  # Force immediate update
    
    # Calling the main function to get the summary text 
    try:
        summary_text = main(youtube_link, selected_model, personality, progress_callback)
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
        app.update()  # Force immediate update

    
def clear_gui():
    """
    Clears all user inputs and resets the summary text box so that the user can input a new video.
    This button also works to clear the fields. 
    """
    entry.delete(0, tk.END)
    model_box.current(0)
    personality_box.current(0)
    summary_textbox.config(state=tk.NORMAL)
    summary_textbox.delete('1.0', tk.END)
    summary_textbox.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    processing_label.config(text="")
    
# Initialize the main application window 
app = ThemedTk(theme="arc")  # Use a modern theme
app.title('YouTube Summary Model')
app.configure(bg="#2b2b2b") # Set a darker background color for the window 

# Set the size of the main window: width to 1300 and height to 800
app.geometry("1300x800")

# Outer frame to center the inner frame
outer_frame = tk.Frame(app, bg="#2b2b2b")
outer_frame.grid(row=0, column=0, sticky="nsew")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Inner frame to hold the input widgets
frame = tk.Frame(outer_frame, bg="#2b2b2b", bd=5)
frame.grid(row=0, column=0, padx=350, pady=10, sticky="ew")
outer_frame.grid_columnconfigure(0, weight=1)

# YouTube entry: 
url_label = tk.Label(frame, text="YouTube link:", font=("Helvetica", 14), bg="#2b2b2b", fg="white")
url_label.grid(row=0, column=0, padx=5, pady=5)
entry = tk.Entry(frame, font=("Arial", 14))
entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry.configure(bg="white", fg="black")

# Choose model: 
model_var = tk.StringVar()
model_label = tk.Label(frame, text="Model:", font=("Helvetica", 14), bg="#2b2b2b", fg="white")
model_label.grid(row=1, column=0, padx=6, pady=5)
model_box = ttk.Combobox(frame, textvariable=model_var, font=("Arial", 14), state="readonly")
model_box['values'] = ("BLIP", "BLIP-2")
model_box.current(0)
model_box.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Choose personality: 
personality_var = tk.StringVar()
personality_label = tk.Label(frame, text="Personality:", font=("Helvetica", 14), bg="#2b2b2b", fg="white")
personality_label.grid(row=2, column=0, padx=6, pady=5)
personality_box = ttk.Combobox(frame, textvariable=personality_var, font=("Arial", 14), state="readonly")
personality_box['values'] = ("Professor", "Mafioso", "Kindergarten")
personality_box.current(0)
personality_box.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Summarize button:
button = ttk.Button(frame, text='Summarize', command=summarize_video)
button.grid(row=2, column=2, padx=5, pady=5)
frame.columnconfigure(1, weight=1)

# Clear button:
clear_button = ttk.Button(frame, text='Clear', command=clear_gui)
clear_button.grid(row=2, column=3, padx=5, pady=5)
frame.columnconfigure(1, weight=1)

# Processing message label
processing_label = tk.Label(frame, text="", font=("Arial", 14), bg="#2b2b2b", fg="white")
processing_label.grid(row=4, column=0, columnspan=3, padx=(50,0), pady=10, sticky="ew")

# Progress bar
progress_bar = ttk.Progressbar(frame, mode='determinate', maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, padx=(100,0), pady=10, sticky="ew")

# Frame for the summary textbox 
summary_frame = tk.Frame(app, bg="white", bd=5)
summary_frame.grid(row=1, column=0, padx=250, pady=20, sticky="nsew")  # Adjust row and padding values to position it higher

# Adding a scrollbar
scrollbar = tk.Scrollbar(summary_frame)
scrollbar.grid(row=0, column=1, sticky ='ns')

# Creating a text widget to display the summary text
summary_textbox = tk.Text(summary_frame, wrap='word', font=("Arial", 14), yscrollcommand=scrollbar.set, bg="white", fg="black", bd=5)
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

