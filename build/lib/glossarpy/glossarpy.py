import datetime
import re


class GlossTxt:
    '''Handles RST-specific output'''

    def underline_text(self, text:str, underlinechar="-"):
        '''Underlines text, used to create a valid rst header or make txt prettier'''
        return [f"{text}\n", underlinechar * len(text) + "\n"]

    def rst_url(self, url):
        '''Generate an RST URL for further reading'''
        return f"`<{url}>`_"

    def rst_bookmark(self):
        '''Generates an RST bookmark for the entry'''
        return f".. _dict {self.return_name(nospaces=False)}:"

    def rst_process_brackets(self, words:list):
        '''Turn [this] into an RST internal link, assuming the part being linked to
        has a bookmark created with rst_bookmark(). Expects words to be a list of
        strings, split upon spaces.'''
        words_processed = []
        multi_word_flag = False
        for word in words:
            if re.search("][a-zA-Z]+", word):
                print(f"""Warning: An entry will have an invalid internal link
                    due RST limitations. Put some sort of whitespace or punctuation before
                    any additional letters after the ending bracket. Problematic word: {word}""")

            # This is the beginning of an internal RST link
            elif word.startswith("["):
                word = word[1:]  # strip [
                if "]" in word:
                    multi_word_flag = False
                    word = word.replace("]", "`")
                    word = f":ref:`dict {word}"
                else:
                    multi_word_flag = True
                    word = f":ref:`dict {word}"

                words_processed.append(word)

            # This is a continuation of a previous word's RST link
            # will break on [Seven Br]idges] but that's not my problem
            elif multi_word_flag is True:

                if "]" in word:
                    multi_word_flag = False
                    word = word.replace("]", "`")
                    word = f"{word}"
                else:
                    word = f"{word}"

                words_processed.append(word)

            else:
                words_processed.append(word)

        return " ".join(words_processed)


