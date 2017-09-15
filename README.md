# more_sense_hat
Additional functions for the Raspberry Py Sense Hat.

### Implemented
1. Progress Bar: In function `full_monotone`.
2. Multiple static bars: Up to 8 bars of configurable color. Use the `Display` 
class.
3. Spark line: Shows change in a single data point over time. Use `spark_line`.
4. MultiPoint: Class that allows display of multiple 2-dimensional data points.

### Prospective
2. ????
3. Profit

### Other tools
1. Timed page display: Allows the user to store various displays, cycling 
through them each `t` time.
    1. implementation: maintain a list/dict of the pages. Each "page" is a 
    function `f()` which is called repeatedly for `t` time.