import base64, csv, io, os, urllib.request

url = 'https://www.vpngate.net/api/iphone/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
lines = [x for x in raw.splitlines() if x and not x.startswith('*')]
header = lines[0].lstrip('#')
rows = list(csv.DictReader(io.StringIO('\n'.join([header] + lines[1:]))))
preferred = {'JP': 10, 'KR': 9, 'SG': 8, 'US': 7, 'CA': 6, 'GB': 5, 'DE': 4, 'FR': 3, 'NL': 2, 'AU': 1}
items = []
for r in rows:
    try:
        cfg = base64.b64decode(r['OpenVPN_ConfigData_Base64']).decode('utf-8', 'replace')
        if 'proto tcp' not in cfg.lower():
            continue
        rank = preferred.get(r.get('CountryShort', ''), 0)
        score = int(r.get('Score') or 0)
        speed = int(r.get('Speed') or 0)
        items.append(((rank, score, speed), r, cfg))
    except Exception:
        pass
items.sort(reverse=True, key=lambda x: x[0])
seen = set()
n = 0
with open('vpngate-nodes.txt', 'w', encoding='utf-8') as meta:
    for _, r, cfg in items:
        ip = r.get('IP')
        if not ip or ip in seen:
            continue
        seen.add(ip); n += 1
        path = f'/tmp/vpn-{n}.ovpn'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cfg + '\nauth-nocache\nconnect-timeout 15\nconnect-retry-max 1\n')
        meta.write(f"{n}\t{r.get('CountryShort')}\t{ip}\t{r.get('Score')}\t{r.get('Speed')}\n")
        if n >= 6:
            break
print(n)
