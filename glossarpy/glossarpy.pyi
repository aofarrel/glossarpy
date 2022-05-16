from typing import Any

class GlossTxt:
    def underline_text(self, text: str, underlinechar: str = ...): ...
    def rst_url(self, url): ...
    def rst_bookmark(self): ...
    def rst_process_brackets(self, words: list): ...

class GlossEntry(GlossTxt):
    name: str
    acronym_full: str
    definition: str
    furtherreading: str
    institute: str
    pronunciation: str
    seealso: str
    updated: datetime
    def __init__(self, name, acronym_full: str = ..., definition: str = ..., furtherreading: str = ..., institute: str = ..., pronunciation: str = ..., seealso: str = ..., updated=...) -> None: ...
    def return_name(self, nospaces: bool = ...): ...
    def text_entry_title(self): ...
    def text_pronunciation(self, format: str = ...): ...
    def text_acronym(self, format: str = ...): ...
    def text_definition(self, format: str = ...): ...
    def text_institute(self, format: str = ...): ...
    def text_seealso(self, format: str = ...): ...
    def text_furtherreading(self, format: str = ...): ...
    def text_updated(self, format: str = ...): ...
    def generate_plaintext(self): ...
    def generate_RST(self): ...

class GreatGloss(GlossTxt):
    title: str
    outfile: str
    outtoc: str
    updated: datetime
    glosslist: list
    def __init__(self, title, outfile: str = ..., outtoc: str = ..., updated=...) -> None: ...
    def add_entry(self, entry: GlossEntry): ...
    def add_entries(self, entries: list): ...
    def add_source(self, format: str = ...): ...
    def sort_entries(self, ignorecase: bool = ...): ...
    def make_toc(self, format, columns: int = ...): ...
    def write_glossary(self, outfile: str = ..., format: str = ..., skipTOC: bool = ..., skipSource: bool = ...) -> None: ...
    def write_toc(self, outtoc: str = ..., format: str = ..., columns: int = ...) -> None: ...
    def text_glossary_title(self): ...
