# -*- coding: utf-8 -*-

"""
PROGRAME TYPE: PURE, UTF8 → UTF8 JSON

IO DATA TYPES:
   • STDARG UTF8: Pipe-separated list of subscripted texts in different languages.
      Sample:
         en|It₁ is₂ so₂.‖fr|C'₁est₂ ainsi₃.
   • STDOUT UTF8 JSON: WOI (Word Order Illustrator) export JSON file.
      Sample:
         {"sentences":[["en",["It"," is"," so","."]],["fr",["C'","est"," ainsi","."]]],"equivalency":[[[0],[0]],[[1,2],[1]],[[],[2]],[[],[]]]}

PURPOSE:
   Mkpoli's “Word Order Illustrator” (https://word-order.mkpo.li/ | https://github.com/mkpoli/word-order/), henceforth referred to as “WOI”, is a tool for creating charts comparing morpheme orders between sentences of same meaning but in different languages.
   Once a word order chart has been created, WOI allows exporting it in JSON format; it is also possible to import back such JSON export files.
   The purpose of this Python program is to create a WOI JSON file out of a plain text input listing two or more sentences in different languages, with each language-sentence pairs being separated by a double pipe character ⟪‖⟫, with each double-pipe being immediately followed by the language's name or ISO code, then a simple pipe character ⟪|⟫ followed by the sentence associated with the language; the sentence may be split into several chunks, each being followed by an ID written in subscript digits ⟪₀₁₂₃₄₅₆₇₈₉⟫, or alternatively with ⟪ₓ⟫. 
   When two chunks belonging to two different language-sentence pairs have the same ID, this means that they are homologous in role across the two sentences, and would be linked together and colored the same in the WOI interface. If the ID is ⟪ₓ⟫ however, this means the chunk has no correspondency in other languages. All chunks bearing the ⟪ₓ⟫ ID will be “ignored” with respect to cross-linking of same-purpose chunks between different language-sentence pairs.
   See the ⟪IO DATA TYPE⟫ section above for an example of well-formed input string.

USAGE EXAMPLES (WITH LINUX BASH):
   ⎈ python3 text_from_woi_json.py "$(< woi_json.json)"
   ※ ↑ The input JSON is first loaded from a file named ⟪woi_json.json⟫, then is passed as the STDARG input of the program.
   
   ⎈ python3 text_from_woi_json.py "$(xsel -ob)"
    ※ ↑ The input JSON is first loaded from the clipboard (provided you first copied it to the clipboard), then is passed as the STDARG input of the program.
"""

import sys, os, json, re

def entrypoint(self_path :str, text :str):
  assert(isinstance(text, str))
  data = []
  for e in text.split("‖"):
    r = e.split("|")
    data.append({"language": r[0], "text_chunks": parse(r[1])})
  # save_as_json_file(woi_data_from(data), path)
  sys.stdout.write(json.dumps(
    woi_data_from(data),
    separators = (',', ':'),
    ensure_ascii = False)
    + '\n'
  )
  return

def parse(s :str):
  lst = re.split(r"([₀₁₂₃₄₅₆₇₈₉ₓ]+)", s)
  if len(lst) > 0 and lst[-1] == "":
    lst = lst[0:-1]
  text_chunks = []
  l = len(lst)
  i = 0
  while i < l:
    nxt = i + 1
    if nxt >= l or lst[nxt] == "ₓ":
      idx = None
    else:
      idx = integer_from_subscript_positional_notation(lst[nxt])
    text_chunks.append({"string": lst[i], "index": idx})
    i += 2
  return text_chunks

def woi_data_from(data :list):
  f = lambda x: [e["string"] for e in x]
  woi_sentences = [[e["language"], f(e["text_chunks"])] for e in data]
  woi_equivalencies = []
  index = 1
  while True:
    eq = []
    was_index_found = False
    for e in data:
      was_index_found_in_e = False
      for i, x in enumerate(e["text_chunks"]):
        if x["index"] == index:
          if not was_index_found_in_e:
            eq.append([i])
          else:
            eq[-1] += [i]
          was_index_found_in_e = True
          was_index_found = True
      if not was_index_found_in_e:
        eq.append([])
    woi_equivalencies.append(eq)
    if not was_index_found:
      break
    index += 1
  return {"sentences": woi_sentences, "equivalency": woi_equivalencies}

def integer_from_subscript_positional_notation(positional_notation):
  return integer_from_positional_notation(positional_notation, "₀₁₂₃₄₅₆₇₈₉")

def integer_from_positional_notation(positional_notation, digits):
    radix = int(len(digits))
    n = 0
    i = len(positional_notation) - 1
    magnitude = 0
    while (i >= 0):
      ## if positional_notation[i] not in digits:
      ##   print(f"⚠ integer_from_positional_notation: ⟪{positional_notation[i]}⟫ ∉ {str(digits)}")
      v = digits.index(positional_notation[i])
      n += v * pow(radix, magnitude)
      i -= 1
      magnitude += 1
    return n


# === ENTRY POINT === #

entrypoint(*sys.argv)

