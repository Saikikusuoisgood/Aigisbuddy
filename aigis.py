import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import random
import pyttsx3
import pygame
import os
import shutil
from moviepy.editor import VideoFileClip

class Aigis:
    def __init__(self, master):
        self.master = master
        master.title("AigisBuddy")
        master.iconbitmap(os.path.join(os.path.dirname(__file__), "aigisbuddy.ico"))

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
        self.button_remindme = tk.Button(master, text="Remind Me", command=self.remind_me)
        self.button_remindme.pack()

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.voice_var = tk.StringVar(master)
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

        # Music Control Buttons
        self.button_play_music = tk.Button(master, text="Play Music", command=self.play_music)
        self.button_play_music.pack()

        self.button_stop_music = tk.Button(master, text="Stop Music", command=self.stop_music)
        self.button_stop_music.pack()

        self.button_change_music = tk.Button(master, text="Change Music", command=self.change_music)
        self.button_change_music.pack()

        self.button_add_music = tk.Button(master, text="Add songs", command=self.add_music)
        self.button_add_music.pack()

        self.button_toggle_speech = tk.Button(master, text="shut it", command=self.toggle_speech_bubble)
        self.button_toggle_speech.pack()

        self.button_shakethatwindowforreal = tk.Button(master, text='Move aigis smoothly', command=self.shakethatwindowforreal)
        self.button_shakethatwindowforreal.pack()

        self.button_thefog = tk.Button(master, text='Surprise', command=self.thefog)
        self.button_thefog.pack()

        self.button_allout = tk.Button(master, text="ALL OUT ATTACK", command=self.gyattthismath, width=13, height=3, background='#f44336')
        
        self.button_exit = tk.Button(master, text="Exit", command=self.exit_application)
        self.button_exit.pack()

        self.music_paused = False
        self.music_changed = False
        self.current_music_index = 0
        self.movingfunction = self.move_window_randomly

        # Initialize pygame mixer
        pygame.mixer.init()
        self.current_music = os.path.abspath(os.path.join(os.path.dirname(__file__), "Media", "default_music.mp3"))
        self.play_music()

        # Create a label to display the GIF
        self.canvas = tk.Canvas(master, width=300, height=200)  # Create canvas
        self.canvas.pack()

        self.button_panpou = tk.Button(master, text="Panpou", command=self.panpou)

        # Load GIF frames
        gif_path = str(os.path.dirname(__file__)) + "\\vibin\\vibing-adachi.gif"
        gif = Image.open(gif_path)
        self.frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

        # Initialize the animated window
        self.window = tk.Toplevel(master)
        self.window.overrideredirect(1)  # Hide the window
        self.window.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window)

        self.window.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index = 0
        self.img = ImageTk.PhotoImage(self.frames[self.index])
        self.label = tk.Label(self.window, image=self.img, bg='#000000')  # Set background to white
        self.window.attributes('-transparentcolor','#000000')
        self.label.pack()

        # Create a speech window
        self.speech_window = tk.Toplevel(master)
        self.speech_window.overrideredirect(1)  # Hide the window border
        self.speech_window.geometry("150x50")  # Set the dimensions
        self.speech_window.attributes('-topmost', True)  # Set the window to always be on top

        self.speech_label = tk.Label(self.speech_window, text="", bg="white", bd=1, relief="solid", wraplength=180)
        self.speech_label.pack(fill=tk.BOTH, expand=True)  # Expand the label to fill the window

        gif_path2 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-yu.gif"
        gif2 = Image.open(gif_path2)
        self.frames2 = [frame2.copy() for frame2 in ImageSequence.Iterator(gif2)]        

        self.window2 = tk.Toplevel(master)
        self.window2.overrideredirect(1)  # Hide the window
        self.window2.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window2)

        self.window2.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index2 = 0
        self.img2 = ImageTk.PhotoImage(self.frames2[self.index2])
        self.label2 = tk.Label(self.window2, image=self.img2, bg='#000000')  # Set background to white
        self.window2.attributes('-transparentcolor','#000000')
        self.label2.pack()

        gif_path3 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-naoto.gif"
        gif3 = Image.open(gif_path3)
        self.frames3 = [frame3.copy() for frame3 in ImageSequence.Iterator(gif3)]        

        self.window3 = tk.Toplevel(master)
        self.window3.overrideredirect(1)  # Hide the window
        self.window3.geometry("%dx%d" % (98, 125))
        self.make_always_on_top(self.window3)

        self.window3.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index3 = 0
        self.img3 = ImageTk.PhotoImage(self.frames3[self.index3])
        self.label3 = tk.Label(self.window3, image=self.img3, bg='#000000')  # Set background to white
        self.window3.attributes('-transparentcolor','#000000')
        self.label3.pack()

        gif_path4 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-chie.gif"
        gif4 = Image.open(gif_path4)
        self.frames4 = [frame4.copy() for frame4 in ImageSequence.Iterator(gif4)]        

        self.window4 = tk.Toplevel(master)
        self.window4.overrideredirect(1)  # Hide the window
        self.window4.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window4)

        self.window4.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index4 = 0
        self.img4 = ImageTk.PhotoImage(self.frames4[self.index4])
        self.label4 = tk.Label(self.window4, image=self.img4, bg='#000000')  # Set background to white
        self.window4.attributes('-transparentcolor','#000000')
        self.label4.pack()

        gif_path5 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-yukiko.gif"
        gif5 = Image.open(gif_path5)
        self.frames5 = [frame5.copy() for frame5 in ImageSequence.Iterator(gif5)]        

        self.window5 = tk.Toplevel(master)
        self.window5.overrideredirect(1)  # Hide the window
        self.window5.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window5)

        self.window5.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index5 = 0
        self.img5 = ImageTk.PhotoImage(self.frames5[self.index5])
        self.label5 = tk.Label(self.window5, image=self.img5, bg='#000000')  # Set background to white
        self.window5.attributes('-transparentcolor','#000000')
        self.label5.pack()

        gif_path6 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-kanji.gif"
        gif6 = Image.open(gif_path6)
        self.frames6 = [frame6.copy() for frame6 in ImageSequence.Iterator(gif6)]        

        self.window6 = tk.Toplevel(master)
        self.window6.overrideredirect(1)  # Hide the window
        self.window6.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window6)

        self.window6.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index6 = 0
        self.img6 = ImageTk.PhotoImage(self.frames6[self.index6])
        self.label6 = tk.Label(self.window6, image=self.img6, bg='#000000')  # Set background to white
        self.window6.attributes('-transparentcolor','#000000')
        self.label6.pack()

        gif_path7 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-yosuke.gif"
        gif7 = Image.open(gif_path7)
        self.frames7 = [frame7.copy() for frame7 in ImageSequence.Iterator(gif7)]        

        self.window7 = tk.Toplevel(master)
        self.window7.overrideredirect(1)  # Hide the window
        self.window7.geometry("%dx%d" % (90, 109))
        self.make_always_on_top(self.window7)

        self.window7.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index7 = 0
        self.img7 = ImageTk.PhotoImage(self.frames7[self.index7])
        self.label7 = tk.Label(self.window7, image=self.img7, bg='#000000')  # Set background to white
        self.window7.attributes('-transparentcolor','#000000')
        self.label7.pack()

        gif_path8 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-teddie.gif"
        gif8 = Image.open(gif_path8)
        self.frames8 = [frame8.copy() for frame8 in ImageSequence.Iterator(gif8)]        

        self.window8 = tk.Toplevel(master)
        self.window8.overrideredirect(1)  # Hide the window
        self.window8.geometry("%dx%d" % (125, 94))
        self.make_always_on_top(self.window8)

        self.window8.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index8 = 0
        self.img8 = ImageTk.PhotoImage(self.frames8[self.index8])
        self.label8 = tk.Label(self.window8, image=self.img8, bg='#000000')  # Set background to white
        self.window8.attributes('-transparentcolor','#000000')
        self.label8.pack()

        gif_path9 = str(os.path.dirname(__file__)) + "\\vibin\\vibing-aigis.gif"
        gif9 = Image.open(gif_path9)
        self.frames9 = [frame9.copy() for frame9 in ImageSequence.Iterator(gif9)]        

        self.window9 = tk.Toplevel(master)
        self.window9.overrideredirect(1)  # Hide the window
        self.window9.geometry("%dx%d" % (gif.width, gif.height))
        self.make_always_on_top(self.window9)

        self.window9.bind("<Button-1>", self.stopstaringUnU)

        # Create a label to display the GIF
        self.index9 = 0
        self.img9 = ImageTk.PhotoImage(self.frames9[self.index9])
        self.label9 = tk.Label(self.window9, image=self.img9, bg='#000000')  # Set background to white
        self.window9.attributes('-transparentcolor','#000000')
        self.label9.pack()

        self.update_image()
        self.update_image2()
        self.update_image3()
        self.update_image4()
        self.update_image5()
        self.update_image6()
        self.update_image7()
        self.update_image8()
        self.update_image9()

        self.movingfunction(self.window)
        self.movingfunction(self.window2)
        self.movingfunction(self.window3)
        self.movingfunction(self.window4)
        self.movingfunction(self.window5)
        self.movingfunction(self.window6)
        self.movingfunction(self.window7)
        self.movingfunction(self.window8)
        self.movingfunction(self.window9)

        self.window.withdraw()
        self.window2.withdraw()
        self.window3.withdraw()
        self.window4.withdraw()
        self.window5.withdraw()
        self.window6.withdraw()
        self.window7.withdraw()
        self.window8.withdraw()

    def greet(self):
        name = simpledialog.askstring("Your Name", "What's your name?")
        if name:
            messagebox.showinfo("Greetings", f"I am the danger {name}")
        else:
            messagebox.showinfo("Greetings", "Why don't you give your name huh? you scared shadow")

    def compliment(self):
        compliments = [
            "You're the least hateable person I've encountered.",
            "Those who actually suceed in life, they just happen to be born with the magic ticket called talent, if you don't have it, you can either accept or deny that fact until you die, that your only choice.",
            "Kimi wa ne tashika ni ano toki watashi no subani ita",
            "You're incredibly intelligent!",
            "You have impeccable taste!"
        ]
        compliment = random.choice(compliments)
        messagebox.showinfo("Compliment", compliment)

    def tell_joke(self):
        jokes = [
            "You, narukami " + u'\U0001F602',
            "Ace detective ? More like, stupei ace defective " + u'\U0001F480',
            "https://www.reddit.com/r/OkBuddyPersona/",
            "Check it out i'm in the house like carpet",
            "I'm out of jokes"
        ]
        joke = random.choice(jokes)
        messagebox.showinfo("Joke", joke)

    def add_reminder(self):
        reminder = self.reminder_entry.get()
        if reminder:
            self.reminders.append(reminder)
            messagebox.showinfo("Reminder Added", f"Okay I'll remind you")
            self.reminder_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Reminder", "Please enter a reminder.")
    
    def remind_me(self):
        messagebox.showinfo('My bad dawg', "I forgor for real" + u'\U0001F480')

    def speak(self):
        text_to_speak = "Welcome back makotoes!"
        selected_voice = self.voice_var.get()
        selected_rate = self.rate_var.get()
        self.engine.setProperty('voice', selected_voice)
        self.engine.setProperty('rate', selected_rate)
        stickingout = pygame.mixer.Sound(str(os.path.dirname(__file__)) + "\\Media\\gyattaigis.wav")
        stickingout.play()
        self.engine.runAndWait()

    def open_calculator(self):
        calculator_window = tk.Toplevel(self.master)
        calculator_window.title("Calculator")

        def calculate():
            messagebox.showinfo("Calculation:", "21")

        entry = tk.Entry(calculator_window)
        entry.pack()

        calculate_button = tk.Button(calculator_window, text="Calculate", command=calculate)
        calculate_button.pack()

        result_label = tk.Label(calculator_window, text="")
        result_label.pack()

    def save_note(self):
        note_text = self.note_entry.get("1.0", tk.END)
        self.notes += note_text
        messagebox.showinfo("Note Saved", "I ain't saving your notes fool!")

    def panpou(self):
        pass # we don't talk about the panpou function

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
        pygame.mixer.music.pause()

    def change_music(self):
        pygame.mixer.music.stop()  # Stop the currently playing music

        # List of music filenames
        with open(str(os.path.dirname(__file__)) + "\\musicpypypy.txt", "r") as file:
            # Read the lines and strip newline characters
            lines = file.readlines()
            # Convert each line to an integer and store in a list
            music_files = [str(line.strip()) for line in lines]

        # Increment the index to select the next music track
        self.current_music_index = (self.current_music_index + 1) % len(music_files)
    
        # Set the current music filename
        self.current_music = str(os.path.dirname(__file__)) + "\\Media\\" + music_files[self.current_music_index]

        # Load and play the new music
        pygame.mixer.music.load(self.current_music)
        pygame.mixer.music.play(-1)  # -1 loops indefinitely

    def add_music(self):
        greatvegetables = filedialog.askopenfilename(filetypes=([("Music files", "*.mp3;*.adachi;*.opus;*.flac;*.wav;*.m4a;*.wma;*.aac"),("All files", "*.*")]))
        if greatvegetables:
            with open(str(os.path.dirname(__file__)) + "\\musicpypypy.txt", "a") as cabbage:
                cabbage.write(os.path.basename(greatvegetables) + '\n')
            shutil.copy(greatvegetables, str(os.path.dirname(__file__)) + "\\Media")

    def exit_application(self):
        pygame.mixer.music.stop()
        self.master.quit()

    def update_image(self):
        self.index = (self.index + 1) % len(self.frames)
        self.img = ImageTk.PhotoImage(self.frames[self.index])
        self.label.config(image=self.img)
        self.label.after(50, self.update_image)
    
    def update_image2(self):
        self.index2 = (self.index2 + 1) % len(self.frames2)
        self.img2 = ImageTk.PhotoImage(self.frames2[self.index2])
        self.label2.config(image=self.img2)
        self.label2.after(50, self.update_image2)

    def update_image3(self):
        self.index3 = (self.index3 + 1) % len(self.frames3)
        self.img3 = ImageTk.PhotoImage(self.frames3[self.index3])
        self.label3.config(image=self.img3)
        self.label3.after(50, self.update_image3)

    def update_image4(self):
        self.index4 = (self.index4 + 1) % len(self.frames4)
        self.img4 = ImageTk.PhotoImage(self.frames4[self.index4])
        self.label4.config(image=self.img4)
        self.label4.after(50, self.update_image4)

    def update_image5(self):
        self.index5 = (self.index5 + 1) % len(self.frames5)
        self.img5 = ImageTk.PhotoImage(self.frames5[self.index5])
        self.label5.config(image=self.img5)
        self.label5.after(50, self.update_image5)

    def update_image6(self):
        self.index6 = (self.index6 + 1) % len(self.frames6)
        self.img6 = ImageTk.PhotoImage(self.frames6[self.index6])
        self.label6.config(image=self.img6)
        self.label6.after(50, self.update_image6)

    def update_image7(self):
        self.index7 = (self.index7 + 1) % len(self.frames7)
        self.img7 = ImageTk.PhotoImage(self.frames7[self.index7])
        self.label7.config(image=self.img7)
        self.label7.after(50, self.update_image7)

    def update_image8(self):
        self.index8 = (self.index8 + 1) % len(self.frames8)
        self.img8 = ImageTk.PhotoImage(self.frames8[self.index8])
        self.label8.config(image=self.img8)
        self.label8.after(50, self.update_image8)

    def update_image9(self):
        self.index9 = (self.index9 + 1) % len(self.frames9)
        self.img9 = ImageTk.PhotoImage(self.frames9[self.index9])
        self.label9.config(image=self.img9)
        self.label9.after(50, self.update_image9)

    def make_always_on_top(self, window):
        window.attributes('-topmost', True)

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
            "What's good?",
            "Bitches and whores",
            "I will mass destruction your ass",
            "Consider killing yourself",
            "Very rizzful",
            "Don't click me!!"
        ]
        random_text = random.choice(speech_texts)

        self.speech_label.config(text=random_text)

        window.after(2000, self.move_window_randomly, window)

    def teleport_window_randomly(self, window, num_steps=20):
        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        def move_step(target_x, target_y, step_count):
            # Calculate the distance to move in each direction for this step
            dx = (target_x - window.winfo_x()) / num_steps
            dy = (target_y - window.winfo_y()) / num_steps

            # Move the window by the calculated amount
            new_x = window.winfo_x() + dx
            new_y = window.winfo_y() + dy
            window.geometry(f"+{int(new_x)}+{int(new_y)}")
            nanako = new_x + 100
            kamoshida = new_y - 30

            # Move the speech bubble window to the same position as the main window
            self.speech_window.geometry(f"+{int(nanako)}+{int(kamoshida)}")

            # If not the final step, schedule the next step
            if step_count < num_steps:
                window.after(50, move_step, target_x, target_y, step_count + 1)

        def move():
            # Generate random target coordinates for the window
            target_x = random.randint(0, screen_width - window.winfo_reqwidth())
            target_y = random.randint(0, screen_height - window.winfo_reqheight())

            # Start moving the window towards the target coordinates
            move_step(target_x, target_y, 0)

            # Generate random text for the speech bubble
            speech_texts = [
                "Hello!",
                "What's good ?",
                "Bitches And Whores.",
                "I will mass destruction your ass",
                "Consider killing yourself",
                "Very rizzful",
                "Don't click me!!"
            ]
            random_text = random.choice(speech_texts)
            self.speech_label.config(text=random_text)

            # Schedule the next move
            window.after(2000, move)

        # Start moving the window
        move()
    
    def toggle_speech_bubble(self):
        if self.speech_window.state() == "normal":
            self.speech_window.withdraw()
        else:
            self.speech_window.deiconify()
    
    def shakethatwindowforreal(self):
        if self.movingfunction == self.move_window_randomly:
            self.movingfunction = self.teleport_window_randomly
        else:
            self.movingfunction = self.move_window_randomly

        self.movingfunction(self.window)

    def stopstaringUnU(self, event=None):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 640
        window_height = 480
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        pygame.mixer_music.stop()
        pygame.mixer_music.load(str(os.path.dirname(__file__)) + "\\Media\\dw.wav")
        pygame.mixer_music.play()
        image_window = tk.Toplevel()
        image_window.title("")
        image_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        image_window.overrideredirect(1)
        image_path = (str(os.path.dirname(__file__)) + "\\Media\\sddefault.jpg")
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image_window, image=photo)
        label.image = photo
        label.pack()
        image_window.after(5000, image_window.destroy)

    def thefog(self):
        video_window = tk.Toplevel()
        video_window.title("")
        video_window.geometry(f"{700}x{480}+{(self.master.winfo_screenwidth() - 700) // 2}+{(self.master.winfo_screenheight() - 480) // 2}")
        video_window.overrideredirect(1)
        VideoPlayer(video_window, video_path=str(os.path.dirname(__file__)) + "\\Media\\ADACHI.mp4", width=700, height=480)
        adacheese = pygame.mixer.Sound(str(os.path.dirname(__file__)) + "\\Media\\ALLOUTATTACK.mp3")
        adacheese.set_volume(1)
        adacheese.play()
        self.window9.withdraw()
        self.window.deiconify()
        self.window2.deiconify()
        self.button_allout.pack()
        self.button_allout.place(x=50, y=50)
        self.toggle_speech_bubble()
        self.master.update()
        pygame.mixer_music.stop()
        pygame.mixer_music.load(str(os.path.dirname(__file__)) + "\\Media\\Thefogp4dSTART.wav")
        pygame.mixer_music.play(-1) #hides aigis and shows adcheese and yu narukami

    def alloutattack(self):
        self.window9.deiconify()
        self.window3.deiconify()
        self.window4.deiconify()
        self.window5.withdraw()
        self.window6.deiconify()
        self.window7.deiconify()
        self.window8.deiconify() # shows all the hidden windows
        self.toggle_speech_bubble()

    def update_video(self):
        self.video_path = (str(os.path.dirname(__file__)) + "\\Media\\ALLOUTATTACK.mp4")
        self.widthz = 700
        self.heightz = 480

        self.video_clip = VideoFileClip(self.video_path)
        self.duration = self.video_clip.duration

        self.current_time = 0
        frame = self.video_clip.get_frame(self.current_time)
        frame = Image.fromarray(frame)

        frame = frame.resize((self.widthz, self.heightz))
        frame = ImageTk.PhotoImage(frame)

        self.label.configure(image=frame)
        self.label.image = frame

        if self.current_time < self.duration:
            self.current_time += 0.04  # Increment by 40 milliseconds (25 frames per second)
            self.master.after(40, self.update_video)
        else:
            self.master.destroy()

    def gyattthismath(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 700
        window_height = 480
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        ggg = pygame.mixer.Sound(str(os.path.dirname(__file__)) + "\\Media\\ALLOUTATTACK.mp3")
        ggg.set_volume(1)
        ggg.play()
        video_window = tk.Toplevel()
        video_window.title("")
        video_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        video_window.overrideredirect(1)
        self.video_window = video_window
        video_path = (str(os.path.dirname(__file__)) + "\\Media\\ALLOUTATTACK.mp4")
        VideoPlayer(video_window, video_path, window_width, window_height)
        self.alloutattack()

class VideoPlayer:
    def __init__(self, master, video_path, width, height):
        self.master = master
        self.video_path = video_path
        self.width = width
        self.height = height

        self.video_clip = VideoFileClip(self.video_path)
        self.duration = self.video_clip.duration

        self.label = tk.Label(master)
        self.label.pack()

        self.current_time = 0
        self.update_video()

    def update_video(self):
        frame = self.video_clip.get_frame(self.current_time)
        frame = Image.fromarray(frame)

        frame = frame.resize((self.width, self.height))
        frame = ImageTk.PhotoImage(frame)

        self.label.configure(image=frame)
        self.label.image = frame

        if self.current_time < self.duration:
            self.current_time += 0.04  # Increment by 40 milliseconds (25 frames per second)
            self.master.after(40, self.update_video)
        else:
            self.master.destroy()

def main():
    root = tk.Tk()
    aigis = Aigis(root)
    root.mainloop()

if __name__ == "__main__":
    main()
