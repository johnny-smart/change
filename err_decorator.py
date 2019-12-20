from kladr_search import main as error_module

def error_decorator(
    # err_rec, result, double
    ):
    def decorator(result_init):
        print('Декоратор сработал arg')
        def result_decorator(town, fname, sheet, houses):
            _result, _err, _double = result_init(town, fname, sheet, houses)
            re_search = (list(map(error_module, _err)))
            # result += _result
            # err_rec += _err
            # double += _double
            return _result, _err, _double, re_search
        return result_decorator
    return decorator