[app]
# (str) Title of your application
title = Hunter System
# (str) Package name (no spaces, lowercase)
package.name = huntersystem
# (str) Package domain (needed for android/ios packaging)
package.domain = org.taafin
# (str) Source code where the main.py live
source.dir = .
# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json
# (str) Application versioning
version = 0.1
# (list) Application requirements
requirements = python3,kivy==2.3.1,kivymd==1.2.0,android
# (str) Presplash/orientation
orientation = portrait
fullscreen = 0
# (list) Permissions
android.permissions =
# (int) Target Android API
android.api = 34
# (int) Minimum API
android.minapi = 21
# (str) Android NDK version to use
android.ndk = 25b
# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a
# (bool) Indicate whether the screen should stay on
android.wakelock = False
# (bool) Allow backup
android.allow_backup = True

# --- Keystore untuk update tanpa uninstall ---
# Path ini diisi otomatis oleh GitHub Actions via environment variable
android.release_artifact = apk

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
# (int) Display warning if buildozer is run as root
warn_on_root = 1
