#2021/07/19

from WebUiKey.Keys import Key


key = Key('Chrome')
key.open('https://www.baidu.com/')
key.input('id', 'kw', '李宇春')
key.click('id', 'su')
