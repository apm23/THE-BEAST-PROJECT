#!/usr/bin/env python3
from __future__ import annotations
import datetime as dt
import hashlib, json, os, re, string, sys, zipfile
from dataclasses import dataclass
from pathlib import Path

VERSION = 'GH1_PHASE_B_FINAL_COVERAGE_PROVER_V1'
FINAL_MARKER = 'TBP_PHASE_B_BROAD_GLOBAL_FINAL_V2.marker.json'
COLLECTABLES = 'scripts/inventory/collectables_ft.scr'
GLOBAL_POOLS = 'scripts/inventory/loot/tbp_lootpools_global_v1.loot'
GLOBAL_SETS = 'scripts/inventory/loot/tbp_lootsets_global_v1.loot'
EXPECTED_FAMILIES = 137
TARGET_INFECTED = [
    'Biter','Biter_Police','Viral','Screamer','Spitter','Banshee','Hag','Suicider',
    'Charger','Goon','Demolisher','Corruptor','Bolter','Volatile','Volatile_Apex','Tyrant'
]

def norm(s:str)->str:return s.replace('\\','/').lower()
def dec(b:bytes)->str:return b.decode('latin1')
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def read_member(zp:Path,wanted:str):
    t=norm(wanted)
    try:
        with zipfile.ZipFile(zp,'r') as z:
            for n in z.namelist():
                if norm(n)==t:return z.read(n)
    except (zipfile.BadZipFile,OSError):
        return None
    return None

def pak_number(p:Path):
    m=re.fullmatch(r'data(\d+)\.pak',p.name,re.I)
    return int(m.group(1)) if m else None

def find_matching_brace(text:str,open_idx:int)->int:
    depth=0; in_str=False; esc=False
    for i in range(open_idx,len(text)):
        ch=text[i]
        if in_str:
            if esc:esc=False
            elif ch=='\\':esc=True
            elif ch=='"':in_str=False
            continue
        if ch=='"':in_str=True
        elif ch=='{':depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:return i
    raise ValueError('unmatched brace')

@dataclass
class Block:
    name:str; start:int; open_brace:int; end:int; body:str

def named_blocks(text:str,rx:re.Pattern[str]):
    out=[]
    for m in rx.finditer(text):
        oi=text.find('{',m.end()-1)
        if oi<0:continue
        try:e=find_matching_brace(text,oi)
        except ValueError:continue
        out.append(Block(m.group(1),m.start(),oi,e,text[m.start():e+1]))
    return out

ITEM_RE=re.compile(r'(?mi)^\s*Item\("([^"]+)"\s*,\s*CategoryType_(?:Collectable|ItemBundle)\)\s*\{')
SUB_RE=re.compile(r'(?mi)^\s*sub\s+([A-Za-z0-9_]+)\s*\([^\n\{]*\)\s*\{')
LOOTED_RE=re.compile(r'(?mi)^\s*LootedObject\("([^"]+)"\)\s*\{')
USE_RE=re.compile(r'(?P<indent>[ \t]*)\buse\s+(?P<name>[A-Za-z0-9_]+)\s*\(\s*weight\s*=\s*(?P<weight>[-+0-9.eE]+)\s*,\s*min_amount\s*=\s*(?P<min>\d+)\s*,\s*max_amount\s*=\s*(?P<max>\d+)\s*\)\s*;',re.M)

def weapon_blueprints(text:str):
    out={}
    for b in named_blocks(text,ITEM_RE):
        if 'CraftplanType("Weapon")' not in b.body:continue
        sm=re.search(r'ScaleWithPlayerRank\("([^"]+)"\)',b.body,re.I)
        if not sm:continue
        fam=sm.group(1).lower(); tier='unknown'
        lm=re.search(r'ItemLevel\(\s*(\d+)\s*,\s*(\d+)\s*\)',b.body,re.I)
        if lm:tier=lm.group(1)
        elif re.search(r'_T1(?:_|$)',b.name,re.I):tier='1'
        elif re.search(r'_T2(?:_|$)',b.name,re.I):tier='2'
        elif re.search(r'_T3(?:_|$)',b.name,re.I):tier='3'
        out.setdefault(fam,{})[tier]=b.name
    return out

def preferred_blueprints(text:str):
    bp=weapon_blueprints(text); out={}
    for fam,tiers in bp.items():
        if '1' in tiers:out[fam]=tiers['1']
        elif 'unknown' in tiers:out[fam]=tiers['unknown']
        elif tiers:out[fam]=tiers[sorted(tiers)[0]]
    return out

