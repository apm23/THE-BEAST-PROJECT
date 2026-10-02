#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, string, sys, zipfile
from pathlib import Path

VERSION = 'GH1_PHASE_C_EXOTIC_POC1_PISTOL_B_LEGENDARY_V1'
MARKER = 'TBP_PHASE_C_EXOTIC_POC1_PISTOL_B_LEGENDARY.marker.json'
COLLECTABLES = 'scripts/inventory/collectables_ft.scr'
TARGET_FAMILY = 'dlc_ft_firearm_pistol_b_legendary_r'
BP1 = 'Craftplan_GH1_dlc_ft_firearm_pistol_b_legendary_T1_Blueprint'
BP2 = 'Craftplan_GH1_dlc_ft_firearm_pistol_b_legendary_T2_Blueprint'
BP3 = 'Craftplan_GH1_dlc_ft_firearm_pistol_b_legendary_T3_Blueprint'
BP4 = 'Craftplan_GH1_dlc_ft_firearm_pistol_b_legendary_T4_Blueprint'


def norm(s:str)->str:
    return s.replace('\\','/').lower()

def dec(b:bytes)->str:
    return b.decode('latin1')

def enc(s:str)->bytes:
    return s.encode('latin1')

def pak_number(p:Path):
    m=re.fullmatch(r'data(\d+)\.pak',p.name,re.I)
    return int(m.group(1)) if m else None

def read_member(zp:Path,wanted:str):
    t=norm(wanted)
    try:
        with zipfile.ZipFile(zp,'r') as z:
            for n in z.namelist():
                if norm(n)==t:
                    return z.read(n)
    except (zipfile.BadZipFile,OSError):
        return None
    return None

def find_matching_brace(text:str,open_idx:int)->int:
    depth=0; in_str=False; esc=False
    for i in range(open_idx,len(text)):
        ch=text[i]
        if in_str:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': in_str=False
            continue
        if ch=='"': in_str=True
        elif ch=='{': depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:return i
    raise RuntimeError('Unmatched brace')

def item_block(text:str,name:str):
    rx=re.compile(r'(?mi)^\s*Item\("'+re.escape(name)+r'"\s*,\s*CategoryType_Collectable\)\s*\{')
    m=rx.search(text)
    if not m:return None
    oi=text.find('{',m.end()-1)
    ei=find_matching_brace(text,oi)
    return m.start(),ei+1,text[m.start():ei+1]

def field(block:str,pat:str,flags=re.I):
    m=re.search(pat,block,flags)
    return m.group(1) if m else None

def update_itemlevel(block:str,tier:int):
    rx=re.compile(r'ItemLevel\(\s*'+str(tier)+r'\s*,\s*3\s*\)\s*;',re.I)
    out,n=rx.subn(f'ItemLevel({tier}, 4);',block,count=1)
    if n!=1:
        raise RuntimeError(f'Expected ItemLevel({tier}, 3) in tier {tier} block')
    return out

def add_next_to_t3(block:str,new_next:str):
    if re.search(r'NextLevelBlueprintName\s*\(',block,re.I):
        raise RuntimeError('T3 unexpectedly already has NextLevelBlueprintName')
    m=re.search(r'(?mi)^(\s*)ItemLevel\(\s*3\s*,\s*4\s*\)\s*;\s*$',block)
    if not m: raise RuntimeError('Patched T3 ItemLevel(3, 4) not found')
    ins=m.group(0)+f'\r\n{m.group(1)}NextLevelBlueprintName("{new_next}");'
    return block[:m.start()]+ins+block[m.end():]

def deterministic_uid(family:str)->str:
    h=int(hashlib.sha256((family+'|EXOTIC_T4_POC1').encode()).hexdigest()[:16],16)
    return str(7000000000000000000 + (h % 900000000000000000))

