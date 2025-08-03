import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import webbrowser
import speech_recognition as sr
from tkinter import messagebox
import threading

try:
    from googlesearch import search
except ImportError:
    messagebox.showerror("Module Missing", "Install googlesearch-python:\npip install googlesearch-python==1.1")


def callback(url):
    webbrowser.open_new_tab(url)

def search_query():
    query = text.get("1.0", "end-1c").strip().replace(" ", "+")
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    if query:
        try:
            results = list(search(query))
            for url in results:
                webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred:\n{e}")


def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("🎙️ Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            print(" Recognizing...")
            query = recognizer.recognize_google(audio)
            text.delete("1.0", tk.END)
            text.insert(tk.END, query)
            search_query()
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand your speech.")
        except sr.RequestError:
            messagebox.showerror("Error", "Speech recognition service failed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Google Voice Search")
root.geometry("1000x700")
root.configure(bg="white")


top_bar = Label(root, bg="black", width=500, height=2)
top_bar.grid(row=0, column=0, sticky="w")


def add_icon_and_label(image_path, text, x, url):
    try:
        icon_img = ImageTk.PhotoImage(Image.open(image_path).resize((20, 20)))
        icon_lbl = Label(root, image=icon_img, borderwidth=0, bg="black")
        icon_lbl.image = icon_img
        icon_lbl.place(x=x, y=10)
        lbl = Label(root, text=text, bg="black", fg="white", cursor="hand2")
        lbl.place(x=x + 25, y=10)
        lbl.bind("<Button-1>", lambda e: callback(url))
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")

add_icon_and_label("Images/apps.png", "Apps", 13, "https://about.google/intl/en/products/")
add_icon_and_label("Images/drive.png", "Google Drive", 85, "https://drive.google.com/")
add_icon_and_label("Images/youtube.png", "YouTube", 210, "https://www.youtube.com/")
add_icon_and_label("Images/gmail.png", "Gmail", 315, "https://mail.google.com/")


g_word = Label(root, text="Gmail", cursor="hand2", bg="white")
g_word.place(x=810, y=55)
g_word.bind("<Button-1>", lambda e: callback("https://mail.google.com/"))

i_word = Label(root, text="Images", cursor="hand2", bg="white")
i_word.place(x=850, y=55)
i_word.bind("<Button-1>", lambda e: callback("https://www.google.com/imghp"))

signinb = Button(root, text="Sign In", font=('Roboto', 10, 'bold'), bg="#4583EC", fg="white", cursor="hand2")
signinb.place(x=920, y=50)
signinb.bind("<Button-1>", lambda e: callback("https://accounts.google.com/signin"))


try:
    g_logo = ImageTk.PhotoImage(Image.open('Images/google.png').resize((300, 100)))
    logo_lbl = Label(root, image=g_logo, bg="white")
    logo_lbl.place(x=350, y=150)
except Exception as e:
    print("Google logo error:", e)


text = Text(root, width=90, height=2, relief=RIDGE, font=('Roboto', 10, 'bold'), borderwidth=2)
text.place(x=170, y=280)


search_btn = Button(root, text="Google Search", relief=RIDGE, font=('Arial', 10), bg="#F3F3F3", fg="#222222", cursor="hand2",
                    command=lambda: threading.Thread(target=search_query).start())
search_btn.place(x=350, y=330)

lucky_btn = Button(root, text="I'm Feeling Lucky", relief=RIDGE, font=('Arial', 10), bg="#F3F3F3", fg="#222222", cursor="hand2")
lucky_btn.place(x=500, y=330)
lucky_btn.bind("<Button-1>", lambda e: callback("https://www.google.com/doodles"))

mic_btn = Button(root, text="🎤 Speak", relief=RIDGE, font=('Arial', 10), bg="#F3F3F3", fg="#222222", cursor="hand2",
                 command=lambda: threading.Thread(target=voice_search).start())
mic_btn.place(x=660, y=330)

offered = Label(root, text="Google offered in:", bg="white")
offered.place(x=240, y=380)
lang = Label(root, text="हिंदी বাংলা తెలుగు मराठी தமிழ் ગુજરાતી ಕನ್ನಡ മലയാളം ਪੰਜਾਬੀ", fg="blue", bg="white")
lang.place(x=350, y=380)


def add_footer_label(text, x, url):
    lbl = Label(root, text=text, cursor="hand2", bg="white")
    lbl.place(x=x, y=650)
    lbl.bind("<Button-1>", lambda e: callback(url))

add_footer_label("About", 50, "https://about.google/")
add_footer_label("Advertising", 110, "https://ads.google.com/")
add_footer_label("Business", 200, "https://www.google.com/business/")
add_footer_label("How Search works", 280, "https://www.google.com/search/howsearchworks/")
add_footer_label("Privacy", 850, "https://policies.google.com/privacy")
add_footer_label("Terms", 920, "https://policies.google.com/terms")

root.mainloop()
