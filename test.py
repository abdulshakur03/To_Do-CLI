from datetime import date

print(bool(date.today()))
print(bool("None"))
print(date.today() or "fallback")
