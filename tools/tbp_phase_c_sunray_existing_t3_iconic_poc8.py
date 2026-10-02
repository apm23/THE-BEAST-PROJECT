#!/usr/bin/env python3
import os,re,sys,json,zipfile,hashlib,subprocess,tempfile,shutil
from pathlib import Path

VERSION="GH1_PHASE_C_SUNRAY_EXISTING_T3_ICONIC_POC8_V1"
FAMILY="dlc_ft_firearm_revolver_c_legendary_r"
T3="Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T3_Blueprint"
MARKER="TBP_PHASE_C_SUNRAY_EXISTING_T3_ICONIC_POC8_V1.marker.json"
COLLECT="scripts/inventory/collectables_ft.scr"

OLD_MARKERS=[
    "TBP_PHASE_C_38REVOLVER_EXISTING_BP_ICONIC_POC7_V1.marker.json",
    "TBP_PHASE_C_38REVOLVER_STANDALONE_ICONIC_POC6_V1.marker.json",
    "TBP_PHASE_C_38REVOLVER_ICONIC_POC5_REGISTRY_V1.marker.json",
    "TBP_PHASE_C_38REVOLVER_ICONIC_POC4_V1.marker.json",
    "TBP_PHASE_C_ICONIC_CHAIN_POC3_V1.marker.json",
    "TBP_PHASE_C_EXOTIC_ALL137_CANDIDATE_V2.marker.json",
    "TBP_PHASE_C_EXOTIC_POC1_PISTOL_B_LEGENDARY.marker.json",
]

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""): h.update(b)
    return h.hexdigest()

def nnum(p):
    m=re.fullmatch(r"data(\d+)\.pak",p.name,re.I)
    return int(m.group(1)) if m else -1

def find_game():
    roots=[]
    if os.name=="nt":
        for key,val in [(r"HKCU\Software\Valve\Steam","SteamPath"),
                        (r"HKLM\SOFTWARE\WOW6432Node\Valve\Steam","InstallPath")]:
            try:
                cp=subprocess.run(["reg","query",key,"/v",val],capture_output=True,text=True,timeout=5)
                m=re.search(rf"{re.escape(val)}\s+REG_\w+\s+(.+)$",cp.stdout,re.M)
                if m: roots.append(Path(m.group(1).strip()))
            except: pass
    for p in [os.path.expandvars(r"%ProgramFiles(x86)%\Steam"),
              os.path.expandvars(r"%ProgramFiles%\Steam"),r"C:\Steam"]:
        if "%" not in p: roots.append(Path(p))
    libs=[]
    for r in roots:
        if r.exists() and r not in libs: libs.append(r)
        v=r/"steamapps"/"libraryfolders.vdf"
        if v.exists():
            s=v.read_text(errors="ignore")
            for m in re.finditer(r'"path"\s*"([^"]+)"',s):
                q=Path(m.group(1).replace("\\\\","\\"))
                if q.exists() and q not in libs: libs.append(q)
    games=[]
    for l in libs:
        g=l/"steamapps"/"common"/"Dying Light The Beast"
        if (g/"ph_ft"/"source"/"data0.pak").exists(): games.append(g)
    if not games: raise RuntimeError("Game tidak ditemukan.")
    if len(games)>1: raise RuntimeError("Lebih dari satu instalasi ditemukan.")
    return games[0]

def read_entry(pak,name):
    try:
        with zipfile.ZipFile(pak) as z:
            mp={x.replace("\\","/").lower():x for x in z.namelist()}
            if name.lower() not in mp: return None
            return z.read(mp[name.lower()])
    except: return None

def effective(src,name):
    for p in sorted(src.glob("data*.pak"),key=nnum,reverse=True):
        b=read_entry(p,name)
        if b is not None:return p,b
    raise RuntimeError(name+" tidak ditemukan.")

def decode(b):
    for e in ("utf-8-sig","utf-8","cp1252","latin1"):
        try:return b.decode(e)
        except:pass
    return b.decode("latin1","ignore")

