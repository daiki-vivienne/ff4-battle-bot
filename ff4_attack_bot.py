import pyautogui
import time
import keyboard

# 少し待ってから処理を始める（FF4にフォーカスする時間用）
time.sleep(3)

## 画像の中心位置を取得する関数
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
#
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

def use_potion():
    print("ポーションで回復します。")

    # if not safe_locate("cecil_hplow.png", confidence=0.6):
    #     print("（処理開始前）セシルのHPは回復済みっぽいので何もしません")
    #     return False

    #戦闘メニューからアイテムを選択
    pyautogui.press("down")
    time.sleep(0.2)
    pyautogui.press("down")
    time.sleep(0.2)
    pyautogui.press("Enter")
    time.sleep(0.2)

    #ポーションを探して選択
    potion_btn = safe_locate("potion.png",confidence=0.6)
    if not potion_btn:
        print("ポーションが見つかりません")
        pyautogui.press("backspace")
        return False
        
    pyautogui.moveTo(pyautogui.center(potion_btn))
    time.sleep(0.2)
    pyautogui.click() 
    time.sleep(0.2)
    
    
    #回復対象のキャラを選ぶ
    target = safe_locate("cecil_hplow.png")
    if not target:
        print("回復対象が見つかりません。回復を中止します。")
    
    # 戻るキーを複数回押して、メニューから脱出（連打で保険）
        pyautogui.press("backspace")
        time.sleep(0.3)
        pyautogui.press("backspace")
        time.sleep(0.3)
        return False
    
    #回復対象をクリック
    pyautogui.moveTo(pyautogui.center(target))
    time.sleep(0.2)
    pyautogui.click() 
    time.sleep(0.2)
    pyautogui.click() 
    time.sleep(0.5)     
    # HP画像が消えるまで最大5回確認
    for i in range(10):
        if not safe_locate("cecil_hplow.png", confidence=0.6):
            break
        print(f"セシル画像まだある（{i+1}回目）")
        time.sleep(0.5)
    return True
    # target = safe_locate("kain_hplow.png")
    # if target:
    #     pyautogui.moveTo(pyautogui.center(target))
    #     time.sleep(0.2)
    #     pyautogui.click() 
    #     time.sleep(0.2)
    #     pyautogui.press("Enter")
    #     return True
    

def is_hp_low():
    print("HPが減っているキャラクターの画像を探します")

    # 少し待ってから画像確認（画面更新待ち）
    time.sleep(0.3)

    cecil_hplow = safe_locate("cecil_hplow.png",confidence=0.6)

    if cecil_hplow:
        print("セシルのHPが減っていると判断されました")
        return use_potion()
    else: 
        print("セシルのHPは正常です")
        return False

def do_battle():
    print("戦闘開始：攻撃ループに入ります。")
    while not safe_locate("victory.png"):
        if keyboard.is_pressed("esc"):
            print("ESCが押されたので戦闘中に強制停止します")
            exit()  # プログラム全体を終了（中断）

        if is_hp_low():
            print("回復しました")
            continue

        atk_btn = safe_locate("attack_button.png")
        if atk_btn:
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
    if keyboard.is_pressed("esc"):
        print("ESCが押されたので強制停止します")
        break  # while True から脱出してBot終了

    for i in range(50):
        wait_for_battle_start()

        if keyboard.is_pressed("esc"):
            print("ESCが押されたので強制停止します")
            break  

        do_battle()
        print(f"{i+1}回目の戦闘完了")
        time.sleep(1)  # 次の移動開始前に小休止




