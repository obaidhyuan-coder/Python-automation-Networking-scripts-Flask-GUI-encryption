import os
import json
class SystemAuth:
 def __init__(self):
  self.max_attempts = 4
  self.file_name = "security.json"
  self.__password = ""
  self.__failed_attempts = 0
  self.__is_locked = False
  self.__load_security_file()
 def __load_security_file(self):
  
   
  if os.path.exists(self.file_name): 

    with open(self.file_name, 'r') as file:
     data = json.load(file)
     if "obaidh" in data :
      self.__password = data["obaidh"]["password"]
      self.__failed_attempts = data["obaidh"]["failed_attempts"]
      self.__is_locked = data["obaidh"]["is_locked"]
     else:
      self.__password = "obaidh"
      self.__failed_attempts = 0
      self.__is_locked = False
       
  else:
      self.__password = "obaidh"
      self.__failed_attempts = 0
      self.__is_locked = False
      self.__save_security_file() 

 def __save_security_file(self):
    data = {
            "obaidh": {
                     "password": self.__password, "failed_attempts": self.__failed_attempts,"is_locked": self.__is_locked}
                   }
                        
                                                                         
                                                          
    with open(self.file_name, 'w') as file:
       json.dump(data, file, indent=4)  

 def attempt_login(self, entered_password):
  if self.__is_locked:
   return "LOCKED"
  if entered_password == self.__password:

   self.__failed_attempts = 0
   self.__save_security_file()
   return "GRANTED"
  else:
    self.__failed_attempts += 1
    if  self.__failed_attempts >= self.max_attempts:
        self.__is_locked = True
        self.__save_security_file()
        return ("LOCKED")
        self.__save_security_file()
    return f"DENIED ({self.max_attempts - self.__failed_attempts} attempts left)"


