# glossarpy
 Generate plaintext or reStructuredText (RST) glossaries/dictionaries for documentation with Python. When output is set to RST, glossarpy will automatically give each entry an internal link, allowing for easy cross-referencing within and outside the glossary it generates. Links to external URLs are also supported.

## Usage
 `pip install glossarpy`

 Once glossarpy is installed in your Python environment, you can import it like any other module. See `examples/` for some typical use cases.

 glossarpy contains three classes:
 * **GlossEntry** - A single glossary entry which at a minimum contains a name for the entry. It may optionally include a definition, a pronunciation guide, a link to another entry, a link to an external website, or a note about how a term is specific to a certain context.
 * **GreatGloss** - A group of GlossEntry objects. A GlossEntry does not need to be inside a GreatGloss, but a GreatGloss needs at least one GlossEntry in it (in its `self.glosslist` to be specific) to actually be useful. Use the `add_entry()` function to add a single GlossEntry to a GreatGloss, or `add_entries()` to add a list of GlossEntry objects to a GreatGloss.
 * **GlossTxt** - Common functions to handle text output for GlossEntry and GreatGloss. Not really useful on its own.

### GlossEntry's attributes
 To declare a GlossEntry, all you need is their name: `WDL = GlossEntry("WDL")` will create a GlossEntry object with a `name` field of `"WDL"`.

 Here's a full list of fields that a GlossEntry can contain (all are type string except `updated` which is type datetime from the datetime module):
    * **name** - entry's name; spaces are supported, do not use [brackets]
    * **acronym_full** - if acronym, what is the full name. if blank, assumed to not be an acronym.
    * **further_reading** - URL to a webpage, usually an "official" one associated with the term
    * **institute** - which institution or context is the phrase associated with?
    * **pronunciation** - pronunciation (ex: wdl - "widdle")
    * **seealso** - links to another GlossEntry
    * **updated** - when the entry was last updated

### Linking one GlossEntry to another GlossEntry
 The `definition` and `acronym_full` arguments can reference other GlossEntry objects by their `name` field. To do so, encapsulate the entry title you which to reference with brackets, such as `WDL = GlossEntry("WDL", acronym_full="[Workflow Description Language]")` or `WDL = GlossEntry("WDL", definition="A shorthand for [Workflow Description Language]")`. When outputting to RST, this will create an internal hyperlink to a GlossEntry that has `name="Workflow Description Language"` assuming such a GlossEntry exists. 

 Do not put any alphanumeric characters immediately before or after either bracket.
 
 `acronym_full` will not link to another entry if brackets are not included, e.g. `GCP = GlossEntry("GCP", acronym_full="Google Cloud Platform")` would not link a GlossEntry 
 `seealso` can also reference another GlossEntry object by name, but it does not need brackets, because it assumes only links to other entries will be put in there. i.e. `GCP = GlossEntry("GCP", seealso="AWS")`.

## Contributors
 As noted in https://github.com/aofarrel/glossarpy/issues/2 I'm seeking some guidance on ensuring this repo is packaged correctly. I am relatively new to this side of Python and would appreciate contributions.

 To setup a dev environment:

 1. Set up a Python venv. Not strictly necessary, but good practice.
 ```
 python3 -m venv ./venv
 source venv/bin/activate
 ```

 2. Pull this repo
 3. `pip install -r requirements-dev.txt`

### Compiling RST output in Sphinx 
 This repo's makefile includes commands to show you what a glossary made glossarpy looks like inside a readthedocs template of Sphinx, by leveraging Dockstore's documentation repo. If you want to be able to do that, pull [the Dockstore documentation repo](https://github.com/dockstore/dockstore-documentation), and have it on the same level as this repo, i.e.
"""
 .
 ├── dockstore-documentation/
 └── glossarpy/
"""
Then, run `make reqs`. Once you have run `make reqs` once, you can run `make all` or `make html` to your heart's content (until you leave your venv of course).
