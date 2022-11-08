# -*- coding: utf-8 -*-

"""
PROGRAME TYPE: PURE, UTF8 JSON → UTF8

IO DATA TYPES:
   • STDARG UTF8 JSON: WOI (Word Order Illustrator) export JSON file.
      Sample:
         {"sentences":[["en",["It"," is"," so","."]],["fr",["C'","est"," ainsi","."]]],"equivalency":[[[0],[0]],[[1,2],[1]],[[],[2]],[[],[]]]}
   • STDOUT UTF8: Pipe-separated list of subscripted texts in different languages.
      Sample:
         en|It₁ is₂ so₂.‖fr|C'₁est₂ ainsi₃.

PURPOSE:
   Mkpoli's “Word Order Illustrator” (https://word-order.mkpo.li/ | https://github.com/mkpoli/word-order/), henceforth referred to as “WOI”, is a tool for creating charts comparing morpheme orders between sentences of same meaning but in different languages.
   Once a word order chart has been created, WOI allows exporting it in JSON format; it is also possible to import back such JSON export files.
   The purpose of this Python program is to convert a WOI JSON into a plain text output listing two or more sentences in different languages, with each language-sentence pairs being separated by a double pipe character ⟪‖⟫, with each double-pipe being immediately followed by the language's name or ISO code, then a simple pipe character ⟪|⟫ followed by the sentence associated with the language; the sentence may be split into several chunks, each being followed by an ID written in subscript digits ⟪₀₁₂₃₄₅₆₇₈₉⟫, or alternatively with ⟪ₓ⟫. 
   When two chunks belonging to two different language-sentence pairs have the same ID, this means that they are homologous in role across the two sentences, and would be linked together and colored the same in the WOI interface. If the ID is ⟪ₓ⟫ however, this means the chunk has no correspondency in other languages. All chunks bearing the ⟪ₓ⟫ ID will be “ignored” with respect to cross-linking of same-purpose chunks between different language-sentence pairs.
   See the ⟪IO DATA TYPE⟫ section above for an example of well-formed output string.

USAGE EXAMPLES (WITH LINUX BASH):
   ⎈ python3 woi_json_from_text.py "en|It₁ is₂ so₂.‖fr|C'₁est₂ ainsi₃."
   ※ ↑ The output JSON will be written to STDOUT.
   
   ⎈ python3 woi_json_from_text.py "en|It₁ is₂ so₂.‖fr|C'₁est₂ ainsi₃." > woi_json.json
   ※ ↑ The output JSON will be written to a file named ⟪woi_json.json⟫.
   
   ⎈ python3 woi_json_from_text.py "en|It₁ is₂ so₂.‖fr|C'₁est₂ ainsi₃." | xsel -ib
   ※ ↑ The output JSON will be written to the clipboard.
"""

import sys, os, json, re

def entrypoint(self_path, woi_json):
  assert(isinstance(woi_json, str))
  t = ""
  for e in data_from_woi_data(json.loads(woi_json)):
    t += (e["language"] + "|" + textify(e["text_chunks"]) + "‖")
  if len(t) > 0:
    t = t[:-1]
  sys.stdout.write(f"{t}\n")
  return

def textify(text_chunks :dict):
  f = lambda n: "ₓ" if n is None else subscript_positional_notation(n)
  t = ""
  for e in text_chunks:
    t += (e["string"] + f(e["index"]))
  return t  

def data_from_woi_data(woi_data):
  woi_sentences = woi_data["sentences"]
  woi_equivalencies = woi_data["equivalency"]
  d = []
  for si, s in enumerate(woi_sentences):
    language, chunks = s
    d.append({
      "language": language,
      "text_chunks": chunks_from_woi_data(chunks, woi_equivalencies, si)
    })
  return d

def chunks_from_woi_data(woi_chunks, woi_equivalencies, si):
  return [
     {
       "string": c,
       "index": index_from_woi_data(ci, si, woi_equivalencies)
     } for ci, c in enumerate(woi_chunks)
  ]

def index_from_woi_data(ci, si, woi_equivalencies):
  for eqi, eql in enumerate(woi_equivalencies):
    if ci in eql[si]:
      return eqi
  return None

def subscript_positional_notation(number):
  return integer_positional_notation(number, "₀₁₂₃₄₅₆₇₈₉")

def integer_positional_notation(number, digits):
    # ⟦digits⟧ is a string or a sequence of all the digits used for encoding the number in positional notation; the number of digits is the target radix in which the number is to be encoded.
    radix = int(len(digits))
    n = int(number)
    if n == 0:
        return digits[0]
    s = ""
    while (n > 0):
        s = digits[n % radix] + s
        n //= radix
    return s


# === ENTRY POINT === #

entrypoint(*sys.argv)

