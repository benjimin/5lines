Motivation
==========

Lots of datacube applications involve transforming one product into another. Typically the source product has 2 spatial dimensions, 1 temporal dimension, and a finite number of bands. The target product usually differs in the number of bands. In some but not all cases, the target product also condenses out the temporal dimension. Otherwise, the extent of the source and target products is the same. 

This transformation is generally "local" in some sense. Commonly, this applies in the strict sense: each cell value in the target depends on the corresponding cell (or, if collapsing a dimension, then the corresponding *cells*) in the source, and is independent of other (e.g. neighbouring) cells in either product. (Additionally, there are other cases where local applies in a weaker sense, such as if the transformation involves reprojection or smoothing; the radius of influence is still bounded.) 

Naturally, the implementation of such applications (on a continental scale) shares the workload among available computing resources, e.g. by splitting the task into blocks. Each different application needs a unique block-transformation function, and the API (using xarray) facilitates concise expressions of this function (which read similarly to the abstract equations of relevant scientific literature). However, work also exists in parsing input configurations (e.g. defining the extent of operation), querying for data, managing the process (e.g. obtaining resources, splitting the task, distributing the load and collecting the results), producing output, and formatting appropriately (e.g. reindexing with an appropriate product definition and harvesting appropriate metadata such as provenance).

Given that numerous plausible and actual examples fit this pattern, it is desirable for the datacube to support these with minimal "boilerplate" code. 

Example
-------

Taking a (git) diff of the ndvi and fc repos (which had been implemented using one as a template for the other):

- The documentation (readme file) legitimately should differ.

- The packaging code (i.e. the remainder of the root directory) has negligible differences (e.g. name/version/url) other than the building of any CPython extensions.

- The difference in configs (yaml) corresponds only to differences in documentation and in output bands.

- The scripts (i.e. for launching on a cluster) really only differ in the name of the core python script.

- The core app differences are also minimal.




Design
======

API
---
Since the distributed API requires a function handle to the code that runs in parallel, the amenable syntax is an annotation (decorating the function-definition of the core algorithm) rather than an iterable (which has no handle to the statements that are looped over it). An alternative would be some kind of inheriting class (but this is unpythonic if a function will suffice). A less sugary alternative is some kind of parallel map command. Here the approach may likely first be a parallel map, followed by annotation sugar.

Environment
-----------
The code should just run locally, if the user tries to do so ordinarily. (Sane default may be to dry-run as far as database indexing is concerned.) But the same code should be used without modification in the distributed environment (e.g. using command line arguments to inform regarding the scheduler/workers). Furthermore, the same code should also (again by another subcommand flag) be able to kick off a PBS job.

Configuration
-------------
The idea is that you specify what is needed for your application, but otherwise rely on sane defaults. For example: 1. read in a template for the defaults, 2. produce the defaults (applying localisation e.g. pulling in the function name), 3. "update" with any fields in a user-supplied file, 4. update with options from the script itself (arguments to the constructor), 5. finally override with command line arguments. (Maybe the templating should occur late?)





