from example_standalone_entries import *
from glossarpy.GlossEntry import GlossEntry
from glossarpy.GreatGloss import GreatGloss
import gc  # yep, that's garbage collector!

"""
Imports the entries from example_standalone_entries.py by simply
importing all of example_standalone_entries.py, then gathering
all GlossEntry objects into a GreatGloss object. This isn't
recommended, but if you want to keep your entries separate from
the actual code that builds them, it is an option.

See readme for info on sourcefile.
"""


outfile = "examples/imported_entries_output.rst"

# this seems like a bad idea, but it does work!
AwooGlossary = GreatGloss("They're Good Dogs, Brent")
for glossary_object in gc.get_objects():
    if isinstance(glossary_object, GlossEntry):
        AwooGlossary.add_entry(glossary_object)
AwooGlossary.sort_entries()
AwooGlossary.write_glossary(outfile, sourcefile=__file__)
