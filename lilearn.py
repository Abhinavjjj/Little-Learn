import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import itertools
from nltk import word_tokenize, pos_tag
import pygame
from gtts import gTTS
import tempfile
import os
from pygame import mixer
mixer.init()

import sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def play_mp3(filepath):
    stop_audio()
    try:
        mixer.music.load(filepath)
        mixer.music.play()
    except Exception as e:
        print("Error playing MP3:", e)

def stop_audio():
    mixer.music.stop()




def play_text_audio(text):
    try:
        # Stop any currently playing audio
        stop_audio()

        # Generate temporary MP3 file
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Optional: Delete the temp file after playing finishes
        def remove_temp():
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            os.remove(temp_path)

        # Start cleanup in the background
        import threading
        threading.Thread(target=remove_temp, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Audio Error", f"Could not play audio: {e}")





# Helper function to create colored buttons with hover effect
def create_colored_button(parent, text, command=None, width=200, height=50, radius=20,
                          bg="#546E7A", fg="white", hover_bg="#455A64", padx=10, pady=5,
                          font=("Segoe UI", 18, "bold")):
    class RoundedButton(tk.Canvas):
        def __init__(self):
            super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent['bg'])
            self.radius = radius
            self.command = command
            self.bg = bg
            self.fg = fg
            self.hover_bg = hover_bg
            self.text = text

            self.shadow = self.create_rounded_rect(4, 4, width, height, radius, fill="#999999")
            self.button = self.create_rounded_rect(0, 0, width-4, height-4, radius, fill=bg)
            self.label = self.create_text(width//2 - 2, height//2 - 2, text=text, fill=fg, font=font)

            # Bind only to the whole canvas, not to individual items
            self.bind("<Button-1>", self._on_click)

            # Hover bindings can stay on items if needed
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.tag_bind(self.button, "<Enter>", self._on_enter)
            self.tag_bind(self.label, "<Enter>", self._on_enter)
            self.tag_bind(self.button, "<Leave>", self._on_leave)
            self.tag_bind(self.label, "<Leave>", self._on_leave)

            self.pack(padx=padx, pady=pady)


        def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
            points = [
                x1+r, y1,
                x2-r, y1,
                x2, y1,
                x2, y1+r,
                x2, y2-r,
                x2, y2,
                x2-r, y2,
                x1+r, y2,
                x1, y2,
                x1, y2-r,
                x1, y1+r,
                x1, y1,
            ]
            return self.create_polygon(points, smooth=True, **kwargs)

        def _on_click(self, event):
            if self.command:
                self.command()

        def _on_enter(self, event):
            self.itemconfig(self.button, fill=self.hover_bg)

        def _on_leave(self, event):
            self.itemconfig(self.button, fill=self.bg)

    return RoundedButton()

translations = {
    'en': {"prev": "<< Previous", "next": "Next >>", "back": "⬅ Back", "speak": "🔊 Speak"},
    'ml': {"prev": "<< മുമ്പേത്", "next": "അടുത്തത് >>", "back": "⬅ പിന്നേയ്ക്ക്", "speak": "🔊 കേൾക്കൂ"},
    'hi': {"prev": "<< पिछला", "next": "अगला >>", "back": "⬅ वापिस", "speak": "🔊 सुनो"},
    'ta': {"prev": "<< முந்தையது", "next": "அடுத்தது >>", "back": "⬅ பின்", "speak": "🔊 கேள்"},
    'te': {"prev": "<< మునుపటి", "next": "తర్వాత >>", "back": "⬅ వెనక్కి", "speak": "🔊 విని"},
    'kn': {"prev": "<< ಹಿಂದಿನದು", "next": "ಮುಂದಿನದು >>", "back": "⬅ ಹಿಂದುಮುಂದಾಗಿ", "speak": "🔊 ಕೇಳಿ"},
}

translations1 = {
    'en': {
        "prev": "<< Previous", "next": "Next >>", "back": "⬅ Back",
        "listen": "🔊 Listen",
        "basic_grammar": "📚 Basic Grammar Study",
        "grammar_analyzer": "📝 Grammar Analyzer",
        "analyze": "✔ Analyze",
        "grammar_options": "Grammar Options",
        "enter_sentence": "Type a sentence to analyze parts of speech:",
        "warning_empty": "Please enter a sentence.",
    },
    'ml': {
        "prev": "<< മുമ്പേത്", "next": "അടുത്തത് >>", "back": "⬅ പിന്നേയ്ക്ക്",
        "listen": "🔊 കേൾക്കൂ",
        "basic_grammar": "📚 അടിസ്ഥാന വ്യാകരണം പഠനം",
        "grammar_analyzer": "📝 വ്യാകരണ വിശകലനം",
        "analyze": "✔ വിശകലനം ചെയ്യുക",
        "grammar_options": "വ്യാകരണ ഓപ്ഷനുകൾ",
        "enter_sentence": "വാക്യം ടൈപ്പുചെയ്യുക:",
        "warning_empty": "ദയവായി ഒരു വാക്യം നൽകുക.",
    },
    'hi': {
        "prev": "<< पिछला", "next": "अगला >>", "back": "⬅ वापस",
        "listen": "🔊 सुनो",
        "basic_grammar": "📚 मूल व्याकरण अध्ययन",
        "grammar_analyzer": "📝 व्याकरण विश्लेषक",
        "analyze": "✔ विश्लेषण करें",
        "grammar_options": "व्याकरण विकल्प",
        "enter_sentence": "भागों का विश्लेषण करने के लिए वाक्य लिखें:",
        "warning_empty": "कृपया एक वाक्य दर्ज करें।",
    },
    'ta': {
        "prev": "<< முந்தையது", "next": "அடுத்தது >>", "back": "⬅ பின் செல்ல",
        "listen": "🔊 கேள்",
        "basic_grammar": "📚 அடிப்படை இலக்கணம் பயிற்சி",
        "grammar_analyzer": "📝 இலக்கணம் பகுப்பாய்வு",
        "analyze": "✔ பகுப்பாய்வு செய்",
        "grammar_options": "இலக்கணம் விருப்பங்கள்",
        "enter_sentence": "பகுப்பாய்விற்காக ஒரு வாக்கியம் தட்டச்சு செய்க:",
        "warning_empty": "தயவு செய்து ஒரு வாக்கியம் உள்ளிடவும்.",
    },
    'te': {
        "prev": "<< మునుపటి", "next": "తరువాత >>", "back": "⬅ వెనక్కి",
        "listen": "🔊 వినండి",
        "basic_grammar": "📚 ప్రాథమిక వ్యాకరణ అధ్యయనం",
        "grammar_analyzer": "📝 వ్యాకరణ విశ్లేషణ",
        "analyze": "✔ విశ్లేషించు",
        "grammar_options": "వ్యాకరణ ఎంపికలు",
        "enter_sentence": "భాగాలను విశ్లేషించడానికి వాక్యం టైప్ చేయండి:",
        "warning_empty": "దయచేసి ఒక వాక్యం నమోదు చేయండి.",
    },
    'kn': {
        "prev": "<< ಹಿಂದಿನದು", "next": "ಮುಂದಿನದು >>", "back": "⬅ ಹಿಂದಕ್ಕೆ",
        "listen": "🔊 ಕೇಳಿ",
        "basic_grammar": "📚 ಮೂಲ ವ್ಯಾಕರಣ ಅಧ್ಯಯನ",
        "grammar_analyzer": "📝 ವ್ಯಾಕರಣ ವಿಶ್ಲೇಷಣೆ",
        "analyze": "✔ ವಿಶ್ಲೇಷಿಸಿ",
        "grammar_options": "ವ್ಯಾಕರಣ ಆಯ್ಕೆಗಳು",
        "enter_sentence": "ವಾಕ್ಯವನ್ನು ಟೈಪ್ ಮಾಡಿ ಭಾಗಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ:",
        "warning_empty": "ದಯವಿಟ್ಟು ಒಂದು ವಾಕ್ಯವನ್ನು ನಮೂದಿಸಿ.",
    }
}

translation2 = {
    "en": {
        "title": "📖 Select a Story",
        "open_story": "📖 Open Story",
        "back": "⬅ Back",
        "listen": "🔊 Listen",
        "warning": "Please select a story.",
    },
    "ml": {
        "title": "📖 ഒരു കഥ തിരഞ്ഞെടുക്കുക",
        "open_story": "📖 കഥ തുറക്കുക",
        "back": "⬅ പിൻവലിക്കുക",
        "listen": "🔊 കേൾക്കുക",
        "warning": "ദയവായി ഒരു കഥ തിരഞ്ഞെടുക്കുക.",
    },
    "hi": {
        "title": "📖 एक कहानी चुनें",
        "open_story": "📖 कहानी खोलें",
        "back": "⬅ वापस",
        "listen": "🔊 सुनें",
        "warning": "कृपया एक कहानी चुनें।",
    },
    "ta": {
        "title": "📖 ஒரு கதை தேர்ந்தெடுக்கவும்",
        "open_story": "📖 கதையை திறக்கவும்",
        "back": "⬅ திரும்பிச் செல்",
        "listen": "🔊 கேளுங்கள்",
        "warning": "தயவுசெய்து ஒரு கதையைத் தேர்ந்தெடுக்கவும்.",
    },
    "te": {
        "title": "📖 కథను ఎంచుకోండి",
        "open_story": "📖 కథ తెరవండి",
        "back": "⬅ వెనక్కి",
        "listen": "🔊 వినండి",
        "warning": "దయచేసి ఒక కథను ఎంచుకోండి.",
    },
    "kn": {
        "title": "📖 ಕಥೆ ಆಯ್ಕೆಮಾಡಿ",
        "open_story": "📖 ಕಥೆ ತೆರೆದುಕೊಳ್ಳಿ",
        "back": "⬅ ಹಿಂದಕ್ಕೆ",
        "listen": "🔊 ಕೇಳಿ",
        "warning": "ದಯವಿಟ್ಟು ಒಂದು ಕಥೆ ಆಯ್ಕೆಮಾಡಿ.",
    }
}

translation3 = {
    "en": {
        "title": "Select a Rhyme",
        "play": "▶ Play Rhyme",
        "stop": "⏹ Stop",
        "back": "⬅ Back",
        "warning": "Warning",
        "select_warning": "Please select a rhyme."
    },
    "ml": {
        "title": "ഒരു ബാലഗാനം തിരഞ്ഞെടുക്കൂ",
        "play": "▶ ഗാനം ആഡ് ചെയ്യുക",
        "stop": "⏹ നിർത്തുക",
        "back": "⬅ മടങ്ങുക",
        "warning": "മുന്നറിയിപ്പ്",
        "select_warning": "ദയവായി ഒരു ബാലഗാനം തിരഞ്ഞെടുക്കുക."
    },
    "hi": {
        "title": "एक कविता चुनें",
        "play": "▶ कविता चलाएं",
        "stop": "⏹ बंद करें",
        "back": "⬅ वापस",
        "warning": "चेतावनी",
        "select_warning": "कृपया एक कविता चुनें।"
    },
    "ta": {
        "title": "ஒரு பாடலைத் தேர்ந்தெடுக்கவும்",
        "play": "▶ பாடலை இயக்கவும்",
        "stop": "⏹ நிறுத்தவும்",
        "back": "⬅ திரும்பவும்",
        "warning": "எச்சரிக்கை",
        "select_warning": "தயவுசெய்து ஒரு பாடலைத் தேர்ந்தெடுக்கவும்."
    },
    "te": {
        "title": "ఒక పద్యం ఎంచుకోండి",
        "play": "▶ పద్యం ఆడించండి",
        "stop": "⏹ ఆపు",
        "back": "⬅ వెనక్కి",
        "warning": "హెచ్చరిక",
        "select_warning": "దయచేసి ఒక పద్యం ఎంచుకోండి."
    },
    "kn": {
        "title": "ಒಂದು ಕಥೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "play": "▶ ಪದ್ಯವನ್ನು ಆಡಿಸಿ",
        "stop": "⏹ ನಿಲ್ಲಿಸಿ",
        "back": "⬅ ಹಿಂದಕ್ಕೆ",
        "warning": "ಎಚ್ಚರಿಕೆ",
        "select_warning": "ದಯವಿಟ್ಟು ಒಂದು ಪದ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ."
    }
}




def set_language_and_open(lang_code, root):
    global selected_lang_code
    selected_lang_code = lang_code
    open_category_window(root, root)

def show_intro_window():
    intro = tk.Tk()
    intro.title("Welcome to Little Learn App")
    intro.attributes('-fullscreen', True)
    intro.configure(bg="gray")

    # Load and set background image
    try:
        pil_image = Image.open(resource_path("Images/intro.jpg"))
        bg_image = ImageTk.PhotoImage(pil_image)
    except Exception as e:
        print("Failed to load image:", e)
        bg_image = None

    if bg_image:
        bg_label = tk.Label(intro, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # --- Custom Rounded Button Class with Shadow and Animation ---
    class AnimatedRoundedButton(tk.Canvas):
        def __init__(self, parent, text, command=None, width=200, height=50, radius=20,
                     bg="#546E7A", fg="white", hover_bg="#455A64", padx=10, pady=5,
                     font_family="Segoe UI", font_size=18, font_weight="normal"):

            self.bg = bg          # save bg before super
            self.fg = fg
            self.hover_bg = hover_bg
            self.command = command
            self.text = text
            self.radius = radius
            self.width = width
            self.height = height
            self.padx = padx
            self.pady = pady
            self.font_family = font_family
            self.font_weight = font_weight
            self.font_size = font_size

            # Use parent's bg color for canvas bg to avoid black edges
            # When calling super().__init__ inside your AnimatedRoundedButton:

            parent_bg = parent['bg'] if 'bg' in parent.keys() else None
            super().__init__(parent, width=width, height=height, highlightthickness=0, bg="#5EC2B7")
    

            # Draw main button
            self.button = self.create_rounded_rect(0, 0, width-4, height-4, radius, fill="", outline="white", width=2)

            # Draw text label
            self.label = self.create_text(width // 2 - 2, height // 2 - 2,
                                          text=text, fill=fg,
                                          font=(font_family, font_size, font_weight))

            # Bindings
            self.bind("<Button-1>", self._on_click)
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.tag_bind(self.button, "<Button-1>", self._on_click)
            self.tag_bind(self.label, "<Button-1>", self._on_click)
            self.tag_bind(self.button, "<Enter>", self._on_enter)
            self.tag_bind(self.label, "<Enter>", self._on_enter)
            self.tag_bind(self.button, "<Leave>", self._on_leave)
            self.tag_bind(self.label, "<Leave>", self._on_leave)

            # Place the canvas padding inside the parent
            self.pack(padx=self.padx, pady=self.pady)

            # Animation cycles
            self.color_cycle = itertools.cycle([bg, hover_bg, "#C08081", "#D36C6C", hover_bg])
            self.size_cycle = itertools.cycle([font_size, font_size + 1, font_size + 2, font_size + 1])

            # Start animations
            self.animate_color()
            self.animate_size()
        def create_tilted_rounded_rect(self, x1, y1, x2, y2, r, tilt_x=10, tilt_y=5, **kwargs):
            points = [
                x1 + r + tilt_x, y1,
                x2 - r + tilt_x, y1,
                x2 + tilt_x + tilt_y, y1 + r,
                x2 + tilt_x + tilt_y, y2 - r,
                x2 - r, y2,
                x1 + r, y2,
                x1, y2 - r,
                x1, y1 + r,
            ]
            return self.create_polygon(points, smooth=True, **kwargs)
        def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
            points = [
                x1 + r, y1,
                x2 - r, y1,
                x2, y1,
                x2, y1 + r,
                x2, y2 - r,
                x2, y2,
                x2 - r, y2,
                x1 + r, y2,
                x1, y2,
                x1, y2 - r,
                x1, y1 + r,
                x1, y1,
            ]
            return self.create_polygon(points, smooth=True, **kwargs)

        def _on_click(self, event):
            if self.command:
                self.command()

        def _on_enter(self, event):
            self.itemconfig(self.button, fill=self.hover_bg)

        def _on_leave(self, event):
            self.itemconfig(self.button, fill=self.bg)

        def animate_color(self):
            new_color = next(self.color_cycle)
            self.itemconfig(self.button, fill=new_color)
            self.after(700, self.animate_color)

        def animate_size(self):
            new_size = next(self.size_cycle)
            self.itemconfig(self.label, font=(self.font_family, new_size, self.font_weight))
            self.after(150, self.animate_size)

    # Add control frame with buttons (assuming create_colored_button is defined elsewhere)
    control_frame = tk.Frame(intro, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')
    create_colored_button(control_frame, "✖", command=intro.destroy, width=40, height=30,
                          radius=16, bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=intro.iconify, width=40, height=30,
                          radius=16, bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    # Instantiate your animated curved button
    start_button = AnimatedRoundedButton(
        intro,
        text="Start Learning",
        command=lambda: open_language_window(intro, intro),
        width=350,
        height=80,
        radius=70,
        bg="#DA70D6",        # metallic pink or your choice
        hover_bg="#FF69B4",  # lighter pink on hover
        fg="white",
        font_family="Arial",
        font_size=24,
        font_weight="bold"
    )
    # Updated code (button placed near bottom center)
    start_button.place(relx=0.5, rely=0.95, anchor="s")


    intro.mainloop()


# --------- Window 1: Language Selection ---------
def open_language_window(int,root):
    int.withdraw()
    roo = tk.Toplevel()
    roo.title("Language Selection")
    roo.attributes('-fullscreen', True)
    roo.configure(bg="#FFFACD")

    control_frame = tk.Frame(roo, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    # Close and minimize buttons
    create_colored_button(control_frame, "✖", command=root.destroy, width=60, height=40,
                          radius=12, bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=roo.iconify, width=60, height=40,
                          radius=12, bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(roo, text="Select Language", font=("Segoe UI", 28, "bold"), bg="#FFFACD", fg="#263238").pack(pady=60)

    # Language buttons
    create_colored_button(roo, "English", command=lambda: open_category_window(roo, root),
                          width=350, height=60, radius=30, bg="#546E7A", hover_bg="#455A64", fg="white").pack(pady=20)

    create_colored_button(roo, "Malayalam", command=lambda: open_category_window_malayalam(roo, root),
                          width=350, height=60, radius=30, bg="#2E7D32", hover_bg="#1B5E20", fg="white").pack(pady=20)

    create_colored_button(roo, "Hindi", command=lambda: open_category_window_hindi(roo, root),
                          width=350, height=60, radius=30, bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)

    create_colored_button(root, "Tamil", command=lambda: open_category_window_tamil(roo, root),
                          width=350, height=60, radius=30, bg="#6A1B9A", hover_bg="#4A148C", fg="white").pack(pady=20)

    create_colored_button(roo, "Telugu", command=lambda: open_category_window_telugu(roo, root),
                          width=350, height=60, radius=30, bg="#00897B", hover_bg="#00695C", fg="white").pack(pady=20)

    create_colored_button(roo, "Kannada", command=lambda: open_category_window_kannada(roo, root),
                          width=350, height=60, radius=30, bg="#FF8F00", hover_bg="#EF6C00", fg="white").pack(pady=20)




# --------- Window 2: Study Category ---------
def open_category_window(prev_win, root):
    prev_win.withdraw()  # Hide language window

    win = tk.Toplevel()
    win.title("Study Menu")
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFFACD")

    control_frame = tk.Frame(win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    # X button closes entire app
    create_colored_button(control_frame, "✖", command=root.destroy,
                          width=60, height=40, radius=12,
                          bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)

    # Minimize button
    create_colored_button(control_frame, "—", command=win.iconify,
                          width=60, height=40, radius=12,
                          bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(win, text="What do you want to study?", font=("Segoe UI", 28, "bold"),
             bg="#FFFACD", fg="#263238").pack(pady=60)

    create_colored_button(win, "Letters", command=lambda: open_letters_window(win, root),
                          width=350, height=60, radius=30,
                          bg="#2196F3", hover_bg="#1976D2", fg="white").pack(pady=20)
    create_colored_button(win, "Grammar", command=lambda: open_grammar_window(win, root),
                          width=350, height=60, radius=30,
                          bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)
    create_colored_button(win, "Story", command=lambda: open_story_window(win, root),
                          width=350, height=60, radius=30,
                          bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)
    create_colored_button(win, "Rhyme", command=lambda: open_rhyme_window(win, root),
                          width=350, height=60, radius=30,
                          bg="#009688", hover_bg="#00796B", fg="white").pack(pady=20)

    # Back button to go back to language window
    create_colored_button(win, "Back", command=lambda: [win.destroy(), prev_win.deiconify()],
                          width=150, height=40, radius=20,
                          bg="#757575", hover_bg="#616161", fg="white").pack(pady=20)



# --------- Window 3: Letters ---------

def open_letters_window(prev_win, root, selected_lang_code='en'):
    prev_win.withdraw()

    letters_win = tk.Toplevel()
    letters_win.title("Learn Letters")
    letters_win.attributes('-fullscreen', True)
    letters_win.configure(bg="#FFFACD")

    control_frame = tk.Frame(letters_win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖", command=lambda: [stop_audio(), letters_win.destroy(), root.destroy()],
                          width=60, height=40, font=("Segoe UI", 14, "bold"),
                          bg="#f44336", fg="white", hover_bg="#d32f2f").pack(side="right", padx=5, pady=5)

    create_colored_button(control_frame, "—", command=letters_win.iconify,
                          width=60, height=40, font=("Segoe UI", 14, "bold"),
                          bg="#2196F3", fg="white", hover_bg="#1976D2").pack(side="right", padx=5, pady=5)

    lang = translations.get(selected_lang_code, translations['en'])

    current_index = {'val': 0}
    letters = [chr(i) for i in range(65, 91)]

    example_words = {
        'A': "A for Apple", 'B': "B for Ball", 'C': "C for Cat", 'D': "D for Dog",
        'E': "E for Elephant", 'F': "F for Fish", 'G': "G for Goat", 'H': "H for Hat",
        'I': "I for Ice", 'J': "J for Jug", 'K': "K for Kite", 'L': "L for Lion",
        'M': "M for Monkey", 'N': "N for Nest", 'O': "O for Owl", 'P': "P for Pig",
        'Q': "Q for Queen", 'R': "R for Rat", 'S': "S for Sun", 'T': "T for Tiger",
        'U': "U for Umbrella", 'V': "V for Van", 'W': "W for Wolf", 'X': "X for X-ray",
        'Y': "Y for Yak", 'Z': "Z for Zebra"
    }

    content_frame = tk.Frame(letters_win, bg="#FFFACD")
    content_frame.pack(expand=True)

    image_label = tk.Label(content_frame, bg="#FFFACD")
    image_label.pack(pady=10)

    letter_label = tk.Label(content_frame, text="", font=("Arial", 60, "bold"), bg="#FFFACD")
    letter_label.pack()

    example_label = tk.Label(content_frame, text="", font=("Arial", 24), bg="#FFFACD")
    example_label.pack(pady=10)

    def show_letter():
        stop_audio()
        letter = letters[current_index['val']]
        example = example_words.get(letter, "")
        letter_label.config(text=f"{letter} / {letter.lower()}")
        example_label.config(text=f"Example: {example}")
        play_text_audio(example)

        image_path = resource_path(f"Images/{letter.lower()}.jpg")
        try:
            img = Image.open(image_path).resize((500, 500))
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo, text="")
            image_label.image = photo
        except Exception:
            image_label.config(image="", text="(Image not found)", font=("Arial", 14))

    def next_letter():
        if current_index['val'] < 25:
            current_index['val'] += 1
            show_letter()

    def prev_letter():
        if current_index['val'] > 0:
            current_index['val'] -= 1
            show_letter()

    btn_frame = tk.Frame(letters_win, bg="#FFFACD")
    btn_frame.pack(pady=20)

    # Navigation buttons
    nav_row = tk.Frame(btn_frame, bg="#FFFACD")
    nav_row.pack(pady=10)

    create_colored_button(nav_row, lang["prev"], prev_letter,
                          width=200, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#607D8B", fg="white", hover_bg="#455A64").pack(side="left", padx=40)

    create_colored_button(nav_row, lang["next"], next_letter,
                          width=200, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#607D8B", fg="white", hover_bg="#455A64").pack(side="right", padx=40)

    # Speak button
    speak_text = translations.get(selected_lang_code, translations['en'])['speak']
    create_colored_button(btn_frame, speak_text,
                          lambda: play_text_audio(example_words[letters[current_index['val']]]),
                          width=200, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#2196F3", fg="white", hover_bg="#1976D2").pack(pady=10)

    # Back button
    create_colored_button(btn_frame, lang["back"],
                          lambda: [stop_audio(), letters_win.destroy(), prev_win.deiconify()],
                          width=200, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#f44336", fg="white", hover_bg="#d32f2f").pack(pady=10)

    show_letter()



# --------- Window 4: Grammar ---------
basic_grammar_texts = {
    'en': """1. Nouns: Names of people, places, or things.
2. Pronouns: Words that replace nouns.
3. Verbs: Action or state of being words.
4. Adjectives: Describe nouns.
5. Adverbs: Describe verbs, adjectives, or other adverbs.
6. Prepositions: Show relationships between words.
7. Conjunctions: Connect words or groups of words.
8. Interjections: Express strong feelings or emotions.""",

    'ml': """1. Nouns: ആളുകൾ, സ്ഥലങ്ങൾ, വസ്തുക്കളുടെ പേര്.
2. Pronouns: നാമം മാറ്റുന്ന വാക്കുകൾ.
3. Verbs: പ്രവർത്തി അല്ലെങ്കിൽ അവസ്ഥ വാക്കുകൾ.
4. Adjectives: നാമങ്ങളെ വിവരണം ചെയ്യുന്നു.
5. Adverbs: ക്രിയ, വിശേഷണം, അല്ലെങ്കിൽ മറ്റ് ക്രിയാവിശേഷണങ്ങളെ വിവരണം ചെയ്യുന്നു.
6. Prepositions: വാക്കുകൾ തമ്മിലുള്ള ബന്ധം കാണിക്കുന്നു.
7. Conjunctions: വാക്കുകൾ അല്ലെങ്കിൽ വാക്കുകളുടെ കൂട്ടങ്ങളെ ബന്ധിപ്പിക്കുന്നു.
8. Interjections: ശക്തമായ വികാരങ്ങൾ പ്രകടിപ്പിക്കുന്നു.""",

    'hi': """1. Nouns: व्यक्ति, स्थान, या वस्तु के नाम।
2. Pronouns: संज्ञा के स्थान पर आने वाले शब्द।
3. Verbs: कार्य या स्थिति दर्शाने वाले शब्द।
4. Adjectives: संज्ञा का वर्णन करने वाले शब्द।
5. Adverbs: क्रिया, विशेषण या अन्य क्रिया विशेषण का वर्णन करने वाले शब्द।
6. Prepositions: शब्दों के बीच संबंध दर्शाते हैं।
7. Conjunctions: शब्दों या शब्द समूहों को जोड़ते हैं।
8. Interjections: तीव्र भाव या भावना व्यक्त करते हैं।""",

    'ta': """1. Nouns: மனிதர்கள், இடங்கள் அல்லது பொருட்களின் பெயர்கள்.
2. Pronouns: பெயர்ச்சொல்லை மாற்றும் சொற்கள்.
3. Verbs: செயல் அல்லது நிலையை கூறும் சொற்கள்.
4. Adjectives: பெயர்ச்சொற்களை விளக்கும் சொற்கள்.
5. Adverbs: வினைச்சொல், பண்பொருள் அல்லது பிற வினையடைச்சொற்களை விளக்கும் சொற்கள்.
6. Prepositions: சொற்களுக்கிடையிலான உறவை காட்டும் சொற்கள்.
7. Conjunctions: சொற்கள் அல்லது சொற்றொடர்களை இணைக்கும் சொற்கள்.
8. Interjections: தீவிரமான உணர்வுகளை வெளிப்படுத்தும் சொற்கள்.""",

    'te': """1. Nouns: వ్యక్తులు, స్థానాలు లేదా వస్తువుల పేర్లు.
2. Pronouns: నామవాచకం స్థానంలో వచ్చే పదాలు.
3. Verbs: కార్యాన్ని లేదా స్థితిని తెలియజేసే పదాలు.
4. Adjectives: నామవాచకాలను వివరించే పదాలు.
5. Adverbs: క్రియ, విశేషణం లేదా ఇతర క్రియావిశేషణాలను వివరించే పదాలు.
6. Prepositions: పదాల మధ్య సంబంధాన్ని చూపుతుంది.
7. Conjunctions: పదాలు లేదా పదబంధాలను కలుపుతాయి.
8. Interjections: తీవ్ర భావాలను వ్యక్తపరుస్తాయి.""",

    'kn': """1. Nouns: ಜನರು, ಸ್ಥಳಗಳು ಅಥವಾ ವಸ್ತುಗಳ ಹೆಸರುಗಳು.
2. Pronouns: ನಾಮಪದದ ಬದಲಾಗಿ ಬರುವ ಪದಗಳು.
3. Verbs: ಕ್ರಿಯೆಯನ್ನು ಅಥವಾ ಸ್ಥಿತಿಯನ್ನು ಸೂಚಿಸುವ ಪದಗಳು.
4. Adjectives: ನಾಮಪದಗಳನ್ನು ವರ್ಣಿಸುವ ಪದಗಳು.
5. Adverbs: ಕ್ರಿಯಾಪದ, ವಿಶೇಷಣ ಅಥವಾ ಇತರೆ ಕ್ರಿಯಾವಿಶೇಷಣಗಳನ್ನು ವರ್ಣಿಸುವ ಪದಗಳು.
6. Prepositions: ಪದಗಳ ನಡುವಿನ ಸಂಬಂಧವನ್ನು ತೋರಿಸುತ್ತದೆ.
7. Conjunctions: ಪದಗಳು ಅಥವಾ ಪದಗುಚ್ಛಗಳನ್ನು ಸಂಪರ್ಕಿಸುತ್ತದೆ.
8. Interjections: ಬಲವಾದ ಭಾವನೆಗಳನ್ನು ವ್ಯಕ್ತಪಡಿಸುತ್ತದೆ."""
}

def open_basic_grammar_study(parent_win, root, lang_code='en'):
    parent_win.withdraw()
    win = tk.Toplevel()
    win.title(translations1[lang_code]["basic_grammar"])
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFF8E1")

    # Title
    tk.Label(win, text=translations1[lang_code]["basic_grammar"],
             font=("Arial", 28, "bold"), bg="#FFF8E1").pack(pady=(20, 10))

    grammar_text = basic_grammar_texts.get(lang_code, basic_grammar_texts['en'])

    # --- Container frame to center white box ---
    center_container = tk.Frame(win, bg="#FFF8E1")
    center_container.pack(expand=True, fill="both")

    # --- White frame centered in the screen ---
    white_frame = tk.Frame(center_container, bg="white", bd=2, relief="groove", width=1100, height=700)
    white_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Make sure frame does not shrink
    white_frame.pack_propagate(False)

    # Text widget inside white frame
    text_widget = tk.Text(white_frame, wrap="word", font=("Arial", 28, "bold"),
                          bg="white", bd=0)
    text_widget.insert("1.0", grammar_text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both", padx=20, pady=20)

    # --- Buttons Frame ---
    btn_frame = tk.Frame(win, bg="#FFF8E1")
    btn_frame.pack(side="bottom", pady=30)

    listen_btn = create_colored_button(btn_frame, translations1[lang_code]["listen"],
                                       lambda: play_text_audio(grammar_text),
                                       width=250, height=60, font=("Segoe UI", 18, "bold"),
                                       bg="#2196F3", hover_bg="#1976D2")
    listen_btn.pack(side="left", padx=20)

    back_btn = create_colored_button(btn_frame, translations1[lang_code]["back"],
                                     lambda: [stop_audio(), win.destroy(), parent_win.deiconify()],
                                     width=250, height=60, font=("Segoe UI", 18, "bold"),
                                     bg="#f44336", hover_bg="#d32f2f")
    back_btn.pack(side="left", padx=20)





def open_grammar_analyzer(parent_win, root, lang_code='en'):
    parent_win.withdraw()
    win = tk.Toplevel()
    win.title(translations1[lang_code]["grammar_analyzer"])
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFF8E1")

    tk.Label(win, text="📝 " + translations1[lang_code]["grammar_analyzer"],
             font=("Arial", 24, "bold"), bg="#FFF8E1").pack(pady=30)

    tk.Label(win, text=translations1[lang_code]["enter_sentence"],
             font=("Arial", 16), bg="#FFF8E1").pack(pady=10)

    input_box = tk.Text(win, height=3, width=60, font=("Arial", 14))
    input_box.pack(pady=10)

    result_label = tk.Label(win, text="", font=("Arial", 16),
                            justify="left", bg="#FFF8E1", anchor="w")
    result_label.pack(pady=15)

    def analyze():
        sentence = input_box.get("1.0", tk.END).strip()
        if not sentence:
            messagebox.showwarning("⚠", translations1[lang_code]["enter_sentence"])
            return
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)

        nouns = [w for w, pos in tagged if pos.startswith("NN")]
        pronouns = [w for w, pos in tagged if pos.startswith("PRP")]
        verbs = [w for w, pos in tagged if pos.startswith("VB")]

        result_text = (
            f"Nouns: {', '.join(nouns) or 'None'}\n"
            f"Pronouns: {', '.join(pronouns) or 'None'}\n"
            f"Verbs: {', '.join(verbs) or 'None'}"
        )
        result_label.config(text=result_text)
        play_text_audio(result_text)

    create_colored_button(win, translations1[lang_code]["analyze"], analyze,
                          width=500, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#009688", hover_bg="#00796B").pack(pady=10)

    create_colored_button(win, translations1[lang_code]["back"],
                          lambda: [stop_audio(), win.destroy(), parent_win.deiconify()],
                          width=300, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#f44336", hover_bg="#d32f2f").pack(pady=30)

def open_grammar_window(prev_win, root, lang_code='en'):
    prev_win.withdraw()
    main_grammar_win = tk.Toplevel()
    main_grammar_win.title("Grammar")
    main_grammar_win.attributes('-fullscreen', True)
    main_grammar_win.configure(bg="#FFF8E1")

    control_frame = tk.Frame(main_grammar_win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖",
                          command=lambda: [stop_audio(), main_grammar_win.destroy(), root.destroy()],
                          width=60, height=40,
                          bg="#f44336", fg="white", hover_bg="#d32f2f").pack(side="right", padx=5, pady=5)

    create_colored_button(control_frame, "—",
                          command=main_grammar_win.iconify,
                          width=60, height=40,
                          bg="#2196F3", fg="white", hover_bg="#1976D2").pack(side="right", padx=5, pady=5)

    tk.Label(main_grammar_win, text=translations1[lang_code]["grammar_options"],
             font=("Arial", 24, "bold"), bg="#FFF8E1").pack(pady=30)

    create_colored_button(main_grammar_win, "📚 " + translations1[lang_code]["basic_grammar"],
                          lambda: open_basic_grammar_study(main_grammar_win, root, lang_code),
                          width=900, height=80, font=("Segoe UI", 26, "bold"),
                          bg="#3F51B5", hover_bg="#303F9F").pack(pady=20)

    create_colored_button(main_grammar_win, "📝 " + translations1[lang_code]["grammar_analyzer"],
                          lambda: open_grammar_analyzer(main_grammar_win, root, lang_code),
                          width=600, height=80, font=("Segoe UI", 26, "bold"),
                          bg="#009688", hover_bg="#00796B").pack(pady=20)

    create_colored_button(main_grammar_win, "⬅ " + translations1[lang_code]["back"],
                          lambda: [main_grammar_win.destroy(), prev_win.deiconify()],
                          width=250, height=60, font=("Segoe UI", 18, "bold"),
                          bg="#f44336", hover_bg="#d32f2f").pack(pady=40)



#------------Story window-------------
def open_story_window(prev_win, root, lang_code="en"):
    prev_win.withdraw()
    story_win = tk.Toplevel()
    story_win.title("Moral Stories")
    story_win.attributes('-fullscreen', True)
    story_win.configure(bg="#FFFACD")

    # Top control panel
    top_frame = tk.Frame(story_win, bg="#FFFACD")
    top_frame.pack(fill='x', side='top', anchor='ne')

    create_colored_button(top_frame, "✖", lambda: [stop_audio(), story_win.destroy(), root.quit()],
                          width=60, height=40,
                          bg="#f44336", fg="white", hover_bg="#d32f2f").pack(side="right", padx=5, pady=5)
    create_colored_button(top_frame, "—", lambda: story_win.iconify(),
                          width=60, height=40,
                          bg="#2196F3", fg="white", hover_bg="#1976D2").pack(side="right", padx=5, pady=5)

    # Title label
    tk.Label(story_win, text=translation2[lang_code]["title"], font=("Arial", 26, "bold"), bg="#FFFACD", fg="#333").pack(pady=20)

    # Sample stories dictionary (title: content)
    stories ={
        "The Lion and the Mouse": (
            "One day, a mighty lion was sleeping peacefully in the forest. "
            "Suddenly, a tiny mouse ran across his paw, waking him up. "
            "The lion caught the mouse and was about to eat it. "
            "The little mouse begged for mercy, promising to help the lion someday. "
            "The lion laughed but let the mouse go.\n\n"
            "A few days later, the lion got trapped in a hunter’s net. "
            "He roared loudly, but no one came to help. "
            "The little mouse heard the roar, came quickly, and gnawed through the ropes to free the lion. "
            "The lion was grateful and realized even the smallest friends can be the greatest helpers.\n\n"
            "Moral: Small acts of kindness can be powerful."
        ),

        "The Thirsty Crow": (
            "On a hot summer day, a thirsty crow flew all over looking for water. "
            "After a long search, it found a pitcher with a little water at the bottom, but the water was too low to reach. "
            "The clever crow picked up small stones and dropped them one by one into the pitcher. "
            "The water level rose, and soon the crow was able to drink.\n\n"
            "The crow’s patience and clever thinking saved it from thirst.\n\n"
            "Moral: Where there is a will, there is a way."
        ),

        "The Honest Woodcutter": (
            "A poor woodcutter was chopping wood by the river when his axe slipped and fell into the water. "
            "He was very sad as he had no money to buy a new one.\n\n"
            "Suddenly, a fairy appeared and offered to help. "
            "She brought up a golden axe and asked if it was his. "
            "The woodcutter honestly said no. "
            "She then showed a silver axe, but he said no again.\n\n"
            "Finally, she showed his old axe, and he happily took it. "
            "The fairy was so impressed with his honesty that she gave him all three axes.\n\n"
            "Moral: Honesty is the best policy."
        ),

        "The Fox and the Grapes": (
            "A hungry fox saw a bunch of ripe grapes hanging high on a vine. "
            "He jumped and jumped but couldn’t reach them. "
            "After many tries, tired and disappointed, he walked away saying, 'Those grapes are sour anyway.'\n\n"
            "This story teaches how sometimes people pretend to dislike what they cannot have.\n\n"
            "Moral: It’s easy to hate what you can’t have."
        ),

        "The Tortoise and the Hare": (
            "The hare was very proud of how fast he could run. "
            "One day, he challenged the slow tortoise to a race. "
            "The race began, and the hare sped ahead, confident he would win easily.\n\n"
            "Feeling sure of victory, the hare took a nap mid-race. "
            "Meanwhile, the tortoise kept moving slowly but steadily. "
            "When the hare woke up, he saw the tortoise crossing the finish line first.\n\n"
            "Moral: Slow and steady wins the race."
        ),

        "The Greedy Dog": (
            "A dog found a big bone and happily carried it home. "
            "On the way, he crossed a river and saw his own reflection in the water with the bone. "
            "Thinking it was another dog with a bigger bone, he barked and dropped his own bone into the water.\n\n"
            "He ended up with no bone at all.\n\n"
            "Moral: Greed leads to loss."
        ),

        "The Ant and the Grasshopper": (
            "All summer long, the hardworking ant gathered food and stored it for winter. "
            "The carefree grasshopper spent the summer singing and playing.\n\n"
            "When winter came, the grasshopper had no food and was hungry and cold. "
            "He asked the ant for help, but the ant reminded him to prepare for hard times.\n\n"
            "Moral: Work today for a better tomorrow."
        )
    }
    # --- Story Listbox ---
    story_listbox = tk.Listbox(
        story_win, font=("Arial", 18, "bold"), height=10, width=50,
        bg="#FFFFFF", fg="#000000", selectbackground="#FFD54F"
    )
    for title in stories:
        story_listbox.insert(tk.END, title)
    story_listbox.pack(pady=10, padx=50, fill='x')

    def open_story_detail():
        selected = story_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", translation2[lang_code]["warning"])
            return
        title = story_listbox.get(selected[0])
        content = stories[title]

        story_detail_win = tk.Toplevel(story_win)
        story_detail_win.title(title)
        story_detail_win.attributes('-fullscreen', True)
        story_detail_win.configure(bg="#FFFACD")

        text_frame = tk.Frame(story_detail_win, bg="#FFFACD", bd=2, relief="groove")
        text_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)

        text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("bold", 30),
            bg="#FFFACD",
            padx=20,
            pady=20
        )
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both")

        button_frame = tk.Frame(story_detail_win, bg="#FFFACD")
        button_frame.pack(side="bottom", pady=30)

        create_colored_button(button_frame, translation2[lang_code]["listen"], lambda: play_text_audio(content),
                              width=300, height=60, radius=30, bg="#2196F3", hover_bg="#1976D2").pack(pady=10)

        create_colored_button(button_frame, translation2[lang_code]["back"], lambda: [stop_audio(), story_detail_win.destroy()],
                              width=300, height=60, radius=30, bg="#f44336", hover_bg="#d32f2f").pack(pady=20)

    button_frame = tk.Frame(story_win, bg="#FFFACD")
    button_frame.pack(pady=30)

    create_colored_button(button_frame, translation2[lang_code]["open_story"], open_story_detail,
                          width=300, height=60, radius=30,
                          bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)

    create_colored_button(button_frame, translation2[lang_code]["back"],
                          lambda: [stop_audio(), story_win.destroy(), prev_win.deiconify()],
                          width=300, height=60, radius=30,
                          bg="#f44336", hover_bg="#d32f2f", fg="white").pack(pady=20)


def open_rhyme_window(prev_win, root, lang_code="en"):
    stop_audio()
    prev_win.withdraw()

    rhyme_win = tk.Toplevel()
    rhyme_win.title("Rhymes")
    rhyme_win.attributes("-fullscreen", True)
    rhyme_win.configure(bg="#E3F2FD")

    t = translation3[lang_code]  # Get translation

    # Title
    tk.Label(
        rhyme_win, text=t["title"], font=("Arial", 32, "bold"),
        bg="#E3F2FD", fg="#0D47A1"
    ).pack(pady=20)

    # Scrollable Rhyme List
    list_frame = tk.Frame(rhyme_win, bg="#E3F2FD")
    list_frame.pack(pady=10)

    scrollbar = tk.Scrollbar(list_frame)
    rhyme_listbox = tk.Listbox(
        list_frame, font=("Arial", 18, "bold"), height=8, width=40,
        yscrollcommand=scrollbar.set, bg="#FFFFFF", fg="#000000", selectbackground="#90CAF9"
    )
    scrollbar.config(command=rhyme_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    rhyme_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Lyrics Display Area inside a frame (optional visual separation)
    display_frame = tk.Frame(rhyme_win, bg="#E3F2FD")
    display_frame.pack(pady=20, padx=40, fill="both", expand=False)

    rhyme_text_display = tk.Text(
        display_frame, font=("Arial", 22, "bold"), wrap="word", height=10, width=70,
        bg="#FFFFFF", fg="#1A237E", padx=10, pady=10, borderwidth=2, relief="groove"
    )
    rhyme_text_display.pack(fill="both", expand=True)

    rhymes = {
        "Twinkle Twinkle Little Star": (
            "Twinkle, twinkle, little star,\n"
            "How I wonder what you are!\n"
            "Up above the world so high,\n"
            "Like a diamond in the sky.\n\n"
            "Twinkle, twinkle, little star,\n"
            "How I wonder what you are!"
            ,"rhymes/twinkle.mp3"
        ),
        "Baa Baa Black Sheep": (
            "Baa baa black sheep, have you any wool?\n"
            "Yes sir, yes sir, three bags full;\n"
            "One for the master, one for the dame,\n"
            "And one for the little boy who lives down the lane."
            ,"rhymes/baa.mp3"
        ),
        "Jack and Jill": (
            "Jack and Jill went up the hill\n"
            "To fetch a pail of water.\n"
            "Jack fell down and broke his crown,\n"
            "And Jill came tumbling after."
             ,"rhymes/jack.mp3"
        ),
        "Humpty Dumpty": (
            "Humpty Dumpty sat on a wall,\n"
            "Humpty Dumpty had a great fall.\n"
            "All the king's horses and all the king's men\n"
            "Couldn't put Humpty together again."
             ,"rhymes/humpty.mp3"
        ),
        "London Bridge Is Falling Down": (
            "London Bridge is falling down,\n"
            "Falling down, falling down,\n"
            "London Bridge is falling down,\n"
            "My fair lady.\n\n"
            
            "Build it up with wood and clay,\n"
            "Wood and clay, wood and clay,\n"
            "Build it up with wood and clay,\n"
            "My fair lady.\n\n"

            "Wood and clay will wash away,\n"
            "Wash away, wash away,\n"
            "Wood and clay will wash away,\n"
            "My fair lady.\n\n"

            "Build it up with bricks and stone,\n"
            "Bricks and stone, bricks and stone,\n"
            "Build it up with bricks and stone,\n"
            "My fair lady.\n\n"

            "Bricks and stone will not stay,\n"
            "Not stay, not stay,\n"
            "Bricks and stone will not stay,\n"
            "My fair lady."
            ,"rhymes/london.mp3"
        ),
        "The Alphabet Song":(
            "A-B-C-D-E-F-G\n"
            "H-I-J-K-LMNOP\n"
            "Q-R-S T-U-V\n"
            "W X Y and Zee\n"
            "Now I know my “ABCs”\n"
            "Next time won’t you sing with me?\n"
            "Now we know our “ABCs”\n"
            "next time we can sing with glee."
            ,"rhymes/alphabet.mp3"
        ),
        "Row Row Row Your Boat": (
            "Row, row, row your boat\n"
            "Gently down the stream.\n"
            "Merrily, merrily, merrily, merrily,\n"
            "Life is but a dream."
            ,"rhymes/row.mp3"
        )
    }

    for title in rhymes:
        rhyme_listbox.insert(tk.END, title)

    # Play selected rhyme
    def play_selected_rhyme():
        selected = rhyme_listbox.curselection()
        if not selected:
            messagebox.showwarning(t["warning"], t["select_warning"])
            return
        title = rhyme_listbox.get(selected[0])
        lyrics, mp3_path1 = rhymes[title]
        mp3_path = resource_path(mp3_path1)

        rhyme_text_display.delete("1.0", tk.END)
        rhyme_text_display.insert(tk.END, lyrics)
        play_mp3(mp3_path)

    # --- Bottom Button Frame ---
    btn_frame = tk.Frame(rhyme_win, bg="#E3F2FD")
    btn_frame.pack(side="bottom", pady=30)

    create_colored_button(
        btn_frame, t["play"], play_selected_rhyme,
        width=250, height=60, radius=30, bg="#4CAF50", hover_bg="#388E3C",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=20)

    create_colored_button(
        btn_frame, t["stop"], stop_audio,
        width=250, height=60, radius=30, bg="#FF9800", hover_bg="#EF6C00",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=20)

    create_colored_button(
        btn_frame, t["back"], lambda: [stop_audio(), rhyme_win.destroy(), prev_win.deiconify()],
        width=250, height=60, radius=30, bg="#f44336", hover_bg="#d32f2f",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=20)



def open_category_window_malayalam(prev_win, root):
    prev_win.withdraw()
    win = tk.Toplevel()
    win.title("പഠന മെനു")
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFFACD")

    control_frame = tk.Frame(win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖", command=win.destroy,
                          width=60, height=40, radius=12,
                          bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=win.iconify,
                          width=60, height=40, radius=12,
                          bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(win, text="നിങ്ങൾ പഠിക്കാൻ ആഗ്രഹിക്കുന്നതു എന്ത്?", font=("Segoe UI", 28, "bold"),
             bg="#FFFACD", fg="#263238").pack(pady=60)

    create_colored_button(win, "അക്ഷരങ്ങൾ", command=lambda: open_letters_window(win, root, selected_lang_code='ml'),
                          width=350, height=60, radius=30,
                          bg="#2196F3", hover_bg="#1976D2", fg="white").pack(pady=20)
    create_colored_button(win, "വ്യാകരണം", command=lambda: open_grammar_window(win, root, lang_code='ml'),
                          width=350, height=60, radius=30,
                          bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)
    create_colored_button(win, "കഥ", command=lambda: open_story_window(win, root, lang_code="ml"),
                          width=350, height=60, radius=30,
                          bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)
    create_colored_button(win, "പാട്ട്", command=lambda: open_rhyme_window(win, root, lang_code="ml"),
                          width=350, height=60, radius=30,
                          bg="#009688", hover_bg="#00796B", fg="white").pack(pady=20)

    create_colored_button(win, "പിന്നേയ്ക്ക്", command=lambda: [win.destroy(), prev_win.deiconify()],
                          width=150, height=40, radius=20,
                          bg="#757575", hover_bg="#616161", fg="white").pack(pady=20)

def open_category_window_hindi(prev_win, root):
    prev_win.withdraw()
    win = tk.Toplevel()
    win.title("अध्ययन मेनू")
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFFACD")

    control_frame = tk.Frame(win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖", command=win.destroy, width=60, height=40,
                          radius=12, bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=win.iconify, width=60, height=40,
                          radius=12, bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(win, text="आप क्या पढ़ना चाहते हैं?", font=("Segoe UI", 28, "bold"),
             bg="#FFFACD", fg="#263238").pack(pady=60)

    create_colored_button(win, "अक्षर", command=lambda: open_letters_window(win, root, selected_lang_code='hi'),
                          width=350, height=60, radius=30, bg="#2196F3", hover_bg="#1976D2", fg="white").pack(pady=20)
    create_colored_button(win, "व्याकरण", command=lambda: open_grammar_window(win, root, lang_code='hi'),
                          width=350, height=60, radius=30, bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)
    create_colored_button(win, "कहानी", command=lambda: open_story_window(win, root, lang_code="hi"),
                          width=350, height=60, radius=30, bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)
    create_colored_button(win, "कविता", command=lambda: open_rhyme_window(win, root, lang_code="hi"),
                          width=350, height=60, radius=30, bg="#009688", hover_bg="#00796B", fg="white").pack(pady=20)

    create_colored_button(win, "वापस", command=lambda: [win.destroy(), prev_win.deiconify()],
                          width=150, height=40, radius=20, bg="#757575", hover_bg="#616161", fg="white").pack(pady=20)

def open_category_window_tamil(prev_win, root):
    prev_win.withdraw()

    win = tk.Toplevel()
    win.title("படிப்பு பட்டி")
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFFACD")

    control_frame = tk.Frame(win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖", command=root.destroy,
                          width=60, height=40, radius=12,
                          bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=win.iconify,
                          width=60, height=40, radius=12,
                          bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(win, text="நீங்கள் என்ன படிக்க விரும்புகிறீர்கள்?", font=("Segoe UI", 28, "bold"),
             bg="#FFFACD", fg="#263238").pack(pady=60)

    create_colored_button(win, "எழுத்துக்கள்", command=lambda: open_letters_window(win, root, selected_lang_code='ta'),
                          width=350, height=60, radius=30,
                          bg="#2196F3", hover_bg="#1976D2", fg="white").pack(pady=20)
    create_colored_button(win, "விலக்கங்கள்", command=lambda: open_grammar_window(win, root, lang_code='ta'),
                          width=350, height=60, radius=30,
                          bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)
    create_colored_button(win, "கதை", command=lambda: open_story_window(win, root, lang_code="ta"),
                          width=350, height=60, radius=30,
                          bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)
    create_colored_button(win, "பாடல்", command=lambda: open_rhyme_window(win, root, lang_code="ta"),
                          width=350, height=60, radius=30,
                          bg="#009688", hover_bg="#00796B", fg="white").pack(pady=20)

    create_colored_button(win, "பின்வா", command=lambda: [win.destroy(), prev_win.deiconify()],
                          width=150, height=40, radius=20,
                          bg="#757575", hover_bg="#616161", fg="white").pack(pady=20)

def open_category_window_telugu(prev_win, root):
    prev_win.withdraw()

    win = tk.Toplevel()
    win.title("అధ్యయన మెనూ")
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFFACD")

    control_frame = tk.Frame(win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖", command=root.destroy,
                          width=60, height=40, radius=12,
                          bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=win.iconify,
                          width=60, height=40, radius=12,
                          bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(win, text="మీరు ఏమి చదవాలనుకుంటున్నారు?", font=("Segoe UI", 28, "bold"),
             bg="#FFFACD", fg="#263238").pack(pady=60)

    create_colored_button(win, "అక్షరాలు", command=lambda: open_letters_window(win, root, selected_lang_code='te'),
                          width=350, height=60, radius=30,
                          bg="#2196F3", hover_bg="#1976D2", fg="white").pack(pady=20)
    create_colored_button(win, "వ్యాకరణం", command=lambda: open_grammar_window(win, root, lang_code='te'),
                          width=350, height=60, radius=30,
                          bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)
    create_colored_button(win, "కథ", command=lambda: open_story_window(win, root, lang_code="te"),
                          width=350, height=60, radius=30,
                          bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)
    create_colored_button(win, "పాట", command=lambda: open_rhyme_window(win, root, lang_code="te"),
                          width=350, height=60, radius=30,
                          bg="#009688", hover_bg="#00796B", fg="white").pack(pady=20)

    create_colored_button(win, "వెనక్కి", command=lambda: [win.destroy(), prev_win.deiconify()],
                          width=150, height=40, radius=20,
                          bg="#757575", hover_bg="#616161", fg="white").pack(pady=20)

def open_category_window_kannada(prev_win, root):
    prev_win.withdraw()

    win = tk.Toplevel()
    win.title("ಅಧ್ಯಯನ ಮೆನು")
    win.attributes('-fullscreen', True)
    win.configure(bg="#FFFACD")

    control_frame = tk.Frame(win, bg="#FFFACD")
    control_frame.pack(fill='x', anchor='ne')

    create_colored_button(control_frame, "✖", command=root.destroy,
                          width=60, height=40, radius=12,
                          bg="#B71C1C", hover_bg="#D32F2F", fg="white").pack(side="right", padx=5, pady=5)
    create_colored_button(control_frame, "—", command=win.iconify,
                          width=60, height=40, radius=12,
                          bg="#1565C0", hover_bg="#1976D2", fg="white").pack(side="right", padx=5, pady=5)

    tk.Label(win, text="ನೀವು ಏನು ಅಧ್ಯಯನ ಮಾಡಲು ಇಚ್ಛಿಸುತ್ತೀರಿ?", font=("Segoe UI", 28, "bold"),
             bg="#FFFACD", fg="#263238").pack(pady=60)

    create_colored_button(win, "ಅಕ್ಷರಗಳು", command=lambda: open_letters_window(win, root, selected_lang_code='kn'),
                          width=350, height=60, radius=30,
                          bg="#2196F3", hover_bg="#1976D2", fg="white").pack(pady=20)
    create_colored_button(win, "ವ್ಯಾಕರಣ", command=lambda: open_grammar_window(win, root, lang_code='kn'),
                          width=350, height=60, radius=30,
                          bg="#FF5722", hover_bg="#E64A19", fg="white").pack(pady=20)
    create_colored_button(win, "ಕಥೆ", command=lambda: open_story_window(win, root, lang_code="kn"),
                          width=350, height=60, radius=30,
                          bg="#9C27B0", hover_bg="#7B1FA2", fg="white").pack(pady=20)
    create_colored_button(win, "ಪದ್ಯ", command=lambda: open_rhyme_window(win, root, lang_code="kn"),
                          width=350, height=60, radius=30,
                          bg="#009688", hover_bg="#00796B", fg="white").pack(pady=20)

    create_colored_button(win, "ಹಿಂದೆ", command=lambda: [win.destroy(), prev_win.deiconify()],
                          width=150, height=40, radius=20,
                          bg="#757575", hover_bg="#616161", fg="white").pack(pady=20)

if __name__ == "__main__":
    show_intro_window()
