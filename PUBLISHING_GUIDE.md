# `egy-names` — Multi-Registry Publishing Guide

This guide outlines the exact, step-by-step instructions to publish **`egy-names`** to all 5 official package registries:
1. **PyPI** (Python)
2. **npm** (TypeScript / JavaScript)
3. **pub.dev** (Dart / Flutter)
4. **NuGet** (C# / .NET)
5. **Maven Central** (Java / Kotlin)

---

## 1. Python → PyPI (`pip install egy-names`)

### Prerequisites
1. Create an account on [pypi.org](https://pypi.org/account/register/).
2. Go to **Account settings** → **API tokens** → **Add API token** (Scope: Entire account or Project).
3. Copy the token starting with `pypi-...`.

### Build & Upload Commands
Run in your terminal:

```bash
cd "/Volumes/MAC/Development/Personal/Egyptian Names/library building/python"

# 1. Install build and twine tools
python3 -m pip install --upgrade build twine

# 2. Build the source distribution (.tar.gz) and wheel (.whl)
python3 -m build

# 3. Upload to PyPI
python3 -m twine upload dist/*
```

*When prompted for username and password:*
- **Username**: `__token__`
- **Password**: `pypi-your-token-here`

---

## 2. TypeScript / JavaScript → npm (`npm install egy-names`)

### Prerequisites
1. Create an account on [npmjs.com](https://www.npmjs.com/signup).
2. Verify your email address on npm (mandatory before publishing).

### Build & Upload Commands
Run in your terminal:

```bash
cd "/Volumes/MAC/Development/Personal/Egyptian Names/library building/typescript"

# 1. Log in to your npm account (interactive login in terminal)
npm login

# 2. Build the TypeScript bundle and copy data assets
npm run build

# 3. Publish to npm registry (public access)
npm publish --access public
```

---

## 3. Dart & Flutter → Pub.dev (`dart pub add egy_names`)

### Prerequisites
1. A Google account to authenticate with [pub.dev](https://pub.dev).

### Verification & Upload Commands
Run in your terminal:

```bash
cd "/Volumes/MAC/Development/Personal/Egyptian Names/library building/dart/egy_names"

# 1. Run automated dry run to verify package compliance
dart pub publish --dry-run

# 2. Publish to pub.dev
dart pub publish
```

*The terminal will output an authentication link: open it in your browser, log in with your Google account, and grant publishing permission.*

---

## 4. C# / .NET → NuGet (`dotnet add package egy-names`)

### Prerequisites
1. Create an account on [nuget.org](https://www.nuget.org).
2. Go to your account name (top right) → **API Keys** → **Create**.
3. Set key name (e.g., `egy-names-publish`), select package scope `*` or `egy-names`, and copy the generated API key.

### Build & Upload Commands
Run in your terminal:

```bash
cd "/Volumes/MAC/Development/Personal/Egyptian Names/library building/csharp/EgyNames"

# 1. Pack the release package (.nupkg)
dotnet pack -c Release -o ./nupkg

# 2. Push to NuGet Gallery
dotnet nuget push ./nupkg/*.nupkg --api-key YOUR_NUGET_API_KEY --source https://api.nuget.org/v3/index.json
```

---

## 5. Java & Kotlin → Maven Central (`com.afify:egy-names`)

### Prerequisites
1. Create an account on the new [Maven Central Portal](https://central.sonatype.com).
2. Register your namespace / Group ID (`com.afify` or `io.github.afify`).
3. Generate a GPG key for signing artifacts (`gpg --gen-key`) and publish the public key to a keyserver (`gpg --keyserver keyserver.ubuntu.com --send-keys YOUR_KEY_ID`).
4. Generate a User Token in the Central Portal account settings.

### Build & Publish Commands
Add your GPG & Sonatype credentials to `~/.m2/settings.xml`, then run:

```bash
cd "/Volumes/MAC/Development/Personal/Egyptian Names/library building/java/egy-names"

# 1. Build, sign, and stage deployment
mvn clean deploy -P release
```

*Alternatively, you can package a bundle ZIP (`target/egy-names-0.1.0-bundle.zip`) using the Central Publishing Plugin and upload it directly in the [central.sonatype.com](https://central.sonatype.com) web dashboard.*

---

## Quick Verification Matrix

After publishing, verify installations across environments:

```bash
# Python
pip install egy-names

# Node / TS
npm install egy-names

# Dart / Flutter
dart pub add egy_names

# .NET / C#
dotnet add package egy-names

# Maven
mvn dependency:get -Dartifact=com.afify:egy-names:0.1.0
```
