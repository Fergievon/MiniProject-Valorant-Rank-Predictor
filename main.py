import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import random

class AimTrainer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Valorant Rank Predictor")
        self.geometry("1298x858")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")

        # Variables
        self.time_left = 30
        self.score = 0
        self.total_clicks = 0
        self.game_running = False

        self.main_canvas = tk.Canvas(self, width=1298, height=858, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)
        self.bg_image_raw = Image.open("ML-Project-BG.png").resize((1298, 858))
        self.bg_img = ImageTk.PhotoImage(self.bg_image_raw)
        self.main_canvas.create_image(0, 0, image=self.bg_img, anchor="nw")


        self.score_id = self.main_canvas.create_text(900, 23, text="0", fill="white", font=("Lexend", 20, "bold"))
        self.accuracy_id = self.main_canvas.create_text(1150, 23, text="0%", fill="white", font=("Lexend", 20, "bold"))
        self.timer_id = self.main_canvas.create_text(1060, 91, text="30s", fill="white", font=("Lexend", 22, "bold"))
        self.rank_id = self.main_canvas.create_text(780, 790, text="---", fill="#00FFFF", font=("Lexend", 20, "bold"))

        self.aim_canvas = tk.Canvas(self, width=910, height=535, bg="#0b1115", highlightthickness=0, bd=0)
        self.main_canvas.create_window(185, 165, anchor="nw", window=self.aim_canvas)
        self.aim_canvas.bind("<Button-1>", self.check_hit)

        self.start_button = ctk.CTkButton(
            self, 
            text="START", 
            font=("Lexend", 20, "bold"),
            command=self.start_game,
            fg_color="#1199AF", 
            hover_color="#086A79", 
            width=147, 
            height=40
        )
        self.main_canvas.create_window(167, 780, anchor="nw", window=self.start_button)


    def start_game(self):
        # Reset Game State
        self.time_left = 30
        self.score = 0
        self.total_clicks = 0
        self.game_running = True
        
        # Reset text if mag start
        self.main_canvas.itemconfig(self.score_id, text="0")
        self.main_canvas.itemconfig(self.accuracy_id, text="0%")
        self.main_canvas.itemconfig(self.rank_id, text="CALCULATING...")
        self.main_canvas.itemconfig(self.timer_id, text="30s")
        
        self.start_button.configure(state="disabled")
        self.spawn_circle()
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.game_running:
            self.time_left -= 1
            self.main_canvas.itemconfig(self.timer_id, text=f"{self.time_left}s")
            self.after(1000, self.update_timer)
        else:
            self.end_game()

    def spawn_circle(self):
        self.aim_canvas.delete("target")
        if self.game_running:
            x = random.randint(40, 870)
            y = random.randint(40, 490)
            r = 20
            self.aim_canvas.create_oval(
                x-r, y-r, x+r, y+r, 
                fill="#ff4655", outline="white", width=2, tags="target"
            )

    #Only problem is whenever mag click siya sa canvas, iconsider niya as a hit
    def check_hit(self, event):
        if not self.game_running:
            return

        self.total_clicks += 1
        clicked_item = self.aim_canvas.find_closest(event.x, event.y)
        
        if "target" in self.aim_canvas.gettags(clicked_item):
            self.score += 1
            # Update Score 
            self.main_canvas.itemconfig(self.score_id, text=str(self.score))
            self.spawn_circle()
        
        # Update Accuracy
        accuracy = (self.score / self.total_clicks) * 100
        self.main_canvas.itemconfig(self.accuracy_id, text=f"{int(accuracy)}%")

    #Diri na part mon, pwede ra ni siya tanggalon/ replace with ML
    def end_game(self):
        self.game_running = False
        self.aim_canvas.delete("target")
        self.start_button.configure(state="normal")
        self.main_canvas.itemconfig(self.timer_id, text="0s")
        
        if self.score > 35:
            rank = "DIAMOND"
        elif self.score > 20:
            rank = "GOLD"
        else:
            rank = "BRONZE"
        
        self.main_canvas.itemconfig(self.rank_id, text=rank)
        print(f"Test Finished. Score: {self.score}, Accuracy: {int((self.score/self.total_clicks)*100)}%")

if __name__ == "__main__":
    app = AimTrainer()
    app.mainloop()