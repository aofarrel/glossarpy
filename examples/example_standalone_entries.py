from glossarpy import glossarpy

"""
Used alongside example_import_entries.py
"""


canine = glossarpy.GlossEntry("canine",
	definition="A digitigrade, mostly-carnivorous animal in the Canidae family of mammals",
	furtherreading="https://en.wikipedia.org/wiki/Canidae")

wolf = glossarpy.GlossEntry("wolf",
	definition="A large [canine] found across the Northern Hemisphere known to form packs",
	furtherreading="https://en.wikipedia.org/wiki/Wolf")