# coding: utf-8
#https://github.com/nekoy3/raspi-nfc-botより
import configparser
import traceback
import os

class ConfigClass():
    cfg = configparser.ConfigParser(comment_prefixes='#', allow_no_value=True)
    def create_config(self):
        self.cfg.read('config.ini', encoding="utf-8")

        self.cfg.add_section('login')
        self.cfg.set('login', '# e-learningの名前を入力')
        self.cfg.set('login', 'name', 'xxx')
        self.cfg.set('login', '# e-learningのパスワードを入力(値をterminalにすることでコンソール上から入力することが出来る。）')
        self.cfg.set('login', 'password', 'xxx')

        with open('config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def read_config(self):
        try:
            self.cfg.read('config.ini')

            self.name = self.cfg['login']['name']
            self.password = self.cfg['login']['password']

            if self.name == 'xxx' or self.password == 'xxx':
                raise ValueError("いずれかの値が初期値になっているので修正してください。")
                
        except Exception as e:
            print("config.iniが存在しないか、設定が間違っています。\n" + traceback.format_exc())
            #ファイルの存在確認(カレントディレクトリにconfig.iniがあるか)
            if not os.path.isfile('config.ini'):
                self.create_config()
            exit()
        else:
            return self.cfg