# coding: utf-8
from getpass import getpass

from cfg_rw import ConfigClass
from lerc_access import BrowserClass

configs = ConfigClass().read_config()
if configs['login']['password'] == 'terminal':
    configs['login']['password'] = getpass('パスワードを入力・・・: ')

e_learning = BrowserClass(configs['login']['name'], configs['login']['password'])
e_learning.e_learning_access()