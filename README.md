# objparser
A python script to parse Analyze object maps (.obj files).

This script can be used to parse .obj files created by [Analyze](https://analyzedirect.com/analyze-12-0/).
The segmentation masks are made accessible as NumPy arrays. Note that the data returned should reflect the
object data as it is stored in the .obj file. While the annotation information for each object is read in
and accessible via the `objects` property, it is not used to transform the data in any way. 

## Usage:

```python
# Assuming script is saved in your workspace directory
from objparser import AnalyzeObjectMap

# Create instance with file argument
obj_map = AnalayzeObjectMap(file='path/to/file.obj')

# Alternatively, initialize instance and then call from_file method
obj_map = AnalyzeObjectMap()
obj_map.from_file('path/to/file.obj')

# Get numpy array representing the segmentation mask
obj_map.get_data()

# Since version 7 of the .obj file format, multiple volumes can be stored in the same file
# They can be accessed by passing the index (idx) of the desired volume.
obj_map.get_data(idx)
```

The .obj file stores some header information for each object in the object map. This information
is accessible via the `objects` instance variable as follows:

```python
# Get number of unique objects in object map
len(obj_map.objects)

# Get first object's name property
obj_map.objects[0].name
```
