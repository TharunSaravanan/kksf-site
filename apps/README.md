# Thirukkural — iOS and Android apps

Two native apps, one for each platform:

| Folder | Platform | Language / UI | Open with |
|---|---|---|---|
| `ios/` | iPhone & iPad (iOS 16+) | Swift + SwiftUI | Xcode (Mac) |
| `android/` | Android 8.0+ (API 26) | Kotlin + Jetpack Compose | Android Studio (Mac/Windows/Linux) |

Both apps work fully offline. All 1,330 kurals, the Historical Texts page and the Learn More page are bundled inside the app as one data file, `thirukkural_data.json`, generated from the same data as the website and book. Sikhism and Real Life Example appear in the apps automatically once the research loop finishes them and they're switched on for the website.

Screens (the same as the website): Home · The Kurals (search, all 133 chapters grouped by Aram / Porul / Inbam, expand a chapter to preview its kurals) · chapter page (previous / next chapter) · kural study page (Tamil, transliteration, Meaning, Elementary, University, Through the Lens of, Real Life Example, numbered sources with tappable links, previous / next kural, Skip to Next Chapter = first kural of the next chapter) · Learn More · Historical Texts.

## Refresh the app data

After any change to the content (the research loop does this automatically):

```
cd ~/Documents/Thirukkural
python3 build_data2.py && python3 build_web.py && python3 apps/build_app_data.py
```

## Run the iOS app on your iPhone

You need a Mac with Xcode (free from the Mac App Store). Running on your own phone is free with a normal Apple ID; publishing to the App Store needs the Apple Developer Program ($99/year).

1. Install XcodeGen once: `brew install xcodegen` (Homebrew: https://brew.sh).
2. `cd ~/Documents/Thirukkural/apps/ios && xcodegen` — creates `Thirukkural.xcodeproj`.
3. `open Thirukkural.xcodeproj`.
4. In Xcode: select the Thirukkural target → Signing & Capabilities → tick "Automatically manage signing" → Team: your Apple ID.
5. Plug in your iPhone (or pick a simulator), press ▶ Run. On the phone, first launch needs Settings → General → VPN & Device Management → trust your developer certificate.

No XcodeGen? In Xcode choose File → New → Project → iOS App (name "Thirukkural", interface SwiftUI), delete the generated `ContentView.swift` and app file, then drag the contents of `ios/Thirukkural/` (the .swift files, `Assets.xcassets`, `Resources/`) into the project, ticking "Copy items if needed" and the app target.

## Run the Android app on your phone

You need Android Studio (free): https://developer.android.com/studio. Publishing to Google Play needs a Play Console account ($25 once).

1. Android Studio → Open → choose `~/Documents/Thirukkural/apps/android`. Let it finish the Gradle sync (it downloads Gradle and the Android SDK the first time; accept any SDK prompts).
2. On your phone: Settings → About phone → tap Build number 7 times, then Developer options → USB debugging on. Plug it in. (Or use an emulator from Device Manager.)
3. Press ▶ Run.

## Before publishing (later)

- App icon: the icon slots are empty placeholders; add a 1024×1024 icon (iOS `Assets.xcassets/AppIcon`) and an adaptive launcher icon (Android Studio → New → Image Asset).
- Store listings need screenshots, a description, a privacy policy URL (the apps collect no data), and age rating.
- Bundle / application id is `com.adhigopal.thirukkural` on both; change it before first upload if you want a different one.
