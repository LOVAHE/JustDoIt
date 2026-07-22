# Archive.org YouTube 21.21.03 IPA audit summary

- Audited URL: `https://archive.org/download/com.google.ios.youtube-21.21.03-Decrypted/com.google.ios.youtube-21.21.03-Decrypted.ipa`
- Download succeeded and the file is a valid ZIP/IPA with no corrupt entry.
- File size: `133577361` bytes (`127.39 MiB`).
- SHA-256: `d5d7464677646beb66a37410f56570b169cb8f081c194062124fa4c65af65cfa`.
- MD5: `8d2d78fae5014f24da4075b08f0dfbda`.
- Archive contains `7722` entries and expands to about `300.75 MiB`.

## Archive item

- Identifier/title: `com.google.ios.youtube-21.21.03-Decrypted`.
- Uploader shown by Archive.org metadata: `gaiters-fatale-0l@icloud.com`.
- Public/added date: `2026-05-28 22:07:36`.
- The Archive.org metadata response did not expose an MD5/SHA1 entry matched by the audit script, so there is no independent Archive hash comparison in this report.

## App identity and structure

- Exactly one main `.app` exists in `Payload`.
- Main bundle ID: `com.google.ios.youtube`.
- Display name: `YouTube`.
- Version/build: `21.21.3`.
- Minimum iOS: `16.0`.
- Main executable: `YouTube`, ARM64, decrypted (`crypt_id=0`).
- Expected Google YouTube extensions are present: notification content/service, WidgetKit, share, intents, and app migration.
- The only embedded framework bundle found is Google's `widevine_cdm_secured_ios.framework`.

## Static warning-sign scan

- Eight Mach-O executables were found: the main YouTube executable, six expected app extensions, and Google's Widevine framework.
- No extra injected tweak/malware dylib load command was found.
- No archive path matched common injection markers such as Frida, Cydia/Substrate, Substitute, ElleKit, libhooker, uYou, YTLite/YTPlus, YouMod, YTUHD, SponsorBlock, Patreon, jailbreak, or sideload.
- No such marker string was found in the main executable by the limited strings scan.
- No non-Google/Apple URL host was found in the main executable by the limited strings scan.

## Assessment

The static audit found no obvious sign that this IPA is a pre-tweaked or plainly injected build. Its identity, extensions, linked libraries, and file layout look consistent with a decrypted stock YouTube 21.21.3 package. This lowers risk compared with a random pre-modded IPA, but it does not prove the main executable is byte-for-byte untouched: the uploader is an unknown third party, the App Store trust chain is lost after decryption/repackaging, and a subtle patch inside the large main executable can evade this type of scan. Preliminary source-risk assessment: moderate, not verified-safe.