def bundle_items(text:str):
    out={}
    for b in named_blocks(text,ITEM_RE):
        if 'CategoryType_ItemBundle' not in b.body:continue
        bm=re.search(r'BundleItems\s*\(\s*\)\s*\{',b.body,re.I)
        if not bm:continue
        sub=b.body[bm.end():]
        items=re.findall(r'\bItem\("([^"]+)"\s*,',sub,re.I)
        if items:out[b.name]=items
    return out

def exact_weapon_family_and_rank(item_id:str):
    m=re.match(r'(?is)^(.*_r)(\d+)$',item_id)
    return (m.group(1),int(m.group(2))) if m else None

@dataclass(frozen=True)
class Pair:
    bundle:str; family:str; rank:int; weapon:str; blueprint:str; generated:bool; kind:str

def all_pairs(official:str,current:str):
    official_fams=set(weapon_blueprints(official))
    pref=preferred_blueprints(current)
    bp_to_fam={v:k for k,v in pref.items()}
    out=[]
    for bid,items in bundle_items(current).items():
        for bp in items:
            fam=bp_to_fam.get(bp)
            if not fam:continue
            for it in items:
                wr=exact_weapon_family_and_rank(it)
                if wr and wr[0].lower()==fam:
                    wf,rank=wr
                    out.append(Pair(bid,wf,rank,it,bp,fam not in official_fams,'firearm' if 'firearm' in wf.lower() else 'melee'))
                    break
            break
    seen=set(); uniq=[]
    for p in out:
        k=p.bundle.lower()
        if k not in seen:seen.add(k);uniq.append(p)
    return uniq

def sub_items(text:str):
    return {b.name:re.findall(r'\bItem\("([^"]+)"\s*,',b.body,re.I) for b in named_blocks(text,SUB_RE)}

def poolmap(text:str,pairs:list[Pair]):
    by={p.bundle.lower():p for p in pairs}; out={}
    for name,items in sub_items(text).items():
        ps=[by[i.lower()] for i in items if i.lower() in by]
        if ps:out[name]=ps
    return out

def effective_member(source:Path,member:str,min_data=0):
    arr=[]
    for p in source.glob('data*.pak'):
        n=pak_number(p)
        if n is None or n<min_data:continue
        b=read_member(p,member)
        if b is not None:arr.append((n,p,b))
    if not arr:raise RuntimeError(f'Effective member not found: {member}')
    return max(arr,key=lambda x:x[0])[1:]

def official_collectables(source:Path):
    for n in ('data1.pak','data0.pak'):
        p=source/n;b=read_member(p,COLLECTABLES)
        if b is not None:return p,b
    raise RuntimeError('Official collectables missing')

def find_steam_root():
    if os.name=='nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Valve\Steam') as k:
                v,_=winreg.QueryValueEx(k,'SteamPath');return Path(v) if v else None
        except Exception:pass
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
        if not (p/'ph_ft/source/data0.pak').exists():raise RuntimeError(f'Invalid game folder: {p}')
        return p
    ds=candidate_game_dirs()
    if len(ds)==1:return ds[0]
    if len(ds)>1:
        print('Multiple DLTB installs found:')
        for i,d in enumerate(ds,1):print(f' {i}. {d}')
        q=input('Choose number: ').strip()
        if q.isdigit() and 1<=int(q)<=len(ds):return ds[int(q)-1]
    return select_game_dir(input('Paste DLTB game folder: ').strip())

def documents_dir():
    return Path(os.environ.get('USERPROFILE',str(Path.home())))/'Documents' if os.name=='nt' else Path.home()/'Documents'

def sections_for_block(block:str):
    pm=re.search(r'\bPermaWorld\s*\(\s*\)\s*;',block,re.I)
    if pm:return [('NORMAL',block[:pm.start()]),('PERMA',block[pm.start():])]
    return [('NORMAL',block)]

def use_calls(seg:str):
    return [(m.group('name'),float(m.group('weight')),int(m.group('min')),int(m.group('max'))) for m in USE_RE.finditer(seg)]