def item_block(text,name):
    m=re.search(rf'Item\s*\(\s*"{re.escape(name)}"\s*,\s*CategoryType_Collectable\s*\)\s*\{{',text,re.I)
    if not m: raise RuntimeError("Blueprint tidak ditemukan: "+name)
    brace=text.find("{",m.start()); d=0; ins=False; esc=False
    for i in range(brace,len(text)):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=="{": d+=1
            elif c=="}":
                d-=1
                if d==0:return m.start(),i+1,text[m.start():i+1]
    raise RuntimeError("Brace tidak balance.")

def cstr(b,name):
    m=re.search(rf'\b{re.escape(name)}\s*\(\s*"([^"]+)"\s*\)\s*;',b,re.I)
    return m.group(1) if m else None

def patch(raw):
    text=decode(raw)
    a,b,orig=item_block(text,T3)
    if cstr(orig,"ScaleWithPlayerRank") != FAMILY:
        raise RuntimeError("Family mismatch.")
    if not re.search(r'Color\s*\(\s*Color_Orange\s*\)\s*;',orig,re.I):
        if re.search(r'Color\s*\(\s*Color_Exotic\s*\)\s*;',orig,re.I):
            raise RuntimeError("Target sudah Color_Exotic; POC8 kemungkinan sudah aktif.")
        raise RuntimeError("Target T3 bukan Color_Orange.")
    patched_block=re.sub(r'Color\s*\(\s*Color_Orange\s*\)\s*;','Color(Color_Exotic);',orig,count=1,flags=re.I)
    text=text[:a]+patched_block+text[b:]
    _,_,chk=item_block(text,T3)
    required_patterns=[
        r'\bItemLevel\s*\(\s*3\s*,\s*3\s*\)\s*;',
        r'\bRequiredItemToShowInShop\s*\(',
        r'\bAlternativePrice\s*\(',
        r'\bScaleWithPlayerRank\s*\(\s*"'+re.escape(FAMILY)+r'"\s*\)\s*;',
        r'\bColor\s*\(\s*Color_Exotic\s*\)\s*;',
    ]
    for p in required_patterns:
        if not re.search(p,chk,re.I): raise RuntimeError("Validation field missing: "+p)
    def scrub_color(x):
        return re.sub(r'Color\s*\(\s*Color_(?:Orange|Exotic)\s*\)\s*;','Color(__RARITY__);',x,flags=re.I)
    if scrub_color(orig)!=scrub_color(chk):
        raise RuntimeError("Unexpected T3 mutation outside Color().")
    return text.encode("utf-8"),orig,chk

def zi(name):
    z=zipfile.ZipInfo(name,(2020,1,1,0,0,0))
    z.compress_type=zipfile.ZIP_DEFLATED
    z.external_attr=0x01800000
    z.create_system=3
    return z

def writepak(path,collect,marker):
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr(zi(COLLECT),collect)
        z.writestr(zi(MARKER),json.dumps(marker,indent=2))
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None: raise RuntimeError("PAK CRC fail.")

def marked(src,marker):
    return [p for p in src.glob("data*.pak") if read_entry(p,marker) is not None]

def cleanup_old(src):
    for marker in OLD_MARKERS:
        for p in marked(src,marker):
            p.unlink()
            print("AUTO-REMOVED OLD EXPERIMENT:",p.name,marker)

def install():
    g=find_game(); src=g/"ph_ft"/"source"
    if marked(src,MARKER): raise RuntimeError("POC8 sudah terinstall.")
    cleanup_old(src)
    base,raw=effective(src,COLLECT)
    patched,before,after=patch(raw)
    nums=[nnum(p) for p in src.glob("data*.pak") if nnum(p)>=0]
    n=max(nums)+1
    if n>7: raise RuntimeError("Slot berikutnya > data7.")
    out=src/f"data{n}.pak"; tmp=src/f".{out.name}.{os.getpid()}.tmp"
    marker={"version":VERSION,"target_ui_observed":"Sunray","target_family":FAMILY,"target_blueprint_id":T3,
            "source":base.name,"mutation":"Color_Orange -> Color_Exotic ONLY; all upgrade metadata preserved",
            "new_blueprint_created":False}
    writepak(tmp,patched,marker)
    os.replace(tmp,out)
    print("INSTALLED:",out)
    print("TARGET UI OBSERVED: Sunray")
    print("TARGET EXISTING T3:",T3)
    print("ONLY CHANGE: Color_Orange -> Color_Exotic")
    print("ItemLevel / AlternativePrice / RequiredItemToShowInShop preserved.")
    print("SHA256:",sha_file(out))

