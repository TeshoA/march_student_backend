import re

def titlecase(s):
         return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(), s)


print('hello')

some_text = "victoria's fourth blog post"
print(some_text)
titlecase_text = titlecase(some_text)
print(titlecase_text)
