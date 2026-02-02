from qgis.core import qgsfunction, QgsGeometry
from qgis import processing

@qgsfunction(group='Network', referenced_columns=[])
def shortest_path(network_layer, start_point, end_point, tolerance, strategy, parent):
    """
    Computes the optimal (shortest or fastest) route path between two points on a network.
    <h4>Syntax</h4>
    <div class="syntax">
    <code>
    <span class="functionname">shortest_path</span>
    (<span class="argument">network_layer</span>,
    <span class="argument">start_point</span>,
    <span class="argument">end_point</span>
    [,<span class="argument">tolerance:=0</span>]
    [,<span class="argument">strategy:=1</span>])
    </code>
    [] marks optional components
    </div>
    <h4>Arguments</h4>
    <div class="arguments">
    <table>
     <tr>
      <td class="argument">network_layer</td>
      <td>a line layer or the path to a line layer that can be used as a network</td>
     </tr>
     <tr>
      <td class="argument">start_point</td>
      <td>a point geometry or a string with the coordinates of the start point</td>
     </tr>
     <tr>
      <td class="argument">end_point</td>
      <td>a point geometry or a string with the coordinates of the end point</td>
     </tr>
     <tr>
      <td class="argument">tolerance</td>
      <td>a floating point number with the tolerance value. 
      Two lines with nodes closer than the specified tolerance are considered connected</td>
     </tr>
     <tr>
      <td class="argument">strategy</td>
      <td>0 (Shortest) or 1 (Fastest), default is 0</td>
     </tr>
    </table>
    </div>
    <h4>Examples</h4>
    <div class="examples">
    <ul>
      <li>shortest_path('roads', start_point, $geometry, 0.01, 1) &rarr; A line geometry</li>
      <li>shortest_path('roads', geometry(@feature), '12.490921,41.898306 [EPSG:4326]', 0.01, 1) &rarr; A line geometry (leading to Rome, Italy)</li>
    </ul>
    </div>
    """
    # Check the type of each parameter
    if(not isinstance(network_layer,str)):
         parent.setEvalErrorString('network_layer must be a string representing a layer name or ID')
    if(not isinstance(start_point,str) and not isinstance(start_point,QgsGeometry) ):
         parent.setEvalErrorString('start_point must be a string representing a point or a Geometry')
    if(not isinstance(end_point,str) and not isinstance(end_point,QgsGeometry) ):
         parent.setEvalErrorString('end_point must be a string representing a point or a Geometry')
    if(not isinstance(tolerance,float)):
         # If tolerance is not a float, check if it is None and set a default value
         if tolerance is None:
            tolerance = 0
         else:
            parent.setEvalErrorString('tolerance must be a floating point number')
    # Check both type and allowed values for "strategy"
    if(not isinstance(strategy,int) or strategy > 1 or strategy < 0):
         # If strategy is not an integer or is not 0 or 1, check if it is None and set a default value
         if strategy is None:
            strategy = 1
         else:
            parent.setEvalErrorString('strategy must be either 0 or 1')
         
    
    params = {
        'INPUT':network_layer,
        'START_POINT':start_point,
        'END_POINT':end_point,
        'TOLERANCE':tolerance,
        'STRATEGY':strategy,
        'OUTPUT': 'memory:'
        }
    path = processing.run("native:shortestpathpointtopoint", params)
    return path['OUTPUT'].getGeometry(1)