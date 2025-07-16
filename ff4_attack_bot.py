import pyautogui
import time

# 少し待ってから処理を始める（FF4にフォーカスする時間用）
time.sleep(3)

## "たたかう"画像の中心位置を取得
def safe_locate(image,confidence=0.7):
    try:
        return pyautogui.locateOnScreen(image,confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None
    except Exception as e:
        print(f"画像認識エラー: {e}")
        return None

def is_battle_started():
    # セシル or ATB が出てたら、戦闘始まってるかも？
    cecil = safe_locate("cecil_battle.png", confidence=0.7)
    atb = safe_locate("atb_frame.png", confidence=0.6)

    if cecil or atb:
        print("セシル or ATB を検出 → 攻撃ボタン待機フェーズへ")

        # 💡最大4.2秒間、攻撃ボタンが出るのを6回まで再チェック
        for i in range(7):
            attack = safe_locate("attack_button.png", confidence=0.65)
            if attack:
                print(f"攻撃ボタン: True（{i+1}回目で検出）")
                return True
            time.sleep(0.7)  # 少し待ってもう一回確認

        print("攻撃ボタン: False（5回チェックしても見つからず）")
        return False
    return False

def wait_for_battle_start():
    while True: 
        if is_battle_started():
            pyautogui.keyUp("a")
            pyautogui.keyUp("d")
            print("戦闘突入")
            break
        pyautogui.keyDown("a")
        time.sleep(0.3)
        pyautogui.keyUp("a")
        pyautogui.keyDown("d")
        time.sleep(0.3)
        pyautogui.keyUp("d")
        time.sleep(0.5)

def do_battle():
    print("戦闘開始：攻撃ループに入ります。")
    while not safe_locate("victory.png"):
        atk_btn = safe_locate("attack_button.png")
        if  atk_btn:
            pyautogui.press("enter")  # たたかう
            time.sleep(0.5)
            pyautogui.press("enter")  # 敵を攻撃
            print("攻撃しました！")
        else:
            print("たたかうボタンが見つかりません。(戦闘中)")
        time.sleep(0.7)  # 次のループまで待機
    print("戦闘勝利画面を検出しました。")
    for i in range(5):
        pyautogui.press('enter')
        print(f"戦闘後のEnter送信 {i+1}回目")
        time.sleep(0.7)

while True:
    for i in range(50):
        wait_for_battle_start()
        do_battle()
        print(f"{i+1}回目の戦闘完了")
        time.sleep(1)  # 次の移動開始前に小休止




