from kladr_search import main as error_module

def error_decorator(err_rec, result, double):
    def decorator(fun):
        print('Декоратор сработал arg')
        def result_decorator(_result, _err, _double, arg):
            _err = error_module('')
            result += _result
            err_rec += _err
            double += _double
            return fun(result, err_rec, double)
        return result_decorator
    return decorator