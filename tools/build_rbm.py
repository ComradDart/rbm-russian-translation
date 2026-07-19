# -*- coding: utf-8 -*-
import os, re, json, html

SCR=os.path.dirname(os.path.abspath(__file__))
# --- CONFIGURE: your Vortex staging folder that holds the RBM module ---
#     e.g. r"C:\Users\<you>\...\Vortex Mods\mountandblade2bannerlord"
#     (or set the VORTEX_STAGING environment variable instead of editing this)
STG=os.environ.get("VORTEX_STAGING", "")
if not STG:
    raise SystemExit("Set VORTEX_STAGING env var or edit STG to your Vortex staging path.")
BASE=os.path.join(STG,"RBM Modules-791-4-3-0-1779498523","Modules","RBM","ModuleData","Languages","LOC-eng.xml")
# output = the module folder shipped in this repo (next to tools/)
OUT=os.path.join(os.path.dirname(SCR), "RBM_Russian_Translation")

tr=json.load(open(os.path.join(SCR,"rbm_translations.json"),encoding="utf-8"))

# --- grammatical gender markup (TaleWorlds RU): tag each item name's head noun
#     so item modifiers (Легендарный/Надломленный/...) agree in gender & number.
#     Applied to item-name categories only (NOT UI/AI/config/troop/modifier text).
from tagger import tag
NAMECATS=("RBM_RAN_","RBM_ARR_","RBM_ARM_","RBM_CLA_","RBM_GLA_","RBM_HEA_","RBM_HAR_","RBM_LAN_","RBM_SHI_")
tr = {k: (tag(v) if k.startswith(NAMECATS) else v) for k, v in tr.items()}

# extra RBM items (ids present in RBM data but missing from RBM's own LOC-eng) -> tag too
extra_items = json.load(open(os.path.join(SCR,"rbm_extra_items.json"),encoding="utf-8"))
extra_items = {i: tag(t) for i, t in extra_items.items()}

rx_line_str=re.compile(r'^(\s*)<string\s+id="([^"]+)"\s+text="(.*)"\s*/?\s*>\s*$')
rx_comment=re.compile(r'^\s*<!--.*-->\s*$')
def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

langdir=os.path.join(OUT,"ModuleData","Languages","RU")
os.makedirs(langdir,exist_ok=True)

out=['﻿<?xml version="1.0" encoding="utf-8"?>',
     '<base xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" type="string">',
     '\t<tags>','\t\t<tag language="Русский" />','\t</tags>','\t<strings>']
n_tr=n_miss=n_extra=0; missing=[]; seen=set()
for raw in open(BASE,encoding="utf-8-sig"):
    line=raw.rstrip("\r\n")
    m=rx_line_str.match(line)
    if m:
        sid=m.group(2)
        if sid in tr:
            out.append(f'\t\t<string id="{sid}" text="{esc(tr[sid])}" />'); n_tr+=1; seen.add(sid)
        else:
            out.append(f'\t\t<string id="{sid}" text="{esc(html.unescape(m.group(3)))}" />'); n_miss+=1; missing.append(sid)
    elif rx_comment.match(line):
        out.append("\t\t"+line.strip())
# --- vanilla RU fixes (override Native strings by id; we load after Native) ---
# br0N6SSH = "Chipped" modifier: vanilla has a stray "?" after "Надломленный"
# that makes the declension engine drop the final "й" -> "Надломленны". Remove it.
vanilla_fix = {
    "br0N6SSH": "{adjectiveGenderCreator(ITEMNAME)}Надломленный{?IS_PLURAL_WORD_GROUP(ITEMNAME)}{.jp}{?}{.j}{\\?} {._}{ITEMNAME}{.n}",
}
out.append('\t\t<!-- Vanilla RU fixes -->')
for sid, txt in vanilla_fix.items():
    out.append(f'\t\t<string id="{sid}" text="{esc(txt)}" />')

out.append('\t\t<!-- Extra RBM item names (ids missing from RBM LOC-eng) -->')
for sid, txt in extra_items.items():
    out.append(f'\t\t<string id="{sid}" text="{esc(txt)}" />')

out.append('\t</strings>'); out.append('</base>')
with open(os.path.join(langdir,"LOC-rus.xml"),"w",encoding="utf-8",newline="\r\n") as o:
    o.write("\n".join(out)+"\n")

# translations present in JSON but not used (typo guard)
extra=[k for k in tr if k not in seen]

# language_data.xml
ld=['<?xml version="1.0" encoding="utf-8"?>',
    '<LanguageData id="Русский" name="Русский" subtitle_extension="ru" supported_iso="ru,rus,ru-ru,ru-md" text_processor="TaleWorlds.Localization.TextProcessor.LanguageProcessors.RussianTextProcessor" under_development="false">',
    '\t<LanguageFile xml_path="RU/LOC-rus.xml" />','</LanguageData>']
with open(os.path.join(langdir,"language_data.xml"),"w",encoding="utf-8",newline="\r\n") as o:
    o.write("\n".join(ld)+"\n")

# SubModule.xml
sm=['<?xml version="1.0" encoding="utf-8"?>','<Module>',
 '\t<Name value="RBM - Russian Translation"/>',
 '\t<Id value="RBM_Russian_Translation"/>',
 '\t<Version value="v1.0.0"/>',
 '\t<DefaultModule value="false"/>',
 '\t<ModuleCategory value="Singleplayer"/>',
 '\t<ModuleType value="Community"/>',
 '\t<Official value="false"/>',
 '\t<DependedModules>',
 '\t\t<DependedModule Id="Native"/>',
 '\t\t<DependedModule Id="RBM" Optional="true"/>',
 '\t</DependedModules>',
 '\t<DependedModuleMetadatas>',
 '\t\t<DependedModuleMetadata id="Native" order="LoadBeforeThis"/>',
 '\t\t<DependedModuleMetadata id="RBM" order="LoadBeforeThis" optional="true"/>',
 '\t</DependedModuleMetadatas>',
 '\t<SubModules/>','\t<Xmls/>','</Module>']
with open(os.path.join(OUT,"SubModule.xml"),"w",encoding="utf-8",newline="\r\n") as o:
    o.write("\n".join(sm)+"\n")

print(f"translated: {n_tr}   base-fallback(missing tr): {n_miss}   unused-json-keys: {len(extra)}")
if missing: print("MISSING:", missing)
if extra: print("UNUSED (id typo?):", extra)
print("-> ", langdir)
