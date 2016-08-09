
import context



import concurrent.futures
class defaultexecutor():
    map = map
    map = concurrent.futures.ThreadPoolExecutor(max_workers=2).map  





def main(func, executor=defaultexecutor(), start_msg="", **context):
    """Main application code"""

    print start_msg #context['msg']['start']

    iterable = (i*10 for i in range(10))

    # TODO: implement orderless map with finite queue    
    for result in executor.map(func, iterable):
        print "received", result
        
    print "finishing"




def annotate(f=None, **kwargs): 
    """API to designate the core function, launch the application, and pass arguments.

    Usage:
        import 5lines

        @5lines.annotate(app_setting=value, ..)
        def myalgorithm(input_chunk):
            ...
            return output_chunk
    """ # but annotate(lambda chunk: chunk) might suffice in a pinch.
    def annotation(func):
        main(func, **context.buildcontext(func.__name__, kwargs))
        return func # no decoration
    return annotation if f is None else annotation(f)



