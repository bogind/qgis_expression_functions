from qgis.core import qgsfunction
import unicodedata

@qgsfunction(args=1, group='Custom')
def normalize_rtl_label(values, feature, parent):
    """
    normalize_rtl_label( <string> ) → string
    Reverses characters in each RTL part of the input string.
    LTR and neutral parts are left in original order.
    """
    val = values[0]
    # allow NULLs to pass through
    if val is None:
        return None
    # enforce string type
    if not isinstance(val, str):
        raise ValueError('normalize_rtl_label: input is not a string')

    # split into bidi runs
    runs = []
    current_dir = None
    current_text = ''
    for ch in val:
        bidi = unicodedata.bidirectional(ch)
        if bidi in ('R','AL','RLE','RLO'):
            dir_flag = 'RTL'
        elif bidi in ('L','LRE','LRO'):
            dir_flag = 'LTR'
        else:
            dir_flag = 'Neutral'

        if dir_flag != current_dir:
            if current_text:
                runs.append((current_text, current_dir))
            current_text = ch
            current_dir = dir_flag
        else:
            current_text += ch

    # flush last run
    if current_text:
        runs.append((current_text, current_dir))

    # rebuild, reversing only RTL runs
    out = []
    for text, direction in runs:
        out.append(text[::-1] if direction == 'RTL' else text)
    return ''.join(out)
