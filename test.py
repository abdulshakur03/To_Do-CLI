from datetime import date

print(bool(date.today()))
print(bool(None))
print(bool(""))
print(date.today() or "fallback")
