# function_keys.py

import keyboard

class FunctionKey: # sends function keys f1 to f24
    @staticmethod
    def f1():
        keyboard.send('f1')

    @staticmethod
    def f2():
        keyboard.send('f2')

    @staticmethod
    def f3():
        keyboard.send('f3')

    @staticmethod
    def f4():
        keyboard.send('f4')

    @staticmethod
    def f5():
        keyboard.send('f5')

    @staticmethod
    def f6():
        keyboard.send('f6')

    @staticmethod
    def f7():
        keyboard.send('f7')

    @staticmethod
    def f8():
        keyboard.send('f8')

    @staticmethod
    def f9():
        keyboard.send('f9')

    @staticmethod
    def f10():
        keyboard.send('f10')

    @staticmethod
    def f11():
        keyboard.send('f11')

    @staticmethod
    def f12():
        keyboard.send('f12')

    @staticmethod
    def f13():
        keyboard.send('f13')

    @staticmethod
    def f14():
        keyboard.send('f14')

    @staticmethod
    def f15():
        keyboard.send('f15')

    @staticmethod
    def f16():
        keyboard.send('f16')

    @staticmethod
    def f17():
        keyboard.send('f17')

    @staticmethod
    def f18():
        keyboard.send('f18')

    @staticmethod
    def f19():
        keyboard.send('f19')

    @staticmethod
    def f20():
        keyboard.send('f20')

    @staticmethod
    def f21():
        keyboard.send('f21')

    @staticmethod
    def f22():
        keyboard.send('f22')

    @staticmethod
    def f23():
        keyboard.send('f23')

    @staticmethod
    def f24():
        keyboard.send('f24')

# when you read this, please update config.yaml and stuff with this:
'''
class FunctionKey:
    @staticmethod
    def send_fkey(n: int):
        if 1 <= n <= 24:
            keyboard.send(f'f{n}')
        else:
            raise ValueError("Function key number must be between 1 and 24")
'''