def uninstall():
    g=find_game(); src=g/"ph_ft"/"source"
    arr=marked(src,MARKER)
    if not arr: print("POC8 absent"); return
    for p in arr:
        p.unlink(); print("REMOVED:",p)

def status():
    g=find_game(); src=g/"ph_ft"/"source"
    print("POC8:", "INSTALLED" if marked(src,MARKER) else "ABSENT")
    base,raw=effective(src,COLLECT); t=decode(raw)
    _,_,b=item_block(t,T3)
    print("EFFECTIVE:",base.name)
    print("TARGET UI OBSERVED: Sunray")
    cm=re.search(r'Color\s*\(\s*([A-Za-z0-9_]+)\s*\)',b,re.I)
    il=re.search(r'ItemLevel\s*\(([^)]*)\)',b,re.I)
    print("COLOR:",cm.group(1) if cm else "<none>")
    print("ITEMLEVEL:",il.group(1) if il else "<none>")
    print("REQUIRED_ITEM_TO_SHOW:",bool(re.search(r'\bRequiredItemToShowInShop\s*\(',b,re.I)))
    print("ALTERNATIVE_PRICE:",bool(re.search(r'\bAlternativePrice\s*\(',b,re.I)))
    print("NEXT:",bool(re.search(r'\bNextLevelBlueprintName\s*\(',b,re.I)))
    print("FAMILY:",cstr(b,"ScaleWithPlayerRank"))
    print("UID:",cstr(b,"UID"))

def selftest():
    src=("Sub X()\r\n{\r\n"
         f'Item("{T3}", CategoryType_Collectable)\r\n{{\r\n'
         'Name("&SUNRAY_N&");\r\nDescription("&SUNRAY_D&");\r\nItemType(ItemType_CraftPlan);\r\n'
         'CraftplanType("Weapon");\r\nRequiredItem("Craft_Scrap",35);\r\nColor(Color_Orange);\r\n'
         f'ScaleWithPlayerRank("{FAMILY}");\r\nHudIcon("blueprint_b");\r\n'
         'AlternativePrice("DLC_FT_UpgradeComponent_T3",1);\r\nAlternativePrice("Craft_Scrap",40);\r\n'
         'RequiredItemToShowInShop("Craftplan_X_T2_Blueprint");\r\nItemLevel(3,3);\r\nUID("777");\r\n}}\r\n}}\r\n').encode()
    patched,before,after=patch(src)
    assert "Color(Color_Exotic);" in after
    assert "ItemLevel(3,3);" in after
    assert 'AlternativePrice("DLC_FT_UpgradeComponent_T3",1);' in after
    assert 'RequiredItemToShowInShop("Craftplan_X_T2_Blueprint");' in after
    assert cstr(before,"UID")==cstr(after,"UID")=="777"
    td=Path(tempfile.mkdtemp())
    try:
        out=td/"data6.pak"; writepak(out,patched,{"version":VERSION})
        assert zipfile.ZipFile(out).testzip() is None
    finally: shutil.rmtree(td,ignore_errors=True)
    print("SELFTEST PASS")
    print("Exact existing Sunray T3: Color-only mutation; upgrade chain metadata byte-preserved.")

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=["install","uninstall","status","selftest"])
    a=ap.parse_args()
    try: globals()[a.action]()
    except Exception as e:
        print("FAIL:",e); sys.exit(1)
