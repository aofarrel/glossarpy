import datetime
import GlossTxt
import GlossEntry


class GreatGloss(GlossTxt):
    '''Object for an entire glossary'''
    def __init__(self, title, outfile="", outtoc="", updated=datetime.date.today()):
        self.title: str = title
        self.outfile: str = outfile
        self.outtoc: str = outtoc
        self.updated: datetime = updated
        self.glosslist: list[GlossEntry] = []  # updated by add_entry

    def add_entry(self, entry:GlossEntry):
        '''Add a new entry to the glossary'''
        self.glosslist.append(entry)

    def add_entries(self, entries:list):
        '''Add a list of entries to the glossary'''
        for entry in entries:
            self.add_entry(entry)

    def add_source(self, format="rst"):
        '''Include a note (as a comment if rst) on entry file to note it was created programatically'''
        message = """This file was created using GreatGloss. It is highly recommended to update the
        source file that this page was generated from rather than modifying it directly."""
        if format == "rst":
            return(f".. {message}\n\n")
        else:
            return message

    def _generate_entry_names_(self, asRSTlinks=False):
        '''Yield the name of every entry. If asRSTlinks==True, make them clickable internal links.
        Instead of calling this externally, use make_toc() instead.'''
        for entry in self.glosslist:
            if asRSTlinks:
                # remember: rst_process_brackets() expects input as a list, not str!
                yield entry.rst_process_brackets([f"[{entry.return_name()}]"])
            else:
                yield f"{entry.return_name()}\n"

    def sort_entries(self, ignorecase=True):
        '''Alphabetically sort all entries by their name field'''
        if ignorecase:
            self.glosslist.sort(key=lambda x: x.name.upper())
        else:
            self.glosslist.sort(key=lambda x: x.name)

    def make_toc(self, format, columns=3):
        '''Generates a TOC as a list of strings
        if columns>=1 && format=="rst": number of hlist columns to use
        if columns<=0 && format=="rst": use Sphinx built in local TOC instead of hlist'''
        TOC = []
        if format == "rst" or format == "RST":
            if columns <= 0:
                TOC.append(".. contents:: Table of Contents \n\t:local:\n\n")
            else:
                TOC.append(f".. hlist:: \n\t:columns: {columns}\n\n")
            for entry in self._generate_entry_names_(asRSTlinks=True):
                TOC.append(f"\t* {entry}\n")
        else:
            for entry in self._generate_entry_names_(asRSTlinks=False):
                TOC.append(entry)
        return TOC

    def write_glossary(self, outfile="", format="rst", skipTOC=False, skipSource=False):
        '''Write a glossary to a file, in plaintext or RST formatting.
        will try to fall back on self.outfile if outfile not declared when calling this function'''
        if outfile == "" and self.outfile == "":
            raise RuntimeError("No output file for glossary specified")
        with open(outfile if outfile != "" else self.outfile, "a") as f:
            if not skipSource:
                f.write(self.add_source(format=format))
            f.write("".join(self.text_glossary_title()))
            if not skipTOC:
                f.write("".join(self.make_toc(format=format)))
                f.write("\n")  # needed to keep RST from getting mad
            for entry in self.glosslist:
                f.write(entry.generate_RST())

    def write_toc(self, outtoc="", format="txt", columns=0):
        '''Write a table of contents to outtoc.
        Will try to fall back on self.outtoc if outtoc not declared when calling this function
        if columns>=1 && format=="rst": number of hlist columns to use
        if columns<=0 && format=="rst": use Sphinx built in local TOC instead of hlist'''
        if outtoc == "" and self.outtoc == "":
            raise RuntimeError("No output file for TOC specified")
        with open(outtoc if outtoc != "" else self.outtoc, "a") as f:
            f.write("".join(self.make_toc(format=format, columns=columns)))

    def text_glossary_title(self):
        '''Generate the overall glossary's title'''
        return self.underline_text(self.title, underlinechar="=")
