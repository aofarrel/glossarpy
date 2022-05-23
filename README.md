# glossarpy
 Generate plaintext or Sphinx-flavored reStructuredText (RST) glossaries/dictionaries for documentation with Python. When output is set to RST, glossarpy will automatically give each entry an internal link, allowing for easy cross-referencing within and outside the glossary it generates. Links to external URLs are also supported.

## Usage
 `pip install glossarpy`

 Once glossarpy is installed in your Python environment, you can import it like any other module. See `examples/` for some typical use cases.

 glossarpy contains three classes:
 * **GlossEntry** - A single glossary entry which at a minimum contains a name for the entry. It may optionally include a definition, a pronunciation guide, a link to another entry, a link to an external website, or a note about how a term is specific to a certain context.
 * **GreatGloss** - A group of GlossEntry objects. A GlossEntry does not need to be inside a GreatGloss, but a GreatGloss needs at least one GlossEntry in it (in its `self.glosslist` to be specific) to actually be useful. Use the `add_entry()` function to add a single GlossEntry to a GreatGloss, or `add_entries()` to add a list of GlossEntry objects to a GreatGloss.
 * **GlossTxt** - Common functions to handle text output for GlossEntry and GreatGloss. Not really useful on its own.

### How to make a GlossEntry
 To declare a GlossEntry, all you need is their name: `WDL = GlossEntry("WDL")` will create a GlossEntry object with a `name` field of `"WDL"`.

 Here's a full list of fields that a GlossEntry can contain (all are type string except `updated` which is type datetime from the datetime module):
 * **name** - entry's name; spaces are supported, do not use [brackets]
 * **acronym_full** - if acronym, what is the full name. if blank, assumed to not be an acronym.
 * **further_reading** - URL to a webpage, usually an "official" one associated with the term
    * if an internal link to another documentation page, do not include .html at the end
 * **institute** - which institution or context is the phrase associated with?
 * **pronunciation** - pronunciation (ex: wdl - "widdle")
 * **seealso** - links to another GlossEntry by that GlossEntry's name field
 * **updated** - when the entry was last updated

## Useful GlossEntry methods
 Generally, you will want to use GreatGloss methods instead.

 * generate_plaintext() - generate entry as plaintext, see examples/example_print_one_entry.py
 * generate_rst() - generate entry as RST

 For either of these methods, you can set `timestamp=True` to have a timestamp get added to the output. That timestamp will be formatted as a comment (ie, will not show up when rendered as HTML in most forms of Sphinx, but will be in the RST file itself) if you are using `generate_rst(timestamp=True)`

### Linking one GlossEntry to another GlossEntry
 The `definition` and `acronym_full` arguments can reference other GlossEntry objects by their `name` field. To do so, encapsulate the entry title you which to reference with brackets, such as `WDL = GlossEntry("WDL", acronym_full="[Workflow Description Language]")` or `WDL = GlossEntry("WDL", definition="A shorthand for [Workflow Description Language]")`. When outputting to RST, this will create an internal hyperlink to a GlossEntry that has `name="Workflow Description Language"` assuming such a GlossEntry exists. 

 Do not put any alphanumeric characters immediately before or after either bracket.
 
 `acronym_full` will not link to another entry if brackets are not included, e.g. `GCP = GlossEntry("GCP", acronym_full="Google Cloud Platform")` would not link a GlossEntry 
 `seealso` can also reference another GlossEntry object by name, but it does not need brackets, because it assumes only links to other entries will be put in there. i.e. `GCP = GlossEntry("GCP", seealso="AWS")`.

## Useful GreatGloss methods
 * add_entry() - Add a single GlossEntry to GreatGloss
 * add_entries() - Add a list of GlossEntry objects to GreatGloss
 * sort_entries(ignorecase:bool = True)
   * Sort all GlossEntry objects added by add_entry() or add_entries() alphabetically by their name field
   * ignorecase: set to True (default) to treat capital and lowercase letters as equivalent (ex: `anaconda Anacondas bat zebra`), set to False to use default Python sorting (ex: `anaconda bat zebra Anacondas`)
 * write_glossary(self, outfile:str = "", format:str = "rst", skipTOC:bool = False, skipSource:bool = False, sourcefile:str = None)
   * Write a glossary to the file described in outfile; will raise a RuntimeError if neither this nor GreatGloss' object's outtoc field are defined
   * format: `rst` for RST output, `txt` for plaintext
   * columns (only matters if `format=="rst"`): Make the TOC render as [RST hlist columns](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-hlist). Set to 0 to use [contents with the local flag](https://docutils.sourceforge.io/docs/ref/rst/directives.html#table-of-contents) instead.
   * skipSource: Whether or not to put a note about the file being autogenerated
   * sourcefile: If skipSource==True, this is the name of the sourcefile to print.
 * write_toc(self, outtoc:str = "", format:str = "rst", columns:int = 0, skipSource:bool = False, sourcefile:str = None)
   * Write a TOC to the file described in outtoc (will fall back to the GreatGloss' object's outtoc field if one was defined during initalization, or, failing that, `toc.rst`)
   * All other arguments are equivalent to how they work in write_glossary()

### Keeping track of source files
 The whole point of glossarpy is to generate files. Generated files should not be updated, instead, their sources should be. To that end, write_toc() and write_glossary() will by default print a notice that they are autogenerated. If `output=="RST"` this notice will be a comment that appears only in the RST output, not in HTML files based upon said RST output.

 If sourcefile is not set (default behavior), the notice will read:

 `DO NOT EDIT THIS FILE. This file is autogenerated from a Python source file, update that instead.`

 You can make this more helpful by setting `sourcefile` to the name of the file that the entries originate from. In most cases, you can use Python built-in `__file__`, which will return the name of the Python file that is currently being executed. See examples/example_import_entries.py and examples/example_typical_usage.py for two examples of this, the former of which will result in an output that starts like this:

 `.. DO NOT EDIT THIS FILE. This file is autogenerated from examples/example_import_entries.py, update that instead.`

 There ae some caveats to using `__file__`, such as the fact this variable is not set when running in an interactive interpreter (resulting in a NameError), so sourcefile is set to None by default. Feel free to replace `__file__` with a string instead, or not set it at all.

 If you would like to only print the basename, first `import os` then `os.path.basename(__file__)`, which in the case of examples/example_import_entries.py would result in:

 `.. DO NOT EDIT THIS FILE. This file is autogenerated from example_import_entries.py, update that instead.`


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
```
 .
 ├── dockstore-documentation/
 └── glossarpy/
```
Then, run `make reqs`. Once you have run `make reqs` once, you can run `make all` or `make html` to your heart's content (until you leave your venv of course).
