import math as m # 1, 2. [import, as]
from browser import console # 3. [from]

# 4. [class] 定義模擬器
class RobotSim:
    # 5. [def] 定義方法
    def keywords_display(self):
        # 6-8. [True, False, None]
        status = True
        error = False
        sensor = None
        
        # 9-11. [if, elif, else]
        if status and not error: # 12, 13, 14. [and, not, is] (is 下方使用)
            pass # 15. [pass]
        elif error:
            return # 16. [return]
        else:
            raise Exception # 17. [raise]

        # 18-21. [try, except, finally, assert]
        try:
            assert True
        except:
            pass
        finally:
            # 22. [global]
            global result
            result = []

        # 23-25. [for, in, continue]
        for i in [1]:
            continue
            
        # 26-28. [while, break, or]
        while False or False:
            break
            
        # 29. [with] 
        # 30. [lambda]
        op = lambda x: x
        
        # 31. [yield]
        def gen():
            yield 1
            
        # 32, 33. [async, await]
        async def task():
            await None

        # 34. [del]
        temp = 1
        del temp
        
        # 35. [nonlocal]
        def outer():
            x = 1
            def inner():
                nonlocal x
            inner()

# 執行並只列印關鍵字清單
all_keywords = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 
    'except', 'finally', 'for', 'from', 'global', 'if', 'import', 
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 
    'return', 'try', 'while', 'with', 'yield'
]

for kw in all_keywords:
    print(kw)