from glossarpy.GreatGloss import GreatGloss
from glossarpy.GlossEntry import GlossEntry

'''
glossarpy typical use case example

This example has two outputs:
* An Sphinx-compatiable RST file containing a glossary
* A plaintext list of every entry in the glossary, useful for keeping track of
what entries have been added/removed in source control

In this example, CheezburgerGlossary is the name of the overall glossary object,
internally known as GreatGloss. A GreatGloss is a list of GlossEntry objects.

If we want either of the outputs to say what file it was created from, we can
use the Python built-in __file__, which will return the name of the Python file
that is currently being executed. There ae some caveats to this, such as the
fact this variable is not set when running in an interactive interpreter, so feel
free to replace __file__ with a string instead. If you would like to only print
the basename, this can be done by importing os, then using os.path.basename(__file__)
'''


outfile = "examples/typical_usage_output.rst"  # name of the overall glossary's output file
contents = "examples/typical_usage_toc.txt"  # name of the table of contents' output file

CheezburgerGlossary = GreatGloss("Very Cool Animals")
CheezburgerGlossary.add_entries([
	GlossEntry("Juice",
		definition="""A mysterious orange housecat, also known as Roofcat, native to the 
		East Side of Santa Cruz who successfully charmed at least four different households 
		into feeding him at the same time""",
		furtherreading="https://roofcat.care"),
	GlossEntry("cat",
		definition="A digitigrade carnivorous animal in the Felidae family of mammals",
		furtherreading="https://en.wikipedia.org/wiki/Felidae"),
	GlossEntry("Roofcat",seealso="Juice"),
	GlossEntry("tiger",
		definition="An orange-and-black striped [cat] native to Southeast Asia",
		furtherreading="https://en.wikipedia.org/wiki/Tiger")
	])

CheezburgerGlossary.sort_entries()  # put entries in alphabetical order
CheezburgerGlossary.write_toc(contents, "txt")
CheezburgerGlossary.write_glossary(outfile, sourcefile=__file__)