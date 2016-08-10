"""
This module is responsible for combining the configuration
settings from various sources.
"""


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
    
    cmdline = commandlineargs()

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
    context.update(cmdline)
    return context


def commandlineargs():
    """ Facilitate receiving settings from the command-line """

    import sys
    if len(sys.argv) <= 1: # if no args (not even --help) then follow default behaviour
        return {}
    else: # need to parse arguments
        app_name = sys.argv[0]
        import click

        class resume(Exception): # kind of like a coroutine?
            def __init__(self, data={}):
                self.contents = data
        
        @click.group(name=app_name)
        def cli():
            pass

        @cli.command()
        def pbs():
            #raise resume(options_dict)
            raise resume
        
        try:
            cli() # click doesn't return
            raise NotImplementedError
        except resume as r:
            return r.contents

