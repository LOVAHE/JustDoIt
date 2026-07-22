#!/usr/bin/env python3
import hashlib, json, os, plistlib, re, shutil, subprocess, sys, zipfile
from pathlib import Path

IPA=Path(sys.argv[1]); META=Path(sys.argv[2]); OUT=Path(sys.argv[3]); EX=OUT.parent/'extracted'
SUSP=re.compile(r'frida|cydia|substrate|substitute|ellekit|libhooker|dobby|fishhook|uyou|ytlite|ytplus|youmod|ytuhd|sponsorblock|patreon|jailbreak|sideload',re.I)
MACHO={b'\xfe\xed\xfa\xce',b'\xce\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xcf\xfa\xed\xfe',b'\xca\xfe\xba\xbe',b'\xbe\xba\xfe\xca',b'\xca\xfe\xba\xbf',b'\xbf\xba\xfe\xca'}

def h(path,alg):
    x=hashlib.new(alg)
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): x.update(b)
    return x.hexdigest()
def esc(v): return str(v).replace('|','\\|').replace('\n',' ')
def is_macho(p):
    try:
        with open(p,'rb') as f:return f.read(4) in MACHO
    except:return False
def plist(path):
    try:
        with open(path,'rb') as f:return plistlib.load(f)
    except:return {}
def strings_hits(path):
    try:
        r=subprocess.run(['strings','-a','-n','6',str(path)],capture_output=True,text=True,timeout=90,errors='replace')
        hits=[]; domains=set()
        for s in r.stdout.splitlines():
            if SUSP.search(s) and len(hits)<80: hits.append(s[:300])
            for m in re.finditer(r'https?://([^/\s"\'<>]+)',s):
                host=m.group(1).lower().split(':')[0]
                if not (host.endswith('google.com') or host.endswith('googleapis.com') or host.endswith('gstatic.com') or host.endswith('youtube.com') or host.endswith('ytimg.com') or host.endswith('apple.com')):
                    domains.add(host)
        return hits,sorted(domains)[:100]
    except Exception as e:return [f'strings failed: {e}'],[]
def macho_info(path):
    out=[]
    try:
        import lief
        fat=lief.MachO.parse(str(path))
        if fat is None:return out
        bins=list(fat) if hasattr(fat,'__iter__') else [fat]
        for b in bins:
            libs=[]
            try: libs=[x.name for x in b.libraries]
            except: pass
            enc='unknown'
            try:
                ei=b.encryption_info
                enc=f'crypt_id={ei.crypt_id}' if ei else 'none'
            except: pass
            out.append({'arch':str(getattr(getattr(b,'header',None),'cpu_type','?')),'encryption':enc,'libraries':libs})
    except Exception as e: out.append({'error':str(e),'libraries':[]})
    return out

OUT.parent.mkdir(parents=True,exist_ok=True)
if EX.exists(): shutil.rmtree(EX)
EX.mkdir()
meta=json.loads(META.read_text(errors='replace')) if META.exists() else {}
size=IPA.stat().st_size; sha=h(IPA,'sha256'); md5=h(IPA,'md5')
rows=[]; zip_error='none'; total_u=0
with zipfile.ZipFile(IPA) as z:
    bad=z.testzip(); zip_error=bad or 'none'
    for i in z.infolist():
        total_u+=i.file_size; rows.append((i.filename,i.file_size,i.compress_size,i.CRC))
    z.extractall(EX)
apps=list(EX.glob('Payload/*.app')); app=apps[0] if len(apps)==1 else None
info=plist(app/'Info.plist') if app else {}
main=app/info.get('CFBundleExecutable','') if app else None
bundles=[]
if app:
    for p in [app]+list(app.rglob('*.appex'))+list(app.rglob('*.framework')):
        q=plist(p/'Info.plist')
        if q: bundles.append((str(p.relative_to(EX)),q.get('CFBundleIdentifier'),q.get('CFBundleShortVersionString'),q.get('CFBundleVersion'),q.get('CFBundleExecutable')))
machos=[p for p in EX.rglob('*') if p.is_file() and is_macho(p)]
mi={str(p.relative_to(EX)):macho_info(p) for p in machos}
injected=[]
for rel,arr in mi.items():
    for sl in arr:
        for lib in sl.get('libraries',[]):
            if SUSP.search(lib) or ('@executable_path/Frameworks/' in lib and lib.lower().endswith('.dylib')): injected.append((rel,lib))
main_hits=[]; third=[]
if main and (app/main).exists(): main_hits,third=strings_hits(app/main)
extra_names=[]
for p in EX.rglob('*'):
    if p.is_file() and SUSP.search(str(p.relative_to(EX))): extra_names.append(str(p.relative_to(EX)))
