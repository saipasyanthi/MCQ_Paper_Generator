[app]
title = MCQ Paper Generator
package.name = mcqpaper
package.domain = org.example
version = 0.1.0
version.regex = ^[0-9]+\.[0-9]+\.[0-9]+$
source.dir = .
source.include_exts = py,kv,json,png,jpg,ttf
requirements = python3,kivy,pypdf2,reportlab
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# License bundling: copy license.json to assets before build
# (buildozer will package it with the app)
presplash.filename = 
icon.filename = 

[buildozer]
log_level = 2
warn_on_root = 1
