import customtkinter as ctk
import tkinter as tk
import random
from PIL import Image

class AimTrainer(ctk.CTk):
    def __init__(self):
        super().__init__()
        #self is like the mother container bai, call this when calling a variable
        self.title("Valorant Rank Predictor")
        self.geometry("1298x858")
        self.resizable(False, False)

        img = Image.open("ML-Project-BG.png") 
        Background_image = ctk.CTkImage(img, size=(1298, 858))
        self.bg_label = ctk.CTkLabel(self, text="", image=Background_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Variables
        self.time_left = 30
        self.score = 0
        self.total_clicks = 0
        self.game_running = False

        self.score_label = ctk.CTkLabel(self.bg_label, text="0", font=("Arial", 24, "bold"), 
                                        bg_color="transparent", text_color="#FFFFFF")
        self.score_label.place(x=900, y=9) 

        self.accuracy_label = ctk.CTkLabel(self.bg_label, text="0%", font=("Arial", 24, "bold"), 
                                           bg_color="transparent", text_color="#FFFFFF")
        self.accuracy_label.place(x=1150, y=9)

        self.timer_label = ctk.CTkLabel(self.bg_label, text="30s", font=("Arial", 22, "bold"), 
                                        bg_color="transparent", text_color="#FFFFFF")
        self.timer_label.place(x=1044, y=78)

        self.rank_result = ctk.CTkLabel(self.bg_label, text="---", font=("Arial", 28, "bold"), 
                                        bg_color="transparent", text_color="#00FFFF")
        self.rank_result.place(x=830, y=805)

        self.canvas = tk.Canvas(self.bg_label, width=910, height=535, bg="#0b1115", 
                                highlightthickness=0, bd=0)
        self.canvas.place(x=185, y=165)
        self.canvas.bind("<Button-1>", self.check_hit)

        self.start_button = ctk.CTkButton(self, text="", 
                                          command=self.start_game,
                                          fg_color="transparent", 
                                          hover_color="#1199AF", 
                                          width=147, height=40)
        self.start_button.place(x=167, y=780)

    def start_game(self):
        self.time_left = 30
        self.score = 0
        self.total_clicks = 0
        self.game_running = True
        self.score_label.configure(text="0")
        self.accuracy_label.configure(text="0%")
        self.rank_result.configure(text="CALCULATING...")
        self.start_button.configure(state="disabled")
        
        self.spawn_circle()
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.game_running:
            self.time_left -= 1
            self.timer_label.configure(text=f"{self.time_left}s")
            self.after(1000, self.update_timer)
        else:
            self.end_game()

    def spawn_circle(self):
        self.canvas.delete("target")
        if self.game_running:
            x = random.randint(40, 870)
            y = random.randint(40, 490)
            r = 20
            self.canvas.create_oval(x-r, y-r, x+r, y+r, 
                                   fill="#ff4655", outline="white", width=2, tags="target")

    def check_hit(self, event):
        if not self.game_running:
            return

        self.total_clicks += 1
        clicked_item = self.canvas.find_closest(event.x, event.y)
        
        if "target" in self.canvas.gettags(clicked_item):
            self.score += 1
            self.score_label.configure(text=str(self.score))
            self.spawn_circle()
        
        # calculate the accuracy, just change if naa nay data
        accuracy = (self.score / self.total_clicks) * 100
        self.accuracy_label.configure(text=f"{int(accuracy)}%")


    # for GUI testing lang ito mon, if ano mukha ng rank text -remove lng or change
    def end_game(self):
        self.game_running = False
        self.canvas.delete("target")
        self.start_button.configure(state="normal")
        self.timer_label.configure(text="0s")
        
        # Simple Logic for now to show it works
        if self.score > 30:
            self.rank_result.configure(text="DIAMOND")
        elif self.score > 15:
            self.rank_result.configure(text="GOLD")
        else:
            self.rank_result.configure(text="BRONZE")

if __name__ == "__main__":
    app = AimTrainer()
    app.mainloop()