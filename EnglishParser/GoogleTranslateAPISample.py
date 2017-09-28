from googletrans import Translator
translator = Translator()
res = translator.translate("hello",dest='ru')
print(res.text)
