# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
from tkinter import messagebox
import turtle, random

def choose_role(): #to choose the player's role
        role_window = tk.Tk()
        role_window.title("Choose Role")
        role_window.geometry("300x200")
        role_window.configure(bg="#7AB276")
        
        selected_role = tk.StringVar()
        
        tk.Label(role_window, text="Choose your role:\n\nChaser: Reach 100 points\nRunner: Survive for 30 seconds").pack(pady=10)
        
        tk.Button(
            role_window, text="Runner", command=lambda: [selected_role.set("runner"),role_window.destroy()]
            ).pack()
        
        tk.Button(
            role_window, text="Chaser", command=lambda: [selected_role.set("chaser"),role_window.destroy()]
            ).pack()
        
        role_window.mainloop()
        return selected_role.get()
    
class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        
        
        self.score = 0
        self.target_score = 50
        self.heart = 3
        self.time_left = 30
        self.game_over = False
        self.role = None
        
        self.hud = turtle.RawTurtle(canvas)
        self.hud.hideturtle()
        self.hud.penup()


    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.update_hud()
        self.canvas.ontimer(self.countdown, 1000)
        self.canvas.ontimer(self.step, self.ai_timer_msec)
    
    def update_hud(self):
        self.hud.clear()
        self.hud.goto(-330, 320)

        if self.role == "runner":
            hearts = "❤️" * self.heart
            self.hud.write(
                f"Time: {self.time_left}   Lives: {hearts}",
                font=("Arial",16,"bold")
            )
        else:
            self.hud.write(
                f"Score: {self.score}/{self.target_score}   Time: {self.time_left}",
                font=("Arial",16,"bold")
            )
    
    def countdown(self):
        if self.game_over:
            return

        self.time_left -= 1
        self.update_hud()
        
        if self.time_left <= 0:

            if self.role == "runner":
                self.end_game(True)

            else:
                self.end_game(False)
        else:
            self.canvas.ontimer(self.countdown, 1000)
            
    def step(self):
        if self.game_over:
            return
        
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        is_catched = self.is_catched()
        if self.is_catched():
            if self.role == "chaser":
                self.score += 10
                self.runner.goto(
                    random.randint(-250,250),
                    random.randint(-250,250)
                )
                while self.runner.distance(self.chaser) < 100:
                    self.runner.goto(
                        random.randint(-250,250),
                        random.randint(-250,250)
                    )

                if self.score >= self.target_score:
                    self.end_game(True)
                    return
            else:
                self.heart -= 1
                self.runner.goto(
                    random.randint(-250,250),
                    random.randint(-250,250)
                )

                while self.runner.distance(self.chaser) < 100:
                    self.runner.goto(
                        random.randint(-250,250),
                        random.randint(-250,250)
                    )

                if self.heart <= 0:
                    self.end_game(False)
                    return


        self.update_hud()
        self.drawer.clear()
        self.drawer.penup()
        self.drawer.setpos(-300,300)

        if self.role == "chaser":

            self.drawer.write(
                f"Target Score: {self.target_score}",
                font=("Arial",12,"bold")
            )

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)
    
    def end_game(self, win):
        self.game_over = True

        if win:
            result = "YOU WON!!! 🎉"
        else:
            result = "YOU LOST!!! 😢"

        if self.role == "runner":
            message = f"Lives Remaining: {self.heart}"
        else:
            message = f"Final Score: {self.score}"

        messagebox.showinfo(
            result,
            message
        )

        self.canvas.bye()
        
            
class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)

        self.step_move = step_move
        self.step_turn = step_turn

        canvas.onkeypress(self.move_forward, 'Up')
        canvas.onkeypress(self.move_backward, 'Down')
        canvas.onkeypress(self.turn_left, 'Left')
        canvas.onkeypress(self.turn_right, 'Right')
        canvas.listen()

    def stay_in_bounds(self):
        x = self.xcor()
        y = self.ycor()

        x = max(-320, min(320, x))
        y = max(-320, min(320, y))

        self.goto(x, y)

    def move_forward(self):
        self.forward(self.step_move)
        self.stay_in_bounds()

    def move_backward(self):
        self.backward(self.step_move)
        self.stay_in_bounds()

    def turn_left(self):
        self.left(self.step_turn)

    def turn_right(self):
        self.right(self.step_turn)

    def run_ai(self, opp_pos, opp_heading):
        pass
        

class RandomRunner(turtle.RawTurtle):

    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)

        self.step_move = step_move
        self.step_turn = step_turn

    def stay_in_bounds(self):
        x = self.xcor()
        y = self.ycor()

        x = max(-320, min(320, x))
        y = max(-320, min(320, y))

        self.goto(x, y)

    def run_ai(self, opp_pos, opp_heading):

        distance = self.distance(opp_pos)

        if distance < 150:

            angle = self.towards(opp_pos)

            self.setheading(angle + 180)

            self.forward(20)

        else:

            self.forward(10)

            if random.randint(0, 10) == 0:
                self.left(random.randint(-45, 45))

        self.stay_in_bounds()
        
class ChaserAI(turtle.RawTurtle):
    def run_ai(self,opp_pos,opp_heading):
        angle = self.towards(opp_pos)
        self.setheading(angle)
        self.forward(15)
        self.stay_in_bounds()
    
    def stay_in_bounds(self):
        x = self.xcor()
        y = self.ycor()

        x = max(-320, min(320, x))
        y = max(-320, min(320, y))

        self.goto(x, y)
       
        
if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    
    role = choose_role()
    root = tk.Tk()
    root.title("Turtle Runaway Game")
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("#A8E6A3")   
    border = turtle.RawTurtle(screen)
    border.hideturtle()
    border.speed(0)
    border.pensize(4)

    border.penup()
    border.goto(-320, -320)
    border.pendown()

    for _ in range(4):
        border.forward(640)
        border.left(90)

    if role == "runner":
        runner = ManualMover(screen)
        chaser= ChaserAI(screen)
    else:
        runner = RandomRunner(screen)
        chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.role = role
    
    game.start()
    screen.mainloop()
