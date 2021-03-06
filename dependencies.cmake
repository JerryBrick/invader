# SPDX-License-Identifier: GPL-3.0-only

# Find some packages
find_package(Python3 REQUIRED)
find_package(Threads REQUIRED)
find_package(ZLIB)
find_package(LibArchive)
find_package(Freetype)
find_package(Git)

option(INVADER_USE_ZLIB "set whether or not to use zlib - required for invader-bitmap and MCC map compatibility" ${ZLIB_FOUND})

if(${ZLIB_FOUND} AND ${INVADER_USE_ZLIB})
    set(DEP_ZLIB_LIBRARIES ${ZLIB_LIBRARIES})
else()
    set(DEP_ZLIB_LIBRARIES "")
    add_definitions(-DDISABLE_ZLIB)
endif()

option(INVADER_USE_AUDIO "set whether or not to use ogg vorbis, FLAC, and secret rabbit code - required for invader-sound as well as certain features of invader-edit-qt and dark circlet" YES)
if(${INVADER_USE_AUDIO})
    set(DEP_AUDIO_LIBRARIES FLAC ogg vorbis vorbisenc samplerate)
else()
    add_definitions(-DDISABLE_AUDIO)
    set(DEP_AUDIO_LIBRARIES "")
endif()