def build_t4_from_t3(t3:str)->str:
    name=field(t3,r'Name\("([^"]+)"\)')
    desc=field(t3,r'Description\("([^"]+)"\)')
    price=field(t3,r'Price\(([^\)]+)\)') or '650'
    mesh=field(t3,r'Mesh\("([^"]+)"\)') or 'blueprint.msh'
    skin=field(t3,r'Skin\("([^"]+)"\)') or 'default'
    fam=field(t3,r'ScaleWithPlayerRank\("([^"]+)"\)')
    hud=field(t3,r'HudIcon\("([^"]+)"\)') or 'blueprint_b'
    snd=field(t3,r'CraftingSound\("([^"]+)"\)') or 'dlc_ft_menu_craft_item_weapon_success'
    snd0=field(t3,r'CraftingSoundStart\("([^"]+)"\)') or 'dlc_ft_menu_craft_item_weapon_start'
    if not all([name,desc,fam]): raise RuntimeError('Could not extract T3 identity fields')
    if fam.lower()!=TARGET_FAMILY: raise RuntimeError(f'T3 family mismatch: {fam}')
    uid=deterministic_uid(TARGET_FAMILY)
    return (
        f'\r\n    // TBP PHASE C EXOTIC POC1 - native-style T4 Exotic\r\n'
        f'    Item("{BP4}", CategoryType_Collectable)\r\n'
        f'    {{\r\n'
        f'        Name("{name}");\r\n'
        f'        Description("{desc}");\r\n'
        f'        ItemType(ItemType_CraftPlan);\r\n'
        f'        CraftplanType("Weapon");\r\n'
        f'        Price({price});\r\n'
        f'        Mesh("{mesh}");\r\n'
        f'        Skin("{skin}");\r\n'
        f'        RequiredItem("Craft_Scrap", 35);\r\n'
        f'        RequiredItem("Craft_wiring", 12);\r\n'
        f'        RequiredItem("Craft_Leather", 12);\r\n'
        f'        RequiredItem("Craft_Firearm_Scrap_FT", 6);\r\n'
        f'        Color(Color_Exotic);\r\n'
        f'        ScaleWithPlayerRank("{fam}");\r\n'
        f'        HudIcon("{hud}");\r\n'
        f'        CraftingSound("{snd}");\r\n'
        f'        CraftingSoundStart("{snd0}");\r\n'
        f'        GameVersion(9);\r\n'
        f'        UID("{uid}");\r\n'
        f'    }}\r\n'
    )

def patch_collectables(text:str):
    if BP4.lower() in text.lower():
        raise RuntimeError('POC T4 blueprint already exists in effective collectables; uninstall old POC first')
    blocks={}
    for tier,bp in [(1,BP1),(2,BP2),(3,BP3)]:
        b=item_block(text,bp)
        if not b: raise RuntimeError(f'Missing generated tier {tier} blueprint: {bp}')
        blocks[tier]=b
    edits=[]
    for tier in (1,2,3):
        s,e,b=blocks[tier]
        nb=update_itemlevel(b,tier)
        if tier==3: nb=add_next_to_t3(nb,BP4)
        edits.append((s,e,nb))
    out=text
    for s,e,nb in sorted(edits,reverse=True):
        out=out[:s]+nb+out[e:]
    b3=item_block(out,BP3)
    if not b3: raise RuntimeError('Patched T3 block lost')
    t4=build_t4_from_t3(b3[2])
    out=out[:b3[1]]+t4+out[b3[1]:]
    validate(out)
    return out

