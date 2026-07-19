# -*- coding: utf-8 -*-
import re

# leading adjective endings (nominative, all genders/number) + common participles
ADJ = re.compile(r'.*(ый|ий|ой|ая|яя|ое|ее|ые|ие|ого|его|ому|ому|ыми|ими|ых|их)$', re.I)
# neuter nouns that end like adjectives (-ие/-ье) — must be treated as HEAD noun
NEUTER = {"одеяние","одеяния","навершие","наплечье","ожерелье","снаряжение",
          "копьё","копье","седло","платье","пальто","древко","древок","пугио","жабо",
          "лезвие","лезвия","облачение","облачения","оперение","покрытие","остриё","усиление"}
# soft-sign (-ь) gender
SOFT_F = {"ткань","скуфь","перевязь","обувь","шапель","вязь","сталь","кость","бронь","гладь","цепь","сеть"}
SOFT_M = {"огонь","билль","конь","ремень","гвоздь","лапоть","желудь"}
PREP = {"с","со","из","изо","поверх","на","в","во","под","для","у","до","за",
        "через","при","об","о","без","от","по","к","над"}
# adverbs / conjunctions / non-noun words to skip (NOT phrase boundaries)
SKIP = {"очень","весьма","совсем","чуть","лишь","более","менее","самый","самая","самое","и"}

def is_number(w):
    w = w.strip('.,')
    return w.isdigit() or w.lower() in {"г","грамм","гр"}   # standalone number/unit only
def clean(w): return w.strip('.,;:!?«»"()')

def adj_gender(adj):
    """Gender implied by a singular adjective ending (None if plural/unknown)."""
    if not adj: return None
    a = adj.lower()
    if re.search(r'(ые|ие|ых|их|ыми|ими)$', a): return None   # plural -> gender hidden
    if re.search(r'(ый|ий|ой)$', a): return "MI"
    if re.search(r'(ая|яя)$', a): return "FI"
    if re.search(r'(ое|ее)$', a): return "NI"
    return None

def noun_gender(w):
    """Gender guessed from the noun itself (compound -> first part)."""
    b = w.lower().split("-")[0]
    if b in NEUTER or re.search(r'(о|е|ё)$', b): return "NI"
    if re.search(r'(а|я)$', b): return "FI"
    if b.endswith("ь"): return "MI" if b in SOFT_M else "FI"
    return "MI"

def head_and_gender(name):
    # strip any existing markup
    name = re.sub(r'\{[^}]*\}', '', name)
    words = [clean(w) for w in name.split()]
    # leading segment: everything up to the first preposition / number
    seg = []
    for w in words:
        if w.lower() in PREP or is_number(w):
            break
        if w:
            seg.append(w)
    if not seg:
        seg = words[:1]
    prev_adj = None
    for w in seg:
        lw = w.lower()
        if lw in SKIP:
            continue
        if lw in NEUTER:
            return ("NI", "s", w)
        if lw.endswith("ся"):
            continue  # reflexive participle used as adjective
        if ADJ.match(lw):
            prev_adj = lw; continue  # leading adjective, remember for gender
        # head noun found
        if re.search(r'(ы|и)$', lw) and not lw.endswith("ь"):
            return ("MI", "p", w)                       # plural (gender-neutral)
        return (adj_gender(prev_adj) or noun_gender(w), "s", w)
    # no explicit noun (elided) -> infer from LAST word of the segment
    w = seg[-1]; lw = w.lower()
    if re.search(r'(ые|ие|ых|их|ыми|ими)$', lw): return ("MI", "p", w)
    if re.search(r'(ая|яя)$', lw): return ("FI", "s", w)
    if re.search(r'(ое|ее)$', lw): return ("NI", "s", w)
    return ("MI", "s", w)

def tag(name):
    g = head_and_gender(name)
    if not g: return name
    gender, num, word = g
    role = ".nnp" if num == "p" else ".nn"
    # replace first standalone occurrence of the head word
    pat = re.compile(r'(?<!\{\.)\b' + re.escape(word) + r'\b')
    repl = "{." + gender + "}" + word + "{" + role + "}"
    return pat.sub(repl, name, count=1)

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        line=line.rstrip("\n")
        if line: print(f"{line}\t=>\t{tag(line)}")