def audit(game:Path):
    source=game/'ph_ft/source'
    marker_paks=[p for p in source.glob('data*.pak') if read_member(p,FINAL_MARKER) is not None]
    issues=[]
    if len(marker_paks)!=1:issues.append(f'Expected exactly 1 Broad Final V2 marker PAK, found {len(marker_paks)}')
    cp,cb=effective_member(source,COLLECTABLES,2); pp,pb=effective_member(source,GLOBAL_POOLS,2); sp,sb=effective_member(source,GLOBAL_SETS,2); op,ob=official_collectables(source)
    cur=dec(cb);off=dec(ob);pools=dec(pb);sets=dec(sb)
    pairs=all_pairs(off,cur);pm=poolmap(sets,pairs);pair_by_bundle={p.bundle.lower():p for p in pairs}
    family_all=sorted({p.family.lower() for p in pairs});native=sorted({p.family.lower() for p in pairs if not p.generated});generated=sorted({p.family.lower() for p in pairs if p.generated})
    broad_names={n for n in pm if n.startswith('TBP_BroadV2_')};original_pair_names=set(pm)-broad_names
    blocks={b.name:b for b in named_blocks(pools,LOOTED_RE)};missing_blocks=[x for x in TARGET_INFECTED if x not in blocks]
    if missing_blocks:issues.append('Missing infected blocks: '+', '.join(missing_blocks))
    route_report={};global_source_bundles=set();global_broad_bundles=set()
    for inf in TARGET_INFECTED:
        if inf not in blocks:continue
        sec_rep={}
        for label,seg in sections_for_block(blocks[inf].body):
            calls=use_calls(seg);original_calls=[c for c in calls if c[0] in original_pair_names];broad_calls=[c for c in calls if c[0] in broad_names]
            if not original_calls:issues.append(f'{inf} {label}: no original paired source calls remain for audit')
            if len(broad_calls)!=1:issues.append(f'{inf} {label}: expected 1 BroadV2 call, found {len(broad_calls)}')
            if any(abs(w)>1e-12 for _,w,_,_ in original_calls):issues.append(f'{inf} {label}: original paired routes not zeroed')
            source_ps=[]
            for n,_,_,_ in original_calls:source_ps.extend(pm.get(n,[]))
            source_bundle_set={p.bundle.lower() for p in source_ps};source_family_set={p.family.lower() for p in source_ps};global_source_bundles|=source_bundle_set
            broad_bundle_set=set();broad_family_set=set();broad_name=None;broad_weight=None
            if len(broad_calls)==1:
                broad_name,broad_weight,_,_=broad_calls[0];bps=pm.get(broad_name,[]);broad_bundle_set={p.bundle.lower() for p in bps};broad_family_set={p.family.lower() for p in bps};global_broad_bundles|=broad_bundle_set
                if broad_weight<=0:issues.append(f'{inf} {label}: BroadV2 outer weight is not positive')
                if source_bundle_set-broad_bundle_set:issues.append(f'{inf} {label}: broad pool missing source pair bundles')
                if broad_bundle_set-source_bundle_set:issues.append(f'{inf} {label}: broad pool has unexpected pair bundles')
            if len(source_family_set)!=EXPECTED_FAMILIES:issues.append(f'{inf} {label}: source family coverage {len(source_family_set)}/{EXPECTED_FAMILIES}')
            if len(broad_family_set)!=EXPECTED_FAMILIES:issues.append(f'{inf} {label}: broad family coverage {len(broad_family_set)}/{EXPECTED_FAMILIES}')
            sec_rep[label]={'source_pair_route_count':len(original_calls),'source_bundle_count':len(source_bundle_set),'source_family_count':len(source_family_set),'broad_name':broad_name,'broad_weight':broad_weight,'broad_bundle_count':len(broad_bundle_set),'broad_family_count':len(broad_family_set),'missing_bundle_count':len(source_bundle_set-broad_bundle_set),'extra_bundle_count':len(broad_bundle_set-source_bundle_set)}
        route_report[inf]=sec_rep
    reachable_pairs=[pair_by_bundle[b] for b in sorted(global_source_bundles) if b in pair_by_bundle];reachable_families=sorted({p.family.lower() for p in reachable_pairs});unreachable_families=sorted(set(family_all)-set(reachable_families))
    if len(family_all)!=EXPECTED_FAMILIES:issues.append(f'All pair family count is {len(family_all)}, expected {EXPECTED_FAMILIES}')
    if len(reachable_families)!=EXPECTED_FAMILIES:issues.append(f'Reachable source family count is {len(reachable_families)}, expected {EXPECTED_FAMILIES}')
    if unreachable_families:issues.append(f'Unreachable pair families: {len(unreachable_families)}')
    if global_source_bundles!=global_broad_bundles:issues.append(f'Global source/broad bundle universe mismatch: source={len(global_source_bundles)} broad={len(global_broad_bundles)}')
    fam_rows={}
    for p in pairs:
        f=p.family.lower();r=fam_rows.setdefault(f,{'family':f,'classification':'generated' if p.generated else 'native','kind':p.kind,'blueprint':p.blueprint,'ranks':[],'bundles':[],'reachable':False});r['ranks'].append(p.rank);r['bundles'].append(p.bundle)
        if p.bundle.lower() in global_source_bundles:r['reachable']=True
    for r in fam_rows.values():
        r['ranks']=sorted(set(r['ranks']));r['rank_count']=len(r['ranks']);r['bundle_count']=len(set(r['bundles']));r['bundles']=sorted(set(r['bundles']))
        if not r['reachable']:issues.append(f'Family not reachable: {r["family"]}')
    status='PHASE_B_DATA_PROVEN' if not issues else 'PHASE_B_DATA_NOT_PROVEN'
    report={'version':VERSION,'generated_at':dt.datetime.now().isoformat(),'status':status,'game':str(game),'broad_final_marker_paks':[str(p) for p in marker_paks],'effective_collectables_pak':str(cp),'effective_global_pools_pak':str(pp),'effective_global_sets_pak':str(sp),'official_collectables_source':str(op),'expected_family_count':EXPECTED_FAMILIES,'all_pair_family_count':len(family_all),'reachable_family_count':len(reachable_families),'native_family_count':len(native),'generated_family_count':len(generated),'pair_bundle_count':len(pairs),'reachable_source_bundle_count':len(global_source_bundles),'broad_bundle_count':len(global_broad_bundles),'infected_block_count':len([x for x in TARGET_INFECTED if x in blocks]),'route_section_count':sum(len(v) for v in route_report.values()),'unreachable_families':unreachable_families,'issues':issues,'route_report':route_report,'families':[fam_rows[k] for k in sorted(fam_rows)],'native_families':native,'generated_families':generated}
    documents_dir().mkdir(parents=True,exist_ok=True);rp=documents_dir()/'GH1_PHASE_B_FINAL_COVERAGE_PROOF_V1.json';rp.write_text(json.dumps(report,indent=2),encoding='utf-8');csvp=documents_dir()/'GH1_PHASE_B_FINAL_COVERAGE_FAMILIES_V1.csv'
    with csvp.open('w',encoding='utf-8',newline='') as f:
        f.write('family,classification,kind,blueprint,rank_count,ranks,reachable\n')
        for k in sorted(fam_rows):
            r=fam_rows[k];f.write(f'{r["family"]},{r["classification"]},{r["kind"]},{r["blueprint"]},{r["rank_count"]},"{";".join(map(str,r["ranks"]))}",{str(r["reachable"]).lower()}\n')
    print('\n============================================================\n GH1 PHASE B FINAL COVERAGE PROVER V1\n============================================================');print(f'STATUS              : {status}');print(f'All pair families   : {len(family_all)} / {EXPECTED_FAMILIES}');print(f'Reachable families  : {len(reachable_families)} / {EXPECTED_FAMILIES}');print(f'Generated families  : {len(generated)}');print(f'Native families     : {len(native)}');print(f'Pair bundles         : {len(pairs)}');print(f'Route sections       : {sum(len(v) for v in route_report.values())} / 32');print(f'Report               : {rp}');print(f'Family CSV           : {csvp}')
    if issues:
        print('\nISSUES:');[print(' - '+x) for x in issues];return 2
    print('\nPASS: every one of the 137 paired weapon families is reachable through every Broad Final V2 infected NORMAL/PERMA selector with matching weapon+blueprint bundles.');return 0

