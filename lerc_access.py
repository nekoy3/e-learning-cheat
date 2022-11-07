from selenium import webdriver
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from functools import wraps


class BrowserClass:
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    #ドライバーを準備するメソッド
    def make_driver_process(self) -> webdriver.Chrome:
        #ChromeOptionsクラスのインスタンスを生成して、それにオプションを追加する
        options = webdriver.ChromeOptions()
        
        #ヘッドレスモードで起動する（バックグラウンドで実行するようになる）
        #options.add_argument("--headless")
        
        #ドライバのパスを指定
        chrome_service = fs.Service(executable_path='./driver/chromedriver.exe')

        #ドライバのパスとオプションを設定してChromeのインスタンスを生成
        chrome = webdriver.Chrome(service=chrome_service, options=options)

        #タイムアウトを10秒で設定、読み込み終わるまで待機する
        chrome.implicitly_wait(10) 

        return chrome
    
    #全てのウィンドウを閉じてドライバを終了する
    def exit_chrome(self):
        self.chrome.quit()

    #ログイン処理等をこなしてトップ画面まで遷移する
    def e_learning_access(self):
        #webdriver読み込んでドライバをフィールドにセットする
        self.chrome = self.make_driver_process()

        #e-learningログイン前画面に移動
        self.chrome.get("https://languagelab.ip.kyusan-u.ac.jp/")
       
        #ログイン画面で値を入力する
        try:
            self.chrome.find_element(By.ID, "username").send_keys(self.name)
            self.chrome.find_element(By.ID, "password").send_keys(self.password)
            self.chrome.find_element(By.ID, "loginbtn").click()
        except: 
            print("ログイン画面に到達できませんでした。時間を空けて再度お試しください。")
            raise Exception("ログイン画面到達不可")
    
        #サインインボタンを押した後ホーム画面に遷移するまでの処理
        try: #e-learning画面のid=page-site-indexがあれば正常遷移
            self.chrome.find_element(By.ID, "page-site-index")
        except:
            try: 
                self.chrome.find_element(By.ID, "loginerrormessage")
            except:
                print("ホーム画面にたどり着けませんでした。メンテナンス等の原因が考えられるため、手動で確認してください。\n" + traceback.format_exc())
                raise Exception("ホーム画面到達不可")
            else:
                print("ログインに失敗しました。IDかパスワードを間違えている可能性があります。config.iniを確認して再度お試しください。")
                raise Exception("ログイン失敗")
        else:
            print("正常にホーム画面に遷移しました。")
    
    #ログアウトボタンを押してウィンドウを閉じる
    def logout_elearning_and_close_window(self):
        print("please wait...")
        self.chrome.find_element(By.XPATH, "//*[@id=\"header-navi\"]/p/a[2]").click()
        #ダイアログが表示されるのでOKボタンを押す
        Alert(self.chrome).accept()
        self.chrome.close()