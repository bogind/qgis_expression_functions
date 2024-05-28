from sys import getdefaultencoding
from qgis.core import qgsfunction
from qgis.PyQt.QtCore import QDateTime, QTimeZone, QByteArray
 
tzones = list(map(lambda x: bytes(x).decode(), QTimeZone().availableTimeZoneIds()))
 
@qgsfunction(group='Date and Time', referenced_columns=[])
def set_timezone(datetime, timezone, feature, parent):
    """
    Sets the timezone of a datetime object.
    <h4>Syntax</h4>
    <div class="syntax">
    <code>
    <span class="functionname">set_timezone</span>
    (<span class="argument">datetime</span>, <span class="argument">tz</span>)
    </code>
    [] marks optional components
    </div>
    <h4>Arguments</h4>
    <div class="arguments">
    <table>
     <tr>
      <td class="argument">datetime</td>
      <td>A datetime object</td>
     </tr>
        <tr>
        <td class="argument">timezone</td>
        <td>A string representing a timezone, see <a href="https://doc.qt.io/qt-5/qtimezone.html#availableTimeZoneIds">QTimeZone::availableTimeZoneIds</a></td>
    </table>
    </div>
    <h4>Examples</h4>
    <div class="examples">
    <ul>
      <li>set_timezone( now() ,'UTC') &rarr; '2024-05-28T09:21:03.769' </li>
      <li>set_timezone( now() ,'America/New_York') &rarr; '2024-05-28T09:21:39.317-04:00'</li>
      <li>set_timezone( now() ,'UTC+03:00') &rarr; '2024-05-28T09:22:04.630+03:00'</li>
    </ul>
    </div>
    """
    
    # Check the type of each parameter
    if(not isinstance(timezone,str)):
       raise ValueError('timezone must be a string')
       
    if(not isinstance(datetime,QDateTime)):
       raise ValueError('datetime must be a datetime object')
    
    if(timezone not in tzones):
        raise ValueError('timezone not found in the list of available timezones')
    
    # Create a timezone object
    sys_encoding = getdefaultencoding()
    tz = QTimeZone(QByteArray(timezone.encode(sys_encoding)))

    # Set the timezone
    datetime.setTimeZone(tz)
    
    return datetime
