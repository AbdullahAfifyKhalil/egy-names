# Update instructions

How to ship a new cut of the ten libraries. Egy-Names is an Afify open-source project. Product page: [afify.co/egy-names](https://afify.co/egy-names).

The eight engines share one book and one version (`0.3.6` today). The two Faker companions have their own line (`0.1.2` today). Do not publish a Faker as `0.3.x`.

A version number can be published **once**. PyPI, npm, NuGet, pub.dev, and Maven Central reject a rebuild of the same version. If a cut is wrong, bump again.

Do not move an existing git tag. If `vX.Y.Z` already points at the wrong commit, ship `X.Y.Z+1`.

Pin [afify.co/egy-names](https://afify.co/egy-names) to what is **actually live**. Do not print a version that is still publishing.

---

## The ten

| # | Library | Registry | Live check |
|---|---|---|---|
| 1 | Python `egy-names` | [PyPI](https://pypi.org/project/egy-names/) | `https://pypi.org/pypi/egy-names/json` |
| 2 | TypeScript `egy-names` | [npm](https://www.npmjs.com/package/egy-names) | `https://registry.npmjs.org/egy-names/latest` |
| 3 | PHP `afify/egy-names` | [Packagist](https://packagist.org/packages/afify/egy-names) | `https://repo.packagist.org/p2/afify/egy-names.json` |
| 4 | Dart `egy_names` | [pub.dev](https://pub.dev/packages/egy_names) | `https://pub.dev/api/packages/egy_names` |
| 5 | C# `egy-names` | [NuGet](https://www.nuget.org/packages/egy-names/) | `https://api.nuget.org/v3-flatcontainer/egy-names/index.json` |
| 6 | Java `egy-names` | [Maven Central](https://central.sonatype.com/artifact/io.github.abdullahafifykhalil/egy-names) and [JitPack](https://jitpack.io/#AbdullahAfifyKhalil/egy-names) | repo1 metadata + JitPack tag |
| 7 | Swift `EgyNames` | Swift PM on the monorepo tag | `git ls-remote origin refs/tags/vX.Y.Z` |
| 8 | C++ `egy_names` | CMake `GIT_TAG` on the same tag | same |
| 9 | Faker Python `faker-egy-names` | [PyPI](https://pypi.org/project/faker-egy-names/) | `https://pypi.org/pypi/faker-egy-names/json` |
| 10 | Faker PHP `afify/faker-egy-names` | [Packagist](https://packagist.org/packages/afify/faker-egy-names) | `https://repo.packagist.org/p2/afify/faker-egy-names.json` |

Java has two doors. Maven Central is `io.github.abdullahafifykhalil:egy-names:X.Y.Z`. JitPack is `com.github.AbdullahAfifyKhalil:egy-names:vX.Y.Z`. Both must resolve after a release.

---

## Before you bump

GitHub secrets on [AbdullahAfifyKhalil/egy-names](https://github.com/AbdullahAfifyKhalil/egy-names):

| Secret | Used by |
|---|---|
| `PYPI_API_TOKEN` | `publish-python.yml`, `publish-faker-python.yml` |
| `NPM_TOKEN` | `publish-npm.yml` |
| `NUGET_API_KEY` | `publish-nuget.yml` |

pub.dev uses GitHub OIDC. No long-lived secret. The publisher on pub.dev must allow **tag** `refType` with pattern `v{{version}}`. A push to `main` or a manual workflow click will test, then fail publish.

Packagist username is **`Afify`**. Add a GitHub → Packagist webhook on both PHP satellite repos, or ping the update API after each tag.

Maven Central needs a Sonatype account for namespace `io.github.abdullahafifykhalil`, plus the GPG key that signed `0.3.2` / `0.3.6`.

Do not paste tokens into chat, the repo, or commit messages.

---

## Engine release (the eight)

Do this as **one commit** on `main`. `tag-release.yml` creates `vX.Y.Z` when `python/pyproject.toml` changes. If you bump Python first and push, the tag will freeze a tree where Java or Dart is still the old number. That is how `v0.3.6` first pointed at the wrong commit.

### 1. Bump every engine version file

| File | Field |
|---|---|
| `python/pyproject.toml` | `version` |
| `typescript/package.json` | `version` |
| `php/egy-names/VERSION` | the whole file |
| `dart/egy_names/pubspec.yaml` | `version:` |
| `dart/egy_names/CHANGELOG.md` | new `## X.Y.Z` section (pub.dev requires it) |
| `java/egy-names/pom.xml` | `<version>` |
| `csharp/EgyNames/EgyNames.csproj` | `<Version>` |
| `swift/EgyNames/VERSION` | the whole file |
| `cpp/egy_names/CMakeLists.txt` | `project(... VERSION X.Y.Z)` |

Also bump the install pins in each language README and in the root `README.md` / `DOCUMENTATION.md`. Each SDK ships **its own** README, not the root page.

Faker Python `egy-names>=A.B.C,<A+1` in `faker-egy-names/pyproject.toml` — only if this engine cut is a new minor the companion must require. That does not mean you publish a new Faker version. Bump Faker only when the wrapper itself changes (see below).

### 2. Push `main`

CI that should fire:

- `publish-python.yml` — PyPI `egy-names`
- `publish-npm.yml` — npm `egy-names`
- `publish-nuget.yml` — NuGet `egy-names`
- `tag-release.yml` — git tag `vX.Y.Z` + GitHub Release
- `publish-pubdev.yml` — tests on `main`; **publish only if the tag job also ran** (pub.dev rejects branch OIDC)

If a publish job fails on a missing secret, do not republish that version later from CI after someone else already uploaded it. Check the live registry first.

### 3. Confirm the tag

```bash
git ls-remote origin refs/tags/vX.Y.Z
git rev-parse vX.Y.Z^{}
```

The tag must be the commit that has **all eight** versions at `X.Y.Z`. Swift PM (`from: "X.Y.Z"`) and CMake `GIT_TAG vX.Y.Z` resolve this tag. There is no extra upload.

---

## Per library

### 1. Python — PyPI `egy-names`

**Bump:** `python/pyproject.toml`

**CI:** `.github/workflows/publish-python.yml` on push to `python/**` or `data/**`.

**If CI has no `PYPI_API_TOKEN`:**

```bash
cd python
python -m pip install --upgrade build twine
python -m build
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-... twine upload dist/*
```

Use a project-scoped token. Revoke it after.

**Live:** `https://pypi.org/project/egy-names/X.Y.Z/`

Never upload the same version twice.

### 2. TypeScript — npm `egy-names`

**Bump:** `typescript/package.json`

**CI:** `.github/workflows/publish-npm.yml`. Needs `NPM_TOKEN`.

**If CI has no token:**

```bash
cd typescript
npm ci
npm publish --access public
```

**Live:** `https://www.npmjs.com/package/egy-names` → version `X.Y.Z`

### 3. PHP — Packagist `afify/egy-names`

Packagist cannot serve a monorepo subdirectory. The live package is the satellite [egy-names-php](https://github.com/AbdullahAfifyKhalil/egy-names-php).

**Bump in the monorepo:** `php/egy-names/VERSION` and that folder’s README.

**Publish:**

```bash
SRC="php/egy-names"
DEST="$(mktemp -d)/egy-names-php"
git clone https://github.com/AbdullahAfifyKhalil/egy-names-php.git "$DEST"
rsync -a --delete --exclude vendor --exclude .phpunit.result.cache --exclude composer.lock --exclude .git "$SRC/" "$DEST/"
cd "$DEST"
git add -A
git commit -m "Release afify/egy-names X.Y.Z."
git tag vX.Y.Z
git push origin HEAD
git push origin vX.Y.Z
gh release create vX.Y.Z --title vX.Y.Z --generate-notes
```

Then update Packagist (webhook, the Update button, or):

```bash
curl -sS -X POST \
  "https://packagist.org/api/update-package?username=Afify&apiToken=TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"repository":{"url":"https://packagist.org/packages/afify/egy-names"}}'
```

**Live:** Composer `p2` JSON `version` is `vX.Y.Z`. The HTML page can lag.

Add a Packagist webhook on the satellite so the next tag does not stall.

### 4. Dart — pub.dev `egy_names`

**Bump:** `dart/egy_names/pubspec.yaml` and `CHANGELOG.md`.

**CI:** `.github/workflows/publish-pubdev.yml` on `main` **and** tags `v*`.

pub.dev will only accept the publish from a **git tag** named `vX.Y.Z` that matches `pubspec.yaml`. `workflow_dispatch` is not allowed for this package.

**Order:** aligned commit on `main` → tag `vX.Y.Z` on that commit → the tag workflow publishes.

**Live:** `https://pub.dev/packages/egy_names` latest is `X.Y.Z`

If the version URL is 200 but latest still shows the old number, wait. Search is slower than the version endpoint.

### 5. C# — NuGet `egy-names`

**Bump:** `csharp/EgyNames/EgyNames.csproj` `<Version>`

**CI:** `.github/workflows/publish-nuget.yml`. Needs `NUGET_API_KEY`.

**If CI has no key:**

```bash
cd csharp/EgyNames
dotnet pack --configuration Release -o out
```

Upload `out/egy-names.X.Y.Z.nupkg` at [nuget.org/packages/manage/upload](https://www.nuget.org/packages/manage/upload), or:

```bash
dotnet nuget push out/egy-names.X.Y.Z.nupkg \
  --api-key KEY --source https://api.nuget.org/v3/index.json --skip-duplicate
```

**Live:** `https://api.nuget.org/v3-flatcontainer/egy-names/X.Y.Z/egy-names.nuspec` returns 200.

### 6. Java — Maven Central and JitPack

**Bump:** `java/egy-names/pom.xml` `<version>`

#### Maven Central

Central is not a git tag. You upload a **signed repository zip**, not the `.jar`.

Uploading the jar fails with `META-INF` / `com/afify/egynames` and “no .pom”. A flat zip (`./egy-names-…`) fails with `File path './' is not valid` and `Missing signature`.

```bash
cd java/egy-names
mvn -DskipTests package
```

That writes:

- `target/egy-names-X.Y.Z.jar`
- `target/egy-names-X.Y.Z-sources.jar`
- `target/egy-names-X.Y.Z-javadoc.jar`

Copy `pom.xml` to `target/egy-names-X.Y.Z.pom`. Put all four under:

```
io/github/abdullahafifykhalil/egy-names/X.Y.Z/
```

Sign each of the four with the same GPG key used for `0.3.2` (fingerprint on those `.asc` files). Add `.md5` / `.sha1` / `.sha256` / `.sha512` next to them.

```bash
cd target/central-bundle-X.Y.Z
zip -X -r ../bundle-X.Y.Z.zip io
```

Upload `bundle-X.Y.Z.zip` at [central.sonatype.com/publishing](https://central.sonatype.com/publishing). Wait for validation. Click **Publish** once. Do not publish the same deployment twice.

**Live** only when repo1 has it:

```
https://repo1.maven.org/maven2/io/github/abdullahafifykhalil/egy-names/X.Y.Z/egy-names-X.Y.Z.pom
```

Search can stay empty for a while after repo1 is 200. The publishing phase is not live yet.

#### JitPack

JitPack builds the **monorepo tag** `vX.Y.Z`. It caches by tag name. If the first build fails, it keeps that failure even after you fix `main`.

`jitpack.yml` runs Maven in `java/egy-names` and skips javadoc. JitPack’s Maven is old; javadoc plugin 3.8.0 will fail if that skip is missing.

After the tag exists: open [jitpack.io/#AbdullahAfifyKhalil/egy-names](https://jitpack.io/#AbdullahAfifyKhalil/egy-names) and **Rebuild** `vX.Y.Z` if status is Error.

**Live:** API `status` is `ok` and `commit` is the current tag commit.

```
https://jitpack.io/api/builds/com.github.AbdullahAfifyKhalil/egy-names/vX.Y.Z
```

### 7. Swift — Swift PM

**Bump:** `swift/EgyNames/VERSION`

Consumers use the root `Package.swift` and:

```swift
.package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "X.Y.Z")
```

No registry upload. The monorepo tag is the publish. Confirm the tag commit includes the Swift tree at `X.Y.Z`.

### 8. C++ — CMake FetchContent

**Bump:** `cpp/egy_names/CMakeLists.txt` `VERSION`

Consumers pin `GIT_TAG vX.Y.Z`. Same tag as Swift. No extra upload.

---

## Faker companions (not 0.3.x)

Bump these when the **wrapper** changes, or when they must require a new egy-names minor. Keep `0.1.x` (or the next companion number). Never retag them as the engine version.

### 9. Faker Python — PyPI `faker-egy-names`

**Bump:** `faker-egy-names/pyproject.toml` `version` and the `egy-names>=…` pin.

**CI:** `.github/workflows/publish-faker-python.yml`

**If CI has no token:** same `build` + `twine upload` as Python, from `faker-egy-names/`.

**Live:** `https://pypi.org/project/faker-egy-names/`

### 10. Faker PHP — Packagist `afify/faker-egy-names`

**Bump in the monorepo:** `faker-egy-names-php/VERSION`

Satellite: [faker-egy-names-php](https://github.com/AbdullahAfifyKhalil/faker-egy-names-php). Same rsync / tag / Packagist ping as the PHP engine, with tag `v0.1.x` and package URL `https://packagist.org/packages/afify/faker-egy-names`.

---

## After the registries are live

1. Confirm all ten with the live-check URLs in the table. Maven Central = repo1 200, not “publishing”. JitPack = `ok`, not a cached Error.
2. Pin [afify.co/egy-names](https://afify.co/egy-names) to those live versions. Website repo: `/Volumes/MAC/Development/Afify.corp/Afify Website`. Files: `src/components/egy/LabWorkbench.jsx`, `LabShelf.jsx`, `LibraryShelf.jsx`, `src/i18n/copy.js` (English and Arabic). Rule in that repo’s `IMPLEMENTATION.md`: do not print a version that is not published.
3. From `/Volumes/MAC/Development/Afify.corp/Afify Website`: `npm run build && firebase deploy --only hosting`
4. Leave Faker pins at the companion version, not the engine version.

---

## If something is already on the registry

| Registry | Same version again? |
|---|---|
| PyPI / npm / NuGet / pub.dev / Maven Central | No. Bump. |
| Packagist | New git tag on the satellite, then Update. |
| Swift / C++ | New monorepo tag. Do not move the old one. |
| JitPack | Rebuild the existing tag, or a new tag. |

---

## License

Copyright (c) 2026 Afify by Abdullah Afify.
