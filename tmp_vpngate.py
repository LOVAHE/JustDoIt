import base64, csv, io, urllib.request

req = urllib.request.Request('https://www.vpngate.net/api/iphone/', headers={'User-Agent': 'Mozilla/5.0'})
raw = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
lines = [x for x in raw.splitlines() if x and not x.startswith('*')]
rows = list(csv.DictReader(io.StringIO('\n'.join([lines[0].lstrip('#')] + lines[1:]))))
items = []
for r in rows:
    try:
        cfg = base64.b64decode(r['OpenVPN_ConfigData_Base64']).decode('utf-8', 'replace')
        if 'proto tcp' not in cfg.lower():
            continue
        items.append((int(r.get('Score') or 0), int(r.get('Speed') or 0), r, cfg))
    except Exception:
        pass
items.sort(reverse=True, key=lambda x: (x[0], x[1]))
seen_ip, seen_country = set(), set(); n = 0
with open('vpngate-nodes.txt', 'w', encoding='utf-8') as meta:
    for _, _, r, cfg in items:
        ip, country = r.get('IP'), r.get('CountryShort')
        if not ip or ip in seen_ip or not country or country in seen_country:
            continue
        seen_ip.add(ip); seen_country.add(country); n += 1
        with open(f'/tmp/vpn-{n}.ovpn', 'w', encoding='utf-8') as f:
            f.write(cfg + '\nauth-nocache\nconnect-timeout 15\nconnect-retry-max 1\nroute-nopull\n')
        meta.write(f"{n}\t{country}\t{ip}\t{r.get('Score')}\t{r.get('Speed')}\n")
        if n >= 8:
            break
print(n)
