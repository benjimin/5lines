"""
Status: works. As far as a silly demo is concerned.

TODO next: start adapting to actual datacube task (albeit simplified),
perhaps starting with just dummy data.

Note: for continental, want workers to write files, and we will index.
But for local, might not even want files written let alone indexing,
perhaps want data returned to us (to visualise).

We need to wrap the user's function. It is data->data, 
or hypothetically, tuple(xarray)->tuple(xarray).
But what we actually want to map out is subquery_parameters->success_indicator
(i.e. output data should be dumped as almost a side-effect).

"""

import context
import concurrent.futures

executor_map = concurrent.futures.ThreadPoolExecutor(max_workers=2).map 

def executor_map(func, iterable):
    """ orderless parallel map """
    # TODO: queues..
    import distributed # massively slow to import...
    executor = distributed.Executor()
    futures = executor.map(func, iterable) # should return immediately
    for future in distributed.as_completed(futures): # blocks
        assert future.done()
        yield future.result()     



def main(func, start_msg="", **context):
    """Main application code"""
   
    def wrapper(subquery, func=func):
        """ Task to execute on a worker (wraps core function) """
        import numpy as np
        input_chunk = np.ones(5)
        output_chunk = func(input_chunk)
        summary = np.sum(output_chunk)
        return subquery, summary
    

    print start_msg #context['msg']['start']

    iterable = (i*11 for i in range(10))

    # TODO: implement orderless map with finite queue    
    for result in executor_map(wrapper, iterable):
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



