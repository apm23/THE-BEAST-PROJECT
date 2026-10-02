#!/usr/bin/env python3
import os,re,sys,json,zipfile,hashlib,subprocess,tempfile,shutil
from pathlib import Path

VERSION="GH1_PHASE_C_38REVOLVER_EXISTING_BP_ICONIC_POC7_V1"
FAMILY="dlc_ft_firearm_revolver_c_legendary_r"
T3="Craftplan_GH1_dlc_ft_firearm_revolver_c_legendary_T3_Blueprint"
MARKER="TBP_PHASE_C_38REVOLVER_EXISTING_BP_ICONIC_POC7_V1.marker.json"
COLLECT="scripts/inventory/collectables_ft.scr"

OLD_MARKERS=[
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
        if (g/"ph_ft"/"source"/"data0.pak").exists():
            games.append(g)
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
        if b is not None: return p,b
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
                if d==0: return m.start(),i+1,text[m.start():i+1]
    raise RuntimeError("Brace tidak balance.")

def cstr(b,name):
    m=re.search(rf'\b{re.escape(name)}\s*\(\s*"([^"]+)"\s*\)\s*;',b,re.I)
    return m.group(1) if m else None

def remove_call(block,name):
    return re.sub(
        rf'^[ \t]*{re.escape(name)}\s*\([^;]*\)\s*;[ \t]*(?:\r?\n)?',
        '',
        block,
        flags=re.I|re.M
    )

def patch(raw):
    text=decode(raw)
    a,b,t3=item_block(text,T3)
    if cstr(t3,"ScaleWithPlayerRank") != FAMILY:
        raise RuntimeError("Family mismatch.")

    if not re.search(r'Color\s*\(\s*Color_Orange\s*\)\s*;',t3,re.I):
        if re.search(r'Color\s*\(\s*Color_Exotic\s*\)\s*;',t3,re.I):
            raise RuntimeError("Target sudah Color_Exotic; POC7 kemungkinan sudah aktif.")
        raise RuntimeError("Target T3 bukan Color_Orange expected.")

    original=t3
    t3=re.sub(r'Color\s*\(\s*Color_Orange\s*\)\s*;','Color(Color_Exotic);',t3,count=1,flags=re.I)

    for call in ("ItemLevel","NextLevelBlueprintName","RequiredItemToShowInShop","AlternativePrice"):
        t3=remove_call(t3,call)

    text=text[:a]+t3+text[b:]
    _,_,chk=item_block(text,T3)
    if 'Color(Color_Exotic);'.lower() not in chk.lower():
        raise RuntimeError("Color_Exotic validation gagal.")
    if cstr(chk,"ScaleWithPlayerRank") != FAMILY:
        raise RuntimeError("ScaleWithPlayerRank berubah.")
    for forbidden in ("ItemLevel","NextLevelBlueprintName","RequiredItemToShowInShop","AlternativePrice"):
        if re.search(rf'\b{forbidden}\s*\(',chk,re.I):
            raise RuntimeError("Masih ada field progression: "+forbidden)

    for identity_call in ("Name","Description","ScaleWithPlayerRank","HudIcon","UID"):
        before=cstr(original,identity_call)
        after=cstr(chk,identity_call)
        if before != after:
            raise RuntimeError(f"Identity field berubah: {identity_call}: {before} -> {after}")

    return text.encode("utf-8"), original, chk

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
    if marked(src,MARKER): raise RuntimeError("POC7 sudah terinstall.")

    cleanup_old(src)
    base,raw=effective(src,COLLECT)
    patched,before,after=patch(raw)

    nums=[nnum(p) for p in src.glob("data*.pak") if nnum(p)>=0]
    n=max(nums)+1
    if n>7: raise RuntimeError("Slot berikutnya > data7.")
    out=src/f"data{n}.pak"; tmp=src/f".{out.name}.{os.getpid()}.tmp"

    marker={
        "version":VERSION,
        "target_family":FAMILY,
        "target_blueprint_id":T3,
        "source":base.name,
        "architecture":"same existing owned blueprint ID converted from terminal Legendary definition to native-style standalone Color_Exotic/Iconic",
        "new_blueprint_created":False
    }
    writepak(tmp,patched,marker)
    os.replace(tmp,out)

    print("INSTALLED:",out)
    print("SOURCE:",base.name)
    print("TARGET EXISTING BLUEPRINT:",T3)
    print("NEW BLUEPRINT CREATED: NO")
    print("SAME OWNERSHIP ID: YES")
    print("SHA256:",sha_file(out))
    print("")
    print("Buka workbench -> .38 Revolver yang SUDAH lu punya.")
    print("Expected test: label blueprint berubah dari LEGENDARY BLUEPRINT menjadi ICONIC BLUEPRINT.")

def uninstall():
    g=find_game(); src=g/"ph_ft"/"source"
    arr=marked(src,MARKER)
    if not arr:
        print("POC7 absent")
        return
    for p in arr:
        p.unlink()
        print("REMOVED:",p)

def status():
    g=find_game(); src=g/"ph_ft"/"source"
    print("POC7:", "INSTALLED" if marked(src,MARKER) else "ABSENT")
    base,raw=effective(src,COLLECT); t=decode(raw)
    _,_,b=item_block(t,T3)
    print("EFFECTIVE:",base.name)
    print("TARGET ID:",T3)
    cm=re.search(r'Color\s*\(\s*([A-Za-z0-9_]+)\s*\)',b,re.I)
    print("COLOR:",cm.group(1) if cm else "<none>")
    print("ITEMLEVEL_PRESENT:",bool(re.search(r'\bItemLevel\s*\(',b,re.I)))
    print("NEXT_PRESENT:",bool(re.search(r'\bNextLevelBlueprintName\s*\(',b,re.I)))
    print("SHOP_GATE_PRESENT:",bool(re.search(r'\bRequiredItemToShowInShop\s*\(',b,re.I)))
    print("ALTPRICE_PRESENT:",bool(re.search(r'\bAlternativePrice\s*\(',b,re.I)))
    print("FAMILY:",cstr(b,"ScaleWithPlayerRank"))
    print("UID:",cstr(b,"UID"))

def selftest():
    src=(
        "Sub X()\r\n{\r\n"
        f'Item("{T3}", CategoryType_Collectable)\r\n'
        "{\r\n"
        'Name("&REV_N&");\r\n'
        'Description("&REV_D&");\r\n'
        'ItemType(ItemType_CraftPlan);\r\n'
        'CraftplanType("Weapon");\r\n'
        'RequiredItem("Craft_Scrap",35);\r\n'
        'Color(Color_Orange);\r\n'
        f'ScaleWithPlayerRank("{FAMILY}");\r\n'
        'HudIcon("blueprint_b");\r\n'
        'AlternativePrice("DLC_FT_UpgradeComponent_T3",1);\r\n'
        'AlternativePrice("Craft_Scrap",40);\r\n'
        'RequiredItemToShowInShop("Craftplan_X_T2_Blueprint");\r\n'
        'ItemLevel(3,3);\r\n'
        'UID("777");\r\n'
        "}\r\n"
        "}\r\n"
    ).encode()

    patched,before,after=patch(src)
    t=patched.decode()
    assert f'Item("{T3}", CategoryType_Collectable)' in t
    assert "Color(Color_Exotic);" in after
    for x in ("ItemLevel(","NextLevelBlueprintName(","RequiredItemToShowInShop(","AlternativePrice("):
        assert x not in after
    assert cstr(before,"UID")==cstr(after,"UID")=="777"
    assert cstr(before,"Name")==cstr(after,"Name")
    assert cstr(before,"ScaleWithPlayerRank")==cstr(after,"ScaleWithPlayerRank")==FAMILY

    td=Path(tempfile.mkdtemp())
    try:
        out=td/"data6.pak"
        writepak(out,patched,{"version":VERSION})
        assert zipfile.ZipFile(out).testzip() is None
    finally:
        shutil.rmtree(td,ignore_errors=True)

    print("SELFTEST PASS")
    print("Same T3 blueprint ID/UID/identity retained; only terminal Legendary progression metadata -> standalone Color_Exotic/Iconic style.")

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("action",choices=["install","uninstall","status","selftest"])
    a=ap.parse_args()
    try:
        globals()[a.action]()
    except Exception as e:
        print("FAIL:",e)
        sys.exit(1)
