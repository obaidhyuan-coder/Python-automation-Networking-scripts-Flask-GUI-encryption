class CaesarCipher:
    def __init__(self, key):
       
       
            self.key = key
       

    def _shift_char(self, char, mode):
       
        start, end = 32, 126
        range_size = end - start + 1
        
        shift = self.key if mode == 'encrypt' else -self.key
        
      
        if start <= ord(char) <= end:
       
            new_unicode = (ord(char) - start + shift) % range_size + start
            return chr(new_unicode)
        
       
        return char

    def encrypt(self, text):
        if not text: 
            return ""
        return "".join(self._shift_char(c, 'encrypt') for c in text)

    def decrypt(self, text):
        if not text: 
            return ""
        return "".join(self._shift_char(c, 'decrypt') for c in text)

