


def buildcontext(fn, kwargs):
    """Aggregate configuration settings.

    Precedence:
        1. command line arguments
        2. annotation keyword-arguments
        3. specific yaml
        4. general template (yaml with PEP292)
       (5. optional-arguments in main)

    Defaults: for example, attributes of a "_default" band should
    be copied into (but overridden by) all other bands, and the
    default band itself should be dropped.
    """
    # locations:
    #   - template.yaml : with package (i.e. near __file__)
    #   - config.yaml   : either CWD or, better, near argv[0] 

    import string
    import yaml

    with open('template.yaml') as f:
        template = string.Template(f.read())

    general = yaml.load(template.substitute(function=fn))

    # TODO: implement command line argument dictionary (try to shoehorn into click rather than argparse style?)

    FileNotFoundError = IOError # nicer in python 3
    try:
        with open('config.yaml') as f:
            specific = yaml.load(f.read())
    except FileNotFoundError:
        specific = {}

    # TODO: defaults

    # TODO: might want to parse some values (from string to python object)?
    
    context = general
    context.update(specific)
    context.update(kwargs)
    return context

import concurrent.futures
class defaultexecutor():
    map = map
    map = concurrent.futures.ThreadPoolExecutor(max_workers=2).map  

########




def main(func, executor=defaultexecutor(), start_msg="", **context):
    """Main application code"""

    print start_msg #context['msg']['start']

    iterable = (i*10 for i in range(10))

    # TODO: implement orderless map with finite queue    
    for result in executor.map(func, iterable):
        print "received", result
        
    print "finishing"

#######


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
        main(func, **buildcontext(func.__name__, kwargs))
        return func # no decoration
    return annotation if f is None else annotation(f)


# ---- all above would be an import


@annotate()
def thing(chunk):
    print "computing", chunk
    #import time
    #import random
    #time.sleep(random.random()*5)    
    return chunk+1

