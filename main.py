import customtkinter as ctk
import tkinter as tk
import random
from PIL import Image

class AimTrainer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Valorant Rank Predictor")
        self.geometry("1298x858")
        ctk.set_appearance_mode("Dark")

        img = Image.open("ML-Project-BG.png")
        Background_image = ctk.CTkImage(img, size=(1298,858))
        bg_label = ctk.CTkLabel(self, text="", image= Background_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #time stuff here + make variables
        self.time_left = 30
        self.score = 0
        self.game_running = False

        self.timer_label = ctk.CTkLabel(self, text=f"Time: {self.time_left}s", font=("Arial", 20), bg_color="transparent")
        self.timer_label.pack(pady=10)

        self.score_label = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 20), bg_color="transparent")
        self.score_label.pack(pady=5)

        self.canvas = tk.Canvas(self, width=956, height=580, bg="#111111", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.check_hit)

        self.start_button = ctk.CTkButton(self, text="START TEST", command=self.start_game)
        self.start_button.pack(pady=10)

        self.target = None

    def start_game(self):
        self.time_left = 30
        self.score = 0
        self.game_running = True
        self.score_label.configure(text="Score: 0")
        self.start_button.configure(state="disabled") #double clicks handle
        self.spawn_circle()
        self.update_timer() #start na ang 30 seconds na time

    def update_timer(self):
        if self.time_left > 0 and self.game_running:
            self.time_left -= 1
            self.timer_label.configure(text=f"Time: {self.time_left}s")

            self.after(1000, self.update_timer)
        else:
            self.end_game()

    def spawn_circle(self):
        self.canvas.delete("target")

        x = random.randint(50, 550)
        y = random.randint(50, 350)
        r = 20

        self.target = self.canvas.create_oval(
            x-r, y-r, x+r, y+r, 
            fill="#ff4655", outline="white", width=2, tags="target"
        )

    def check_hit(self, event):
        if not self.game_running:
            return

        clicked_item = self.canvas.find_closest(event.x, event.y)
        if "target" in self.canvas.gettags(clicked_item):
            self.score += 1
            self.score_label.configure(text=f"Score: {self.score}")
            self.spawn_circle()

    def end_game(self):
        self.game_running = False
        self.canvas.delete("target")
        self.start_button.configure(state="normal")
        self.timer_label.configure(text="GAME OVER")
        print(f"Final Score: {self.score}")

if __name__ == "__main__":
    app = AimTrainer()
    app.mainloop()