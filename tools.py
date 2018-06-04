def findcaller(func):
    def wrapper(*args,**kwargs):
        import sys
        f=sys._getframe()
        filename=f.f_back.f_code.co_filename
        lineno=f.f_back.f_lineno
        print( '######################################')
        print( 'caller filename is ',filename)
        print( 'caller lineno is',lineno)
        print( 'the passed args is',args,kwargs)
        print( '######################################')
        func(*args,**kwargs)
    return wrapper