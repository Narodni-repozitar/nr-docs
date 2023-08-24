import pathlib


__version__ = (pathlib.Path(__file__).parent / 'VERSION').read_text().strip()
