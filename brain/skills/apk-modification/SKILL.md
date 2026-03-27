---
name: Android APK Modification
tier: 2
description: Skills for decompiling, modifying, and rebuilding Android APK files
---

# Android APK Modification Skill

## Purpose
Decompile, modify, and rebuild Android APK files to customize functionality, UI, or data sources.

## Core Tools

### Required Tools
```powershell
# apktool - decompile/rebuild APKs
java -jar apktool.jar d app.apk -o app_decompiled

# uber-apk-signer - sign APKs
java -jar uber-apk-signer.jar --apks app.apk
```

## Key File Types

### 1. AndroidManifest.xml
**Location**: `AndroidManifest.xml`

**Common modifications:**
```xml
<!-- Change package name -->
<manifest package="com.newapp.name">

<!-- Change app name -->
<application android:label="@string/app_name">

<!-- Remove permissions -->
<!-- <uses-permission android:name="android.permission.CAMERA"/> -->

<!-- Add/remove activities -->
<activity android:name=".NewActivity" android:exported="true"/>
```

### 2. Resources (res/)

**Strings** (`res/values/strings.xml`):
```xml
<string name="app_name">New App Name</string>
```

**Colors** (`res/values/colors.xml`):
```xml
<color name="primary">#FF5722</color>
```

**Layouts** (`res/layout/*.xml`):
- Modify UI structures
- Change visibility
- Add/remove elements

### 3. Smali Code (smali/)

**What is Smali?**
- Dalvik bytecode (Android's assembly language)
- Result of decompiling Java/Kotlin code
- Human-readable but complex

**Basic structure:**
```smali
.class public Lcom/example/MyClass;
.super Ljava/lang/Object;

.method public myMethod()V
    .registers 2
    const-string v0, "Hello"
    return-void
.end method
```

**Common operations:**
```smali
# String assignment
const-string v0, "my text"

# Method call
invoke-virtual {v0}, Landroid/util/Log;->d(Ljava/lang/String;)I

# If statement
if-eqz v0, :label_name

# Return
return-void
```

## Typical Modifications

### 1. Change Data Source

**Find**: Network/API calls
```smali
const-string v0, "https://old-api.com/data"
```

**Replace**:
```smali
const-string v0, "https://new-api.com/data"
```

### 2. Remove Features

**Option A**: Comment out in Smali
```smali
# .method public showAds()V
#     ...
# .end method
```

**Option B**: Remove from manifest
```xml
<!-- <activity android:name=".AdsActivity"/> -->
```

### 3. Modify UI

**Hide elements** in layout XML:
```xml
<Button
    android:id="@+id/loginButton"
    android:visibility="gone"/>
```

**Or in Smali** (set visibility programmatically):
```smali
# Find setVisibility call
const/16 v1, 0x8  # View.GONE = 8
invoke-virtual {v0, v1}, Landroid/view/View;->setVisibility(I)V
```

## Build & Sign Process

### 1. Rebuild APK
```powershell
java -jar apktool.jar b app_decompiled -o app_rebuilt.apk
```

**Common errors:**
- Missing resources → Check res/ folder
- Invalid XML → Validate syntax
- Smali syntax errors → Review edits

### 2. Sign APK
```powershell
java -jar uber-apk-signer.jar --apks app_rebuilt.apk
```

**Output**: `app_rebuilt-aligned-debugSigned.apk`

### 3. Install & Test
```powershell
adb install app_rebuilt-aligned-debugSigned.apk
```

## Finding What to Modify

### Search for strings:
```powershell
# Windows
findstr /s /i "login" .\smali\**\*.smali

# See what references it
grep -r "Lcom/example/LoginActivity" smali/
```

### Find resource IDs:
Look in `res/values/public.xml`:
```xml
<public type="id" name="loginButton" id="0x7f0a0123"/>
```

Then search for `0x7f0a0123` in Smali files.

## Android TV Specific

### Leanback Support
```xml
<uses-feature android:name="android.software.leanback" android:required="true"/>
```

### Launcher Intent
```xml
<intent-filter>
    <action android:name="android.intent.action.MAIN"/>
    <category android:name="android.intent.category.LEANBACK_LAUNCHER"/>
</intent-filter>
```

### Banner Icon
```xml
<application android:banner="@mipmap/ic_banner">
```

## Debugging Modified APKs

### Logcat
```powershell
adb logcat | findstr "MyApp"
```

### Check for crashes
```powershell
adb logcat *:E  # Errors only
```

## Best Practices

1. **Backup original APK** before modifying
2. **Test after each change** - incremental approach
3. **Document changes** you make
4. **Use version control** for decompiled files
5. **Respect app licenses** - only modify for personal/educational use

## Quick Workflow

```powershell
# 1. Decompile
apktool d original.apk

# 2. Make changes
# Edit files in original/

# 3. Rebuild
apktool b original -o modified.apk

# 4. Sign
uber-apk-signer --apks modified.apk

# 5. Install
adb install modified-aligned-debugSigned.apk
```

---

**Use this skill when**: Modifying existing Android apps, customizing APKs, removing unwanted features
