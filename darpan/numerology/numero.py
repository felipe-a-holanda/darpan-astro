import string





class Numero(object):
    def __init__(self, name, birthday=''):
        self.name = name
        self.birthday = birthday
    
    def get_number_from_string(self, name):
        return self.reduce(str(name).strip().lower())
        
    def get_life_path_number(self):
        return self.get_number_from_string(self.birthday)
    
    def get_destiny_number(self):
        return self.get_number_from_string(self.name)
        
    def reduce(self, letters):
        n = sum([self.translate_letter(letter) for letter in letters])
        if n>9 and n!=11 and n!=22 and n!=33:
            return self.reduce(str(n))
        return n
        
    def translate_letter(self, letter):
        letter = letter.lower()
        if letter in string.ascii_lowercase:
            return ((ord(letter) - ord('a'))%9 + 1)
        elif letter in string.digits:
            return int(letter)
        return 0


class NumeroOld(object):
    def __init__(self, name, birthday='', alternate_name=''):
        self.name = self.format_name(name)
        
        
        self.name_numbers_list = self.translate(self.name)
        self.name_total = sum(self.name_numbers_list)
        self.name_number = self.reduce(self.name)
        
        if birthday:
            self.has_birthday = True
            self.birthday = self.format_birthday(birthday)
            self.birthday_numbers_list = self.translate(self.birthday)
            self.birthday_total = sum(self.birthday_numbers_list)
            self.birthday_number = self.reduce(self.birthday)
        else:
            self.has_birthday = False
            
        if alternate_name:
            
            self.has_alternate_name = True
            self.alt_name = self.format_name(alternate_name)
            self.alt_name_numbers_list = self.translate(self.alt_name)
            self.alt_name_total = sum(self.alt_name_numbers_list)
            self.alt_name_number = self.reduce(self.alt_name)
        else:
            self.has_alternate_name = False
            
    def get_life_path_number(self):
        return self.birthday_number
    
    def get_destiny_number(self):
        return self.name_number
        
    def format_name(self, name):
        return ' '.join([n.capitalize() for n in name.lower().split()])
    
    def format_birthday(self, birthday):
        return '/'.join(''.join([d  if d in string.digits else ' ' for d in str(birthday)]).split())
        
    def dict(self):
        d = dict()
        d['name'] = self.name
        d['name_number'] = self.name_number
        if self.has_birthday:
            d['birthday'] = self.birthday
            d['birthday_number'] = self.birthday_number
        
    def __str__(self):
        if self.has_birthday:
            report = "%s (%s)\n" % (self.name, self.birthday)
            report += "%10s = %d\n" % ('Name', self.name_number)
            report += "%10s = %d" % ('Birthday', self.birthday_number)
            report += '\n'
        else:
            report = "%s\n" % (self.name)
            report += "%10s = %d\n" % ('Name', self.name_number)
        
        if self.has_alternate_name:
            report += "%10s = %d (%s)\n" % ('Alt Name', self.alt_name_number, self.alt_name)
            
        return report
    
    def reduce(self, letters):
        n = sum([self.translate_letter(letter) for letter in letters])
        if n>9 and n!=11 and n!=22 and n!=33:
            return self.reduce(str(n))
        return n
    
    def translate(self, letters):
        return [self.translate_letter(letter) for letter in letters]
        
    def translate_letter(self, letter):
        letter = letter.lower()
        if letter in string.ascii_lowercase:
            return ((ord(letter) - ord('a'))%9 + 1)
        elif letter in string.digits:
            return int(letter)
        return 0
        
if __name__ == '__main__':
    print(NumeroOld('Felipe Andrade  holanda'))
    print(NumeroOld('Felipe Andrade  holanda', '22 12/1986'))
    print(NumeroOld('Felipe Andrade  holanda', '22 12/1986', 'Darpan Deva'))

    print(NumeroOld('Emerson Labella Bering', '3/11/1995'))
