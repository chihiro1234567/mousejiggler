from machine import Pin
import time
import urandom as random
'''
Pico GP18 → ULN2003 IN1
Pico GP19 → ULN2003 IN2
Pico GP20 → ULN2003 IN3
Pico GP21 → ULN2003 IN4

Pico VBUS → ULN2003 + (5V)
Pico GND → ULN2003 - (GND)
'''
# 動作の間隔（秒）
SLEEP_SECONDS = 10
# 512ステップで1周 360deg
STEP_COUNT=int(512/4)
# ステップ間の遅延（ms）
DELAY_MS = 10

# --- ピンの定義 ---
pin_in1 = Pin(18, Pin.OUT)
pin_in2 = Pin(19, Pin.OUT)
pin_in3 = Pin(20, Pin.OUT)
pin_in4 = Pin(21, Pin.OUT)

# --- 励磁パターンの定義 ---
# 1seq: 1相励磁
SEQUENCE1 = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]
# 2seq: 2相励磁
SEQUENCE2 = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
]
CURRENT_SEQUENCE = SEQUENCE1

def all_off():
    pin_in1.value(0)
    pin_in2.value(0)
    pin_in3.value(0)
    pin_in4.value(0)

def step_motor(steps, delay_ms=5, reverse=False):
    """
    reverse: Trueの場合、逆回転
    """
    # 既存のロジックを崩さず、一時的に反転させたリストを使用
    seq = CURRENT_SEQUENCE if not reverse else CURRENT_SEQUENCE[::-1]
    
    for _ in range(steps):
        for phase in seq:
            pin_in1.value(phase[0])
            pin_in2.value(phase[1])
            pin_in3.value(phase[2])
            pin_in4.value(phase[3])
            time.sleep_ms(delay_ms)
    
    all_off()

# --- メイン処理 ---
print("Mouse Jiggler Started (Random Mode)")
all_off()

while True:
    try:
        # --- ここからランダム化 ---
        # 1. 回転方向のランダム (True: 逆回転 / False: 正回転)
        is_reverse = random.choice([True, False])
        
        # 2. ステップ数のランダム (元々の STEP_COUNT を基準に 0.5倍〜2.0倍の幅)
        rand_steps = random.randint(int(STEP_COUNT * 0.5), int(STEP_COUNT * 4.0))
        
        # 3. ディレイのランダム
        rand_delay = random.randint(int(DELAY_MS * 0.3), int(DELAY_MS * 5))
        print("Stepping %d steps, Delay %d ms, Reverse: %s" % (rand_steps, rand_delay, is_reverse))
        # 実行
        step_motor(rand_steps, rand_delay, is_reverse)
        
        rand_sleep = random.randint(int(SLEEP_SECONDS * 0.2), int(SLEEP_SECONDS * 10.0))

        print("Wait %d seconds..." % rand_sleep)
        time.sleep(rand_sleep)
        
    except KeyboardInterrupt:
        all_off()
        print("Stopped by user.")
        break