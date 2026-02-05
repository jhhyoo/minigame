import tkinter as tk
import random

# -------------------
# Настройки
# -------------------
WINDOW_SIZE = 400
CELL_SIZE = 100
GAME_TIME = 30
CLIENT_MIN = 6
CLIENT_MAX = 8
INGREDIENTS = ["サラダ", "チーズ", "トマト"]
ALL_INGREDIENTS = ["トースト"] + INGREDIENTS

# -------------------
# Состояние игры
# -------------------
player_pos = 0
order = []
sandwich = []
score = 0
game_time = GAME_TIME
client_time = 0
game_active = True
timer_job = None

# -------------------
# Логика
# -------------------
def generate_order():
    length = random.randint(4, 8)
    middle = [random.choice(INGREDIENTS) for i in range(length - 2)]
    return ["トースト"] + middle + ["トースト"]

def new_client():
    global order, sandwich, client_time
    order = generate_order()
    sandwich = []
    client_time = random.randint(CLIENT_MIN, CLIENT_MAX)
    draw_all()

def choose_ingredient():
    global sandwich, score
    if not game_active:
        return
    ingredient = ALL_INGREDIENTS[player_pos]

    # Ошибка: тост в середине
    if ingredient == "トースト" and len(sandwich) > 0 and len(sandwich) < len(order) - 1:
        new_client()
        return

    sandwich.append(ingredient)

    # Проверка готовности
    if len(sandwich) == len(order):
        if sandwich == order:
            score += 1
        new_client()

    draw_all()

def remove_last_ingredient(event=None):
    if not game_active:
        return
    if len(sandwich) > 0:
        sandwich.pop()
        draw_all()

def move_left(event=None):
    global player_pos
    if not game_active:
        return
    if player_pos > 0:
        player_pos -= 1
        draw_all()

def move_right(event=None):
    global player_pos
    if not game_active:
        return
    if player_pos < len(ALL_INGREDIENTS) - 1:
        player_pos += 1
        draw_all()

def move_up(event=None):
    if game_active:
        choose_ingredient()

# -------------------
# Таймеры
# -------------------
def update_timers():
    global game_time, client_time, timer_job
    if not game_active:
        timer_job = None
        return

    game_time -= 1
    client_time -= 1

    if client_time <= 0:
        new_client()

    if game_time <= 0:
        game_over()
        timer_job = None
        return

    draw_all()
    timer_job = root.after(1000, update_timers)

def game_over():
    global game_active
    game_active = False
    canvas.delete("all")
    canvas.create_text(WINDOW_SIZE//2, WINDOW_SIZE//2,
                       text=f"時間切れ！\nスコア： {score}\nRで再挑戦",
                       font=("Arial", 16), fill="black")

def restart(event=None):
    global score, game_time, game_active, timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    score = 0
    game_time = GAME_TIME
    game_active = True
    new_client()
    draw_all()
    timer_job = root.after(1000, update_timers)

# -------------------
# Отрисовка
# -------------------
def draw_all():
    canvas.delete("all")

    # Фон
    canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill="white")

    # Сетка
    for i in range(0, WINDOW_SIZE, CELL_SIZE):
        canvas.create_line(i, 0, i, WINDOW_SIZE, fill="lightgrey")
        canvas.create_line(0, i, WINDOW_SIZE, i, fill="lightgrey")

    # Столы (ряд 3, серый прямоугольник, сверху картинка ингредиента)
    for i, ing in enumerate(ALL_INGREDIENTS):
        x = i * CELL_SIZE
        y = 2 * CELL_SIZE

        # Серый "стол"
        canvas.create_rectangle(x+15, y+10, x+85, y+80, fill="lightgrey", outline="black")

        # Картинка ингредиента поверх
        canvas.create_image(x+50, y+45, image=images[ing])

        # Название под столом
        canvas.create_text(x+50, y+90, text=ing, font=("Arial", 10))

    # Персонаж (ряд 4)
    canvas.create_image(player_pos*CELL_SIZE+50, 3*CELL_SIZE+45, image=images["キャラクター"])

    # Заказ (верхний левый угол 2x2)
    for i, ing in enumerate(order):
        canvas.create_image(50, CELL_SIZE+60 - i*10, image=images[ing])

    # Собранный сэндвич (правое поле)
    for i, ing in enumerate(sandwich):
        canvas.create_image(CELL_SIZE+50, CELL_SIZE+60 - i*10, image=images[ing])

    # Клиент (ряд 2 справа)
    canvas.create_image(2*CELL_SIZE+50, CELL_SIZE+30, image=images["クライアント"])

    # Шкала времени клиента
    bar_width = (client_time / CLIENT_MAX) * 60
    canvas.create_rectangle(2*CELL_SIZE+20, 80, 2*CELL_SIZE+20+bar_width, 90, fill="orange")

    # Счёт, таймер и заказ
    canvas.create_text(WINDOW_SIZE-120, 20, text=f"スコア： {score}", font=("Arial", 14), anchor="w")
    canvas.create_text(WINDOW_SIZE-120, 45, text=f"タイム： {game_time}", font=("Arial", 14), anchor="w")
    canvas.create_text(WINDOW_SIZE-350, 45, text=f"オーダー", font=("Arial", 14))

# -------------------
# Запуск
# -------------------
root = tk.Tk()
root.title("サンドイッチ")

canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
canvas.pack()

# -------------------
# Загрузка изображений
# -------------------
images = {
    "トースト": tk.PhotoImage(file="images/tost.png"),
    "サラダ": tk.PhotoImage(file="images/salad.png"),
    "チーズ": tk.PhotoImage(file="images/cheese.png"),
    "トマト": tk.PhotoImage(file="images/tomato.png"),
    "クライアント": tk.PhotoImage(file="images/client.png"),
    "キャラクター": tk.PhotoImage(file="images/character.png")
}

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Up>", move_up)
root.bind("<Down>", remove_last_ingredient)
root.bind("r", restart)

# Старт
new_client()
draw_all()
root.after(1000, update_timers)

root.mainloop()
