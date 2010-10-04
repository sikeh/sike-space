class Foo(object):
    def __init__(self):
        self.name = 'name'
        
    def print_me(self):
        print self.name
        
if __name__ == '__Main__':
    Foo().print_me()