class GlossEntry(GlossTxt):
    '''Object for an individual glossary entry'''
    def __init__(self, name, acronym_full="", definition="", furtherreading="", institute="",
            pronunciation="", seealso="", updated=datetime.date.today()):
        '''
        name - entry's name; spaces are supported, do not use [brackets]
        acronym_full - if acronym, what is the full name. if blank, assumed to not be an acronym.
        further_reading - URL to a webpage, usually an "official" one associated with the term
        institute - which institution is the phrase associated with?
        pronunciation - pronunciation (ex: wdl - "widdle")
        seealso - related but not equivalent entries, such as CLI being related to Dockstore CLI.
        updated - when the entry was last updated

        When outputting to RST, acronym_full, seealso, & definition will replace text in [brackets]
        with a working internal hyperlink to another entry. For example, if self.definition="I use
        [Seven Bridges]", then the RST out will be "I use :ref:`dict Seven Bridges`" (although the
        link will not be clickable if there is no entry for Seven Bridges)
        '''
        self.name: str = name
        self.acronym_full: str = acronym_full
        self.definition: str = definition
        self.furtherreading: str = furtherreading
        self.institute: bool = institute
        self.pronunciation: str = pronunciation
        self.seealso: str = seealso
        self.updated: datetime = updated

    def return_name(self, nospaces=False):
        '''Returns name of the entry'''
        if not nospaces:
            return self.name
        else:
            processed_characters = []
            for character in self.return_name(nospaces=False):
                if character == " ":
                    character = "-"
                processed_characters.append(character)
            return "".join(processed_characters)

    def text_entry_title(self):
        '''Return underlined title. Same in RST, Markdown, and plaintext.'''
        entry_title = []
        entry_title.append("\n\n")  # keep space between entries big enough to keep RST happy
        entry_title.extend(self.underline_text(self.name))
        return "".join(entry_title)

    def text_pronunciation(self, format="txt"):
        '''Return pronunciation'''
        if format == "txt":
            return f"[pronounced {self.pronunciation}]\n"
        elif format == "rst":
            return f"pronounced {self.pronunciation}  \n\n"

    def text_acronym(self, format="txt"):
        '''Return acronym's full form, in italics if RST. We need an extra newline in RST to prevent
        the acronym from being considered a header relative to the definition.'''
        if format == "txt":
            return f"abbreviation for {self.acronym_full}\n"
        elif format == "rst":
            words = self.acronym_full.split()
            return f"*abbreviation for* {self.rst_process_brackets(words)}  \n\n"

    def text_definition(self, format="txt"):
        '''Return the definition of the entry.
        If RST, calls a function that turns bracketed [text] into internal links.
        Limitations: RST does not support letters coming after a link without a puncuation mark.'''
        if format == "txt":
            return f"    {self.definition}\n"
        elif format == "rst":
            words = self.definition.split()
            processed_with_links = self.rst_process_brackets(words)
            return f"    {processed_with_links}  \n\n"

    def text_institute(self, format="txt"):
        '''Return a caveat about how this term may mean something else outside the context of
        self.institute. In RST form this becomes a note block.'''
        if format == "txt":
            return f"This term as we define it here is associated with {self.institute} and may have different definitions in other contexts.\n"
        elif format == "rst":
            return f".. note:: This term as we define it here is associated with {self.institute} and may have different definitions in other contexts.  \n"

    def text_seealso(self, format="txt"):
        '''Returns the entry's seealso information, which links to another entry.
        There is a supposedly simplier way to do this with sphinx.ext.autosectionlabel, via:
            see also :ref:`{self.seealso}`
        ...but using extension often requires people reformat tons of links. For example, in
        Dockstore's documentation, loading sphinx.ext.autosectionlabel raises 175 new errors.'''
        if format == "txt":
            return f"see also {self.seealso}\n"
        elif format == "rst":
            if self.institute == "":
                return f"see also :ref:`dict {self.seealso}`  \n"
            else:  # not strictly necessary to render, but without this warning will be thrown
                return f"\nsee also :ref:`dict {self.seealso}`  \n"

    def text_furtherreading(self, format="txt"):
        '''Returns the entry's further reading section, which is a single URL.
        In RST, if there is a see also, we need an extra newline in further reading.'''
        if format == "txt":
            return f"Further reading: {self.furtherreading}\n"
        elif format == "rst":
            if self.seealso == "" and self.institute == "":
                return f"Further reading: {self.rst_url(self.furtherreading)}  \n"
            else:
                return f"\nFurther reading: {self.rst_url(self.furtherreading)}  \n"

    def text_updated(self, format="txt"):
        '''Return when entry was last updated (visibly if txt, as a comment if RST)
        Caveat: This isn't very helpful if you keep all of your entries in the same file and
        parse all of them at the same time.'''
        if format == "txt":
            return self.updated.strftime("updated %Y-%m-%d\n")
        elif format == "rst":
            return self.updated.strftime("\n.. updated %Y-%m-%d  \n\n\n\n")

    def generate_plaintext(self):
        '''Generate plaintext output of this entry'''
        plaintext = []
        plaintext.append(self.text_entry_title())
        if self.pronunciation != "":
            plaintext.append(self.text_pronunciation())
        if self.acronym_full != "":
            plaintext.append(self.text_acronym())
        if self.definition != "":
            plaintext.append(self.text_definition())
        if self.institute != "":
            plaintext.append(self.text_institute())
        if self.seealso != "":
            plaintext.append(self.text_seealso())
        if self.furtherreading != "":
            plaintext.append(self.text_furtherreading())
        plaintext.append(self.text_updated())
        return "".join(plaintext)

    def generate_RST(self):
        '''Generate RST output of this entry'''
        rst = []
        rst.append(self.rst_bookmark())
        rst.append(self.text_entry_title())
        if self.pronunciation != "":
            rst.append(self.text_pronunciation(format="rst"))
        if self.acronym_full != "":
            rst.append(self.text_acronym(format="rst"))
        if self.definition != "":
            rst.append(self.text_definition(format="rst"))
        if self.institute != "":
            rst.append(self.text_institute(format="rst"))
        if self.seealso != "":
            rst.append(self.text_seealso(format="rst"))
        if self.furtherreading != "":
            rst.append(self.text_furtherreading(format="rst"))
        rst.append(self.text_updated(format="rst"))
        return "".join(rst)


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
