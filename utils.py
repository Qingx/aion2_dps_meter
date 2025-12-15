from datetime import datetime

from skimage.metrics import structural_similarity

def images_not_similar(prev, cur, threshold=0.9):
    if prev is None or cur is None:
        return True
    return structural_similarity(prev, cur, channel_axis=2, full=False) < threshold


def fuzzy_string_match(lhs, rhs, deep=1):
    len_diff = abs(len(lhs) - len(rhs))
    if len_diff > deep:
        return False

    miss = len_diff
    for i in range(0, min(len(lhs), len(rhs))):
        miss += 0 if rhs[i] == lhs[i] else 1
        if miss > deep:
            return False

    return True


def format_timestamp(timestamp_ms):
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    except:
        return str(timestamp_ms)
