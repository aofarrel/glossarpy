from glossarpy.GreatGloss import *

'''
glossarpy typical use case example

This example has two outputs:
* An Sphinx-compatiable RST file containing a glossary
* A plaintext list of every entry in the glossary, useful for keeping track of
what entries have been added/removed in source control

In this example, CheezburgerGlossary is the name of the overall glossary object,
internally known as GreatGloss. A GreatGloss is a list of GlossEntry objects.
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
CheezburgerGlossary.write_toc(contents)
CheezburgerGlossary.write_glossary(outfile)