def validate(text:str):
    for tier,bp in [(1,BP1),(2,BP2),(3,BP3),(4,BP4)]:
        b=item_block(text,bp)
        if not b: raise RuntimeError(f'Validation missing T{tier}')
        body=b[2]
        fam=field(body,r'ScaleWithPlayerRank\("([^"]+)"\)')
        if not fam or fam.lower()!=TARGET_FAMILY: raise RuntimeError(f'T{tier} family mismatch')
        if tier<=3:
            if not re.search(rf'ItemLevel\(\s*{tier}\s*,\s*4\s*\)',body,re.I):
                raise RuntimeError(f'T{tier} max level was not raised to 4')
        else:
            if not re.search(r'Color\(Color_Exotic\)',body,re.I): raise RuntimeError('T4 is not Color_Exotic')
            if re.search(r'ItemLevel\s*\(',body,re.I): raise RuntimeError('T4 should mirror native Exotic and omit ItemLevel')
    t3=item_block(text,BP3)[2]
    if not re.search(r'NextLevelBlueprintName\("'+re.escape(BP4)+r'"\)',t3,re.I):
        raise RuntimeError('T3 does not point to T4')
    return True

def find_steam_root():
    if os.name=='nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Valve\Steam') as k:
                v,_=winreg.QueryValueEx(k,'SteamPath'); return Path(v) if v else None
        except Exception: pass
    return None

def candidate_game_dirs():
    seen=set();out=[];cand=[];steam=find_steam_root()
    if steam:cand.append(steam/'steamapps/common/Dying Light The Beast')
    for d in string.ascii_uppercase:
        r=Path(f'{d}:/')
        cand += [r/'Program Files (x86)/Steam/steamapps/common/Dying Light The Beast',r/'Program Files/Steam/steamapps/common/Dying Light The Beast',r/'SteamLibrary/steamapps/common/Dying Light The Beast',r/'Steam/steamapps/common/Dying Light The Beast',r/'Games/Steam/steamapps/common/Dying Light The Beast',r/'Games/SteamLibrary/steamapps/common/Dying Light The Beast']
    for p in cand:
        k=str(p).lower()
        if k in seen:continue
        seen.add(k)
        if (p/'ph_ft/source/data0.pak').exists():out.append(p)
    return out

def select_game_dir(explicit=None):
    if explicit:
        p=Path(explicit.strip('"')).resolve()
        if not (p/'ph_ft/source/data0.pak').exists(): raise RuntimeError(f'Invalid game folder: {p}')
        return p
    ds=candidate_game_dirs()
    if len(ds)==1:return ds[0]
    if len(ds)>1:
        print('Multiple installs found:')
        for i,d in enumerate(ds,1):print(f' {i}. {d}')
        q=input('Choose number: ').strip()
        if q.isdigit() and 1<=int(q)<=len(ds):return ds[int(q)-1]
    return select_game_dir(input('Paste Dying Light The Beast game folder: ').strip())

def effective_collectables(source:Path):
    arr=[]
    for p in source.glob('data*.pak'):
        n=pak_number(p)
        if n is None:continue
        b=read_member(p,COLLECTABLES)
        if b is not None:arr.append((n,p,b))
    if not arr: raise RuntimeError('No collectables_ft.scr found in data*.pak')
    return max(arr,key=lambda x:x[0])

def marker_paks(source:Path):
    return [p for p in source.glob('data*.pak') if read_member(p,MARKER) is not None]

def next_pak(source:Path):
    nums=[pak_number(p) for p in source.glob('data*.pak')]
    nums=[n for n in nums if n is not None]
    return source/f'data{max(nums+[1])+1}.pak'

