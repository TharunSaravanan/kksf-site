# Deploying the iOS and Android apps

Pipeline: `.github/workflows/deploy-apps.yml` (GitHub Actions). iOS goes to TestFlight, Android to the Play Console internal track. It runs on the 1st of each month and on demand. Run `python3 apps/build_app_data.py` first so the bundled data is current.

## One-time setup (needs your accounts)
1. Put this folder in a GitHub repo (private is fine) and push.
2. Apple Developer Program ($99/yr): create the app "com.adhigopal.thirukkural" in App Store Connect; create an API key (App Store Connect > Users and Access > Keys); create an Apple Distribution certificate (.p12) and an App Store provisioning profile.
3. Google Play Console ($25): create the app, enable the Play Developer API, create a service-account JSON with release permission; create an upload keystore (`keytool -genkey -v -keystore release.jks -alias upload -keyalg RSA -keysize 2048 -validity 10000`).
4. Add these repository secrets: ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_P8, APPLE_TEAM_ID, IOS_DIST_CERT_P12_BASE64, IOS_DIST_CERT_PASSWORD, IOS_PROVISIONING_PROFILE_BASE64, ANDROID_KEYSTORE_BASE64, ANDROID_KEYSTORE_PASSWORD, ANDROID_KEY_ALIAS, ANDROID_KEY_PASSWORD, PLAY_SERVICE_ACCOUNT_JSON.
5. Store listing items (screenshots, description, privacy policy URL, age rating) must be completed once in each console. The first Play upload must be done manually in the console.