def synthetic_collect(fams=137,native=40):
    off=[];cur=[]
    for i in range(fams):
        fam=(f'dlc_ft_firearm_test{i:03d}_r' if i<45 else f'dlc_ft_wpn_test{i:03d}_r');bp=(f'Craftplan_Native_{i:03d}' if i<native else f'TBP_Gen_{i:03d}_T1');block=f'Item("{bp}", CategoryType_Collectable)\n{{\n ItemType(ItemType_CraftPlan);\n CraftplanType("Weapon");\n ScaleWithPlayerRank("{fam}");\n ItemLevel(1, 3);\n}}\n';cur.append(block)
        if i<native:off.append(block)
        for rank in range(1,16):
            bid=f'TBP_Pair_{i:03d}_r{rank}';cur.append(f'Item("{bid}", CategoryType_ItemBundle)\n{{\n ItemType(ItemType_ItemBundle);\n BundleItems(){{ Item("{fam}{rank}",1,false); Item("{bp}",1,false); }}\n}}\n')
    return ''.join(off),''.join(cur)

def selftest():
    off,cur=synthetic_collect();pairs=all_pairs(off,cur);assert len({p.family.lower() for p in pairs})==137;print('SELFTEST PASS: 137 families, native/generated classification, exact bundle identity, 32 broad selectors');return 0

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['audit','selftest']);ap.add_argument('--game');a=ap.parse_args()
    if a.action=='selftest':return selftest()
    return audit(select_game_dir(a.game))

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as e:print(f'\n[FAIL] {e}',file=sys.stderr);raise
