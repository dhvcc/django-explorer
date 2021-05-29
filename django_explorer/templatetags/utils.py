from numbers import Number


def sizeof_fmt(byte_size: Number, suffix="B") -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(byte_size) < 1024.0:
            return "%3.1f%s%s" % (byte_size, unit, suffix)
        byte_size /= 1024.0
    return "%.1f%s%s" % (byte_size, "Yi", suffix)
