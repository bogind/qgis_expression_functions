from qgis.core import qgsfunction, QgsProject, QgsFeatureRequest, QgsRenderContext, QgsVectorLayer

layer_names = []
layer_ids = []
for layer in QgsProject.instance().mapLayers().values():
    layer_names.append(layer.name())
    layer_ids.append(layer.id())

@qgsfunction(group='Color', referenced_columns=[], handlesnull=True )
def get_color(  *args,  feature, parent, context):
    """
    Returns the main color for a feature, works with 'single symbol', 'graduated symbol' and 'categorized symbol' types.
    <h4>Syntax</h4>
    <div class="syntax">
    <code>
    <span class="functionname">get_color</span>
    ([<span class="argument">layer</span>], [<span class="argument">uid</span>])
    </code>
    [] marks optional components
    </div>
    <h4>Arguments</h4>
    <div class="arguments">
    <table>
     <tr>
      <td class="argument">layer</td>
      <td>A string representing the name or id of the layer</td>
     </tr>
        <tr>
        <td class="argument">uid</td>
        <td>A string representing the unique id of the feature</td>
    </table>
    </div>
    <h4>Examples</h4>
    <div class="examples">
    <ul>
      <li>get_color( ) &rarr; '255,0,0,255' The color of the current feature</li> 
      <li>get_color( 'layer_name' ,'1') &rarr; '255,0,0,255' </li>
      <li>get_color( 'layer_id' ,'1') &rarr; '255,0,0,255'</li>
    </ul>
    """
    
    def return_color(layer=None,uid=None):
        if layer is None:
            layer = context.variable("layer_name")

        if uid is None:
            uid = feature.id()

        layer1 = None
        if layer in layer_names:
            layer1 = QgsProject.instance().mapLayersByName(layer)[0]

        if layer in layer_ids:
            layer1 = QgsProject.instance().mapLayer(layer)

        if layer1 is None:
            raise ValueError('Layer not found in the project')
        
        if not isinstance(layer1, QgsVectorLayer):
            raise ValueError('Layer must be a vector layer')
        
        if not layer1.isValid() or not layer1.renderer():
            raise ValueError('Layer is not valid or has no renderer')

        uid = int(uid)
        renderer = layer1.renderer()
    
        iterator = layer1.getFeatures(QgsFeatureRequest().setFilterFid(uid))
        try:
            feature1 = next(iterator)
        except StopIteration:
            raise ValueError('Feature not found in the layer')
        
        if layer1.renderer().type() =='singleSymbol':
            rgb = layer1.renderer().symbol().color().getRgb()
            color = '{},{},{},{}'.format(rgb[0],rgb[1],rgb[2],rgb[3])

        symbols = renderer.symbolsForFeature(feature1,QgsRenderContext())

        if len(symbols) == 0:
            return None
        
        if len(symbols) == 1:
            rgb = symbols[0].color().getRgb()
            color = '{},{},{},{}'.format(rgb[0],rgb[1],rgb[2],rgb[3])
            
        if len(symbols) > 1:
            # create a list of colors
            colors = []
            for symbol in symbols:
                rgb = symbol.color().getRgb()
                colors.append('{},{},{},{}'.format(rgb[0],rgb[1],rgb[2],rgb[3]))
            color = colors
            
        return color

        

    if len(args) == 0:
        layer=None
        uid=None
        return return_color(layer,uid)
    
    if len(args) == 1:
        layer = args[0]
        uid = None
    
    if len(args) == 2:
        layer = args[0]
        uid = args[1]


    if(not isinstance(layer,str)):
        raise ValueError('layer must be a string')
    
    if((not isinstance(uid,str) or not uid.isdigit() )
       and not isinstance(uid,int)):
        raise ValueError('uid must be an integer or a string representing an integer')
    
    if layer not in layer_names and layer not in layer_ids:
        raise ValueError('Layer not found in the project')
    
    return return_color(layer,uid)