from glossarpy.GlossEntry import GlossEntry

cat = GlossEntry("cat",
    definition="A digitigrade carnivorous animal in the Felidae family of mammals",
    furtherreading="https://en.wikipedia.org/wiki/Felidae")

print(cat.generate_plaintext())