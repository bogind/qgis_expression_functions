import json
from qgis.core import qgsfunction, QgsNetworkAccessManager
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.PyQt.QtCore import QUrl
 
@qgsfunction(group='Custom', referenced_columns=[])
def wiki_description(title, feature, parent):
    """
    Get the short description from Wikipedia for the title of an article.
    <h4>Syntax</h4>
    <div class="syntax">
    <code>
    <span class="functionname">wiki_description</span>
    (<span class="argument">title</span>)
    </code>
    [] marks optional components
    </div>
    <h4>Arguments</h4>
    <div class="arguments">
    <table>
     <tr>
      <td class="argument">title</td>
      <td>The title of a Wikipedia article</td>
     </tr>
    </table>
    </div>
    <h4>Examples</h4>
    <div class="examples">
    <ul>
      <li>wiki_description('Italy') &rarr; 'Country in southern Europe'</li>
    </ul>
    </div>
    """
    # Check the type of each parameter
    if(not isinstance(title,str)):
       raise ValueError('value must be a string')
    
    # Build the url for the request
    base_url = 'https://en.wikipedia.org/w/api.php?action=query&prop=description&format=json&titles='
    url = base_url + title
    
    # Create and send the request
    req = QNetworkRequest(QUrl(url))
    reply = QgsNetworkAccessManager.instance().blockingGet(req)
    
    # parse the response into a json object
    data = json.loads(reply.content().data())
    
    # Return the description of the first page
    pages = data['query']['pages']
    key = list(pages.keys())[0]
    description = pages[key]['description']
    return description
