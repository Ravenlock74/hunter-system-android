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
# kivymd from pypi is enough for the widgets used in this app
# "android" recipe is required for the android.storage import in main.py
requirements = python3,kivy==2.3.1,kivymd==1.2.0,android

# (str) Presplash/orientation
orientation = portrait
fullscreen = 0

# (list) Permissions
# This app only writes to its own private app storage (app_storage_details),
# so no extra storage permission is required.
android.permissions =

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Indicate whether the screen should stay on
android.wakelock = False

# (bool) Allow backup
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
