import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox
import random
import pyttsx3
import pygame

class Aigis:
    def __init__(self, master):
        self.master = master
        master.title("Aigis")

        self.label = tk.Label(master, text="Welcome back!")
        self.label.pack()

        self.button_greet = tk.Button(master, text="Greet Me", command=self.greet)
        self.button_greet.pack()

        self.button_compliment = tk.Button(master, text="Compliment", command=self.compliment)
        self.button_compliment.pack()

        self.button_joke = tk.Button(master, text="Tell a Joke", command=self.tell_joke)
        self.button_joke.pack()

        self.reminders = []
        self.reminder_entry = tk.Entry(master)
        self.reminder_entry.pack()
        self.button_add_reminder = tk.Button(master, text="Add Reminder", command=self.add_reminder)
        self.button_add_reminder.pack()

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.voice_var = tk.StringVar(master)
        self.voice_var.set(self.voices[0].id)  # Default voice
        self.voice_dropdown = tk.OptionMenu(master, self.voice_var, *[voice.name for voice in self.voices])
        self.voice_dropdown.pack()

        self.rate_var = tk.DoubleVar(master)
        self.rate_var.set(150)  # Default speech rate
        self.rate_scale = tk.Scale(master, from_=100, to=300, orient=tk.HORIZONTAL, label="Speech Rate", variable=self.rate_var)
        self.rate_scale.pack()

        self.button_speak = tk.Button(master, text="Speak", command=self.speak)
        self.button_speak.pack()

        self.button_calculator = tk.Button(master, text="Calculator", command=self.open_calculator)
        self.button_calculator.pack()

        self.notes = ""
        self.note_entry = tk.Text(master, height=5, width=30)
        self.note_entry.pack()
        self.button_save_note = tk.Button(master, text="Save Note", command=self.save_note)
        self.button_save_note.pack()

        self.button_exit = tk.Button(master, text="Exit", command=self.exit_application)
        self.button_exit.pack()

        # Music Control Buttons
        self.button_play_music = tk.Button(master, text="Play Music", command=self.play_music)
        self.button_play_music.pack()

        self.button_stop_music = tk.Button(master, text="Stop Music", command=self.stop_music)
        self.button_stop_music.pack()

        self.button_change_music = tk.Button(master, text="Change Music", command=self.change_music)
        self.button_change_music.pack()

        self.button_toggle_speech = tk.Button(master, text="pourrais-tu fermer ta bouche ma jolie ^^", command=self.toggle_speech_bubble)
        self.button_toggle_speech.pack()

        self.music_paused = False
        self.music_changed = False
        self.current_music_index = 0  # Start with the first music track

        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_music = "default_music.mp3"
        self.play_music()

        # Create a label to display the GIF
        self.canvas = tk.Canvas(master, width=300, height=200)  # Create canvas
        self.canvas.pack()

        self.button_panpou = tk.Button(master, text="Panpou", command=self.panpou)
        self.button_panpou.pack()

        # Load GIF frames
        gif_path = "vibing-aigis.gif"
        gif = Image.open(gif_path)
        self.frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

        # Initialize the animated window
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(1)  # Hide the window
        self.window.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window)

        # Create a label to display the GIF
        self.index = 0
        self.img = ImageTk.PhotoImage(self.frames[self.index])
        self.label = tk.Label(self.window, image=self.img, bg='#000000')  # Set background to white
        self.window.attributes('-transparentcolor','#000000')
        self.label.pack()

        # Create a speech window
        self.speech_window = tk.Toplevel(master)
        self.speech_window.overrideredirect(1)  # Hide the window border
        self.speech_window.geometry("100x50")  # Set the dimensions
        self.speech_window.attributes('-topmost', True)  # Set the window to always be on top

        self.speech_label = tk.Label(self.speech_window, text="", bg="white", bd=1, relief="solid", wraplength=180)
        self.speech_label.pack(fill=tk.BOTH, expand=True)  # Expand the label to fill the window

        # Start updating the image
        self.update_image()

        # Start moving the window randomly
        self.move_window_randomly(self.window)

    def greet(self):
        name = messagebox.askstring("Your Name", "What's your name?")
        if name:
            messagebox.showinfo("Greetings", f"Hello {name}! How can I assist you today?")
        else:
            messagebox.showinfo("Greetings", "Hello! How can I assist you today?")

    def compliment(self):
        compliments = [
            "You're looking great today!",
            "You have a wonderful smile!",
            "You always bring positivity to the room!",
            "You're incredibly intelligent!",
            "You have impeccable taste!"
        ]
        compliment = random.choice(compliments)
        messagebox.showinfo("Compliment", compliment)

    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It's a shame they'll never meet.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "I'm reading a book on anti-gravity. It's impossible to put down!"
        ]
        joke = random.choice(jokes)
        messagebox.showinfo("Joke", joke)

    def add_reminder(self):
        reminder = self.reminder_entry.get()
        if reminder:
            self.reminders.append(reminder)
            messagebox.showinfo("Reminder Added", f"Reminder '{reminder}' added successfully!")
            self.reminder_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Reminder", "Please enter a reminder.")

    def speak(self):
        text_to_speak = "Welcome back makotoes!"
        selected_voice = self.voice_var.get()
        selected_rate = self.rate_var.get()
        self.engine.setProperty('voice', selected_voice)
        self.engine.setProperty('rate', selected_rate)
        self.engine.say(text_to_speak)
        self.engine.runAndWait()

    def open_calculator(self):
        calculator_window = tk.Toplevel(self.master)
        calculator_window.title("Calculator")

        def calculate():
            expression = entry.get()
            try:
                result = eval(expression)
                result_label.config(text=f"Result: {result}")
            except Exception as e:
                result_label.config(text="Error!")

        entry = tk.Entry(calculator_window)
        entry.pack()

        calculate_button = tk.Button(calculator_window, text="Calculate", command=calculate)
        calculate_button.pack()

        result_label = tk.Label(calculator_window, text="")
        result_label.pack()

    def save_note(self):
        note_text = self.note_entry.get("1.0", tk.END)
        self.notes += note_text
        messagebox.showinfo("Note Saved", "Note saved successfully!")

    def panpou(self):
        panpous = [
            "Will you forget me someday...?",
            "am I... real for you..?",
            "I love you panpou",
            "Do you love me ?",
            "Never leave me"
        ]
        panpou = random.choice(panpous)
        messagebox.showinfo("Aigis", panpou)

    def play_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.current_music)
            pygame.mixer.music.play(-1)  # -1 loops indefinitely
        else:
            if self.music_paused:
                pygame.mixer.music.unpause()
                self.music_paused = False
            else:
                pygame.mixer.music.pause()
                self.music_paused = True

    def stop_music(self):
        pygame.mixer.music.stop()

    def change_music(self):
        pygame.mixer.music.stop()  # Stop the currently playing music

        # List of music filenames
        music_files = ["default_music.mp3", "alternative_music.mp3", "iwotodaidormp3r.mp3", "iwotodaidormp3.mp3"]

        # Increment the index to select the next music track
        self.current_music_index = (self.current_music_index + 1) % len(music_files)
    
        # Set the current music filename
        self.current_music = music_files[self.current_music_index]

        # Load and play the new music
        pygame.mixer.music.load(self.current_music)
        pygame.mixer.music.play(-1)  # -1 loops indefinitely


    def exit_application(self):
        pygame.mixer.music.stop()
        self.master.quit()

    def update_image(self):
        self.index = (self.index + 1) % len(self.frames)
        self.img = ImageTk.PhotoImage(self.frames[self.index])
        self.label.config(image=self.img)
        self.label.after(50, self.update_image)

    def make_always_on_top(self, window):
        window.attributes('-topmost', True)  # Set the window as topmost

    def move_window_randomly(self, window):
        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Generate random coordinates for the window
        x = random.randint(0, screen_width - window.winfo_reqwidth())
        y = random.randint(0, screen_height - window.winfo_reqheight())
        gyatt = 100 + x
        rizz = y - 30
        

        # Move the window to the random coordinates
        window.geometry(f"+{x}+{y}")

        # Move the speech bubble window to the same random coordinates
        self.speech_window.geometry(f"+{gyatt}+{rizz}")

        # Generate random text for the speech bubble
        speech_texts = [
            "Hello!",
            "How can I help you?",
            "Nice weather today!",
            "What's on your mind?",
            "I'm here to assist you!",
            "I love you"
        ]
        random_text = random.choice(speech_texts)

        # Update speech bubble text
        self.speech_label.config(text=random_text)

        # Schedule the next movement after a certain interval (in milliseconds)
        window.after(2000, self.move_window_randomly, window)  # Change 2000 to adjust the interval in milliseconds
    
    def toggle_speech_bubble(self):
        if self.speech_window.state() == "normal":
            self.speech_window.withdraw()  # Hide the speech window
        else:
            self.speech_window.deiconify()  # Show the speech window
    
    def apply_alpha(self, widget, alpha):
        # Get the current background color of the widget
        current_color = widget.cget("background")

        # Check if the current color is white
        if current_color.lower() == "white":
            # Apply the alpha value to the widget's background color
            widget.attributes('-alpha', alpha)

def main():
    root = tk.Tk()
    aigis = Aigis(root)
    root.mainloop()

if __name__ == "__main__":
    main()