archive_file=next((x for x in meta.get('files',[]) if x.get('name')==IPA.name),{})
flags=[]
if len(apps)!=1: flags.append(f'Payload contains {len(apps)} .app bundles')
if info.get('CFBundleIdentifier')!='com.google.ios.youtube': flags.append('main bundle id is not com.google.ios.youtube')
if injected: flags.append('suspicious/injected dylib load commands detected')
if extra_names: flags.append('tweak/sideload marker names found in archive paths')
if main_hits: flags.append('tweak/sideload marker strings found in main executable')
if archive_file.get('md5') and archive_file['md5']!=md5: flags.append('downloaded MD5 differs from Archive.org metadata')
if archive_file.get('sha1') and archive_file['sha1']!=h(IPA,'sha1'): flags.append('downloaded SHA1 differs from Archive.org metadata')
score='LOW-MODERATE'
if injected or extra_names or main_hits: score='HIGH'
elif info.get('CFBundleIdentifier')=='com.google.ios.youtube' and len(apps)==1: score='MODERATE'

L=[]
L+=['# Static audit: YouTube 21.21.03 decrypted IPA','',f'- File: `{IPA.name}`',f'- Size: `{size}` bytes ({size/1024/1024:.2f} MiB)',f'- SHA-256: `{sha}`',f'- MD5: `{md5}`',f'- ZIP integrity: `{zip_error}`',f'- ZIP entries: `{len(rows)}`; uncompressed: `{total_u/1024/1024:.2f} MiB',f'- Preliminary source-risk rating: **{score}**','']
L+=['## Archive.org item metadata','',f'- Identifier: `{meta.get("metadata",{}).get("identifier")}`',f'- Title: `{esc(meta.get("metadata",{}).get("title"))}`',f'- Uploader: `{esc(meta.get("metadata",{}).get("uploader"))}`',f'- Public date: `{esc(meta.get("metadata",{}).get("publicdate"))}`',f'- Item added: `{esc(meta.get("metadata",{}).get("addeddate"))}`',f'- Metadata IPA size: `{archive_file.get("size")}`',f'- Metadata MD5: `{archive_file.get("md5")}`',f'- Metadata SHA1: `{archive_file.get("sha1")}`','']
L+=['## Main application metadata','',f'- App bundles in Payload: `{len(apps)}`',f'- Bundle ID: `{info.get("CFBundleIdentifier")}`',f'- Name: `{info.get("CFBundleDisplayName") or info.get("CFBundleName")}`',f'- Version: `{info.get("CFBundleShortVersionString")}` (`{info.get("CFBundleVersion")}`)',f'- Executable: `{info.get("CFBundleExecutable")}`',f'- Minimum iOS: `{info.get("MinimumOSVersion")}`',f'- Background modes: `{info.get("UIBackgroundModes")}`',f'- Has `_CodeSignature`: `{bool(app and (app/"_CodeSignature").exists())}`',f'- Has embedded provisioning profile: `{bool(app and (app/"embedded.mobileprovision").exists())}`','']
L+=['## Embedded bundles','','| Path | Bundle ID | Short version | Build | Executable |','|---|---|---:|---:|---|']
for r in bundles:L.append('| '+' | '.join(esc(x) for x in r)+' |')
L+=['','## Mach-O binaries and linked libraries','']
for rel,arr in mi.items():
    L.append(f'### `{rel}`')
    for sl in arr:
        L.append(f'- Arch: `{esc(sl.get("arch"))}`; encryption: `{esc(sl.get("encryption"))}`')
        for lib in sl.get('libraries',[]):L.append(f'  - `{lib}`')
L+=['','## Indicators requiring attention','']
L+=([f'- {x}' for x in flags] or ['- No obvious injected-tweak indicator was found by these checks.'])
if injected:
    L+=['','### Suspicious load commands']+[f'- `{a}` -> `{b}`' for a,b in injected]
if extra_names:
    L+=['','### Suspicious archive paths']+[f'- `{x}`' for x in extra_names[:100]]
if main_hits:
    L+=['','### Marker strings in main executable']+[f'- `{esc(x)}`' for x in main_hits]
L+=['','## Non-Google/Apple URL hosts found in the main executable']
L+=([f'- `{x}`' for x in third] or ['- None found by the limited strings scan.'])
L+=['','## Largest archive entries','','| Path | Uncompressed MiB | Compressed MiB | CRC32 |','|---|---:|---:|---:|']
for n,u,c,crc in sorted(rows,key=lambda x:x[1],reverse=True)[:80]:L.append(f'| `{n}` | {u/1048576:.2f} | {c/1048576:.2f} | `{crc:08x}` |')
L+=['','## Interpretation','','This is a static triage, not a proof of safety. Matching Archive.org hashes only proves the downloaded bytes match that Archive.org item; it does not prove the uploader supplied an untouched App Store binary. A decrypted IPA also cannot retain Apple App Store authenticity guarantees after repackaging. The strongest warning signs are unknown injected dylibs, tweak markers, unexpected bundle identifiers, or nonstandard executables. Absence of those signs lowers risk but does not rule out malicious changes inside the main executable.']
OUT.write_text('\n'.join(L),encoding='utf-8')
print(OUT)