def install(game:Path):
    source=game/'ph_ft/source'
    mp=marker_paks(source)
    if mp:
        raise RuntimeError('POC1 already installed: '+', '.join(map(str,mp)))
    n,base,raw=effective_collectables(source)
    patched=patch_collectables(dec(raw))
    out=next_pak(source)
    marker={
      'version':VERSION,'target_family':TARGET_FAMILY,'base_pak':str(base),'base_data_number':n,
      'member':COLLECTABLES,'t4_blueprint':BP4,
      'changes':['T1 ItemLevel 1/3 -> 1/4','T2 ItemLevel 2/3 -> 2/4','T3 ItemLevel 3/3 -> 3/4','T3 NextLevelBlueprintName -> T4','add native-style Color_Exotic T4 without ItemLevel'],
      'phase_b_loot_modified':False
    }
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_STORED) as z:
        z.writestr(COLLECTABLES,enc(patched))
        z.writestr(MARKER,json.dumps(marker,indent=2).encode('utf-8'))
    rb=read_member(out,COLLECTABLES)
    if rb is None: raise RuntimeError('Created PAK cannot be read back')
    validate(dec(rb))
    print('\n============================================================')
    print(' GH1 PHASE C EXOTIC POC1 INSTALLED')
    print('============================================================')
    print('Target family :',TARGET_FAMILY)
    print('T4 blueprint  :',BP4)
    print('Output PAK    :',out)
    print('Base          :',base)
    print('Loot changed  : NO')
    print('\nTEST: open workbench -> weapon blueprint upgrade. Upgrade this target blueprint from T3 to T4. Expected final rarity: EXOTIC.')
    print('After crafting/upgrading, save/reload once and report whether Exotic + weapon stats persist.')
    return 0

def uninstall(game:Path):
    source=game/'ph_ft/source'; mp=marker_paks(source)
    if not mp:
        print('POC1 marker not found. Nothing removed.'); return 0
    if len(mp)!=1: raise RuntimeError('Safety stop: multiple POC1 marker PAKs: '+', '.join(map(str,mp)))
    p=mp[0]; p.unlink()
    print('Removed only POC1 marker PAK:',p)
    return 0

def status(game:Path):
    source=game/'ph_ft/source';mp=marker_paks(source)
    print('Installed marker PAKs:',len(mp))
    for p in mp:print(' -',p)
    n,p,b=effective_collectables(source)
    print('Effective collectables:',p)
    text=dec(b)
    print('Target T1:',bool(item_block(text,BP1)))
    print('Target T2:',bool(item_block(text,BP2)))
    print('Target T3:',bool(item_block(text,BP3)))
    print('Target T4:',bool(item_block(text,BP4)))
    if item_block(text,BP4): validate(text); print('POC structure: PASS')
    return 0

def selftest():
    fam=TARGET_FAMILY
    def block(bp,tier,color,nxt=None):
        nxtline=f'        NextLevelBlueprintName("{nxt}");\r\n' if nxt else ''
        return (f'    Item("{bp}", CategoryType_Collectable)\r\n    {{\r\n'
                f'        Name("&test_n&");\r\n        Description("&test_d&");\r\n'
                f'        ItemType(ItemType_CraftPlan);\r\n        CraftplanType("Weapon");\r\n        Price(650);\r\n'
                f'        Mesh("blueprint.msh");\r\n        Skin("default");\r\n        RequiredItem("Craft_Scrap", 10);\r\n'
                f'        Color({color});\r\n        ScaleWithPlayerRank("{fam}");\r\n        HudIcon("blueprint_b");\r\n'
                f'        ItemLevel({tier}, 3);\r\n{nxtline}'
                f'        CraftingSound("dlc_ft_menu_craft_item_weapon_success");\r\n        CraftingSoundStart("dlc_ft_menu_craft_item_weapon_start");\r\n'
                f'        GameVersion(8);\r\n        UID("1234567890123456789");\r\n    }}\r\n')
    s='sub main()\r\n{\r\n'+block(BP1,1,'Color_Blue',BP2)+block(BP2,2,'Color_Violet',BP3)+block(BP3,3,'Color_Orange')+'}\r\n'
    p=patch_collectables(s)
    assert BP4 in p and 'Color(Color_Exotic)' in p and 'ItemLevel(3, 4)' in p
    validate(p)
    print('SELFTEST PASS: generated T1/T2/T3 -> native-style Exotic T4 chain; loot untouched')
    return 0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['install','uninstall','status','selftest'])
    ap.add_argument('--game')
    a=ap.parse_args()
    if a.action=='selftest':return selftest()
    game=select_game_dir(a.game)
    return {'install':install,'uninstall':uninstall,'status':status}[a.action](game)

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as e:
        print('\n[FAIL]',e,file=sys.stderr)
        raise
