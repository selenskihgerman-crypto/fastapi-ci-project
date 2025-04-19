# Ошибки в классе Person

1. В get_age возвращается `self.yob - now.year`, а должно быть `now.year - self.yob`.
2. В set_name не происходит присваивания нового имени.
   Было: self.name = self.name
   Должно быть: self.name = name
3. В set_address используется сравнение, а не присваивание.
   Было: self.address == address
   Должно быть: self.address = address
4. В is_homeless переменная address не определена, нужно self.address.
   Было: return address is None
   Должно быть: return self.address is None
