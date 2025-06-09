from bytecode import Bytecode, Instr, CellVar
'''
可以处理闭包变量
'''

def save_function_code_info(func, filename="function_info.txt"):
    """
    将函数的字节码信息写入文件
    
    Args:
        func: 要分析的函数对象
        filename: 输出文件名(默认function_info.txt)
    """
    code = func.__code__
    
    with open(filename, 'a', encoding='utf-8') as f:
        # 写入标题行
        f.write(f"Function: {func.__qualname__} info:\n")
        f.write("="*50 + "\n")
        
        # 写入所有co_*属性
        for attr in dir(code):
            if attr.startswith('co_'):
                value = getattr(code, attr)
                # 特殊处理code对象
                if attr == 'co_code':
                    value = f"<bytes length={len(value)}>"
                elif attr == 'co_consts':
                    value = [str(c) for c in value]
                f.write(f"{attr:15}:\t{value}\n")
        f.write(code)

class get_local(object):
    cache = {}
    is_activate = False

    def __init__(self, *args):
        self.varnames = list(args)
        type(self).cache


    def __call__(self, func):
        if not type(self).is_activate:
            # 打印函数的字节码信息，调试
            # save_function_code_info(func)
            return func
        
        if func.__qualname__ not in type(self).cache:
            type(self).cache[func.__qualname__] = [self.varnames]

        c = Bytecode.from_code(func.__code__)

        # 在函数开始时存储原始变量值
        extra_code = []
        for varname in self.varnames:
            extra_code.extend([
                Instr('LOAD_FAST', varname) if varname in func.__code__.co_varnames else \
                Instr('LOAD_DEREF', CellVar(varname))
            ])
        # 拼接返回元组       
        extra_code.extend([Instr('BUILD_TUPLE', len(self.varnames)+1)])
        extra_code.extend([
            Instr('STORE_FAST', '_result_tuple'),
            Instr('LOAD_FAST', '_result_tuple')])

        c[-1:-1] = extra_code
        func.__code__ = c.to_code()

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except UnboundLocalError as e:
                print("UnboundLocalError:", e)
                print("Function code And Extra code: ")
                print(Bytecode.from_code(func.__code__))
                print(extra_code)
                exit(1)
            res, values = result[0], result[1:]
            cache_list = []
            for value in values:
                if hasattr(value, 'detach'):
                    cache_list.append(value.detach().cpu().numpy())
                elif isinstance(value, list) or isinstance(value, tuple):
                    vals = []
                    for val in value:
                        vals.append(val.detach().cpu().numpy() if hasattr(val, 'detach') else val)
                    cache_list.append(vals)
                else:
                    cache_list.append(value)
            type(self).cache[func.__qualname__].append(cache_list)
            return res
        return wrapper

    @classmethod
    def clear(cls):
        cls.cache = {}

    @classmethod
    def activate(cls):
        cls.is_activate = True
