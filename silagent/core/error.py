
class LoadError(Exception):
    def __init__(self, name: str, message: str, suberror: "LoadError" = None):
        super().__init__(f"{name}: {message}")

        self.__sub_error = suberror
    
    def show (self):
        if self.__sub_error is not None:
            self.__sub_error.show()
        
        print(self)
