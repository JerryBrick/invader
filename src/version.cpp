// SPDX-License-Identifier: GPL-3.0-only

#include <invader/version.hpp>
#include <invader/hek/data_type.hpp>
#include <invader/printf.hpp>

#ifndef INVADER_VERSION_MAJOR
#define INVADER_VERSION_MAJOR 0
#define INVADER_VERSION_MINOR 0
#define INVADER_VERSION_PATCH 0
#else
#ifndef INVADER_VERSION_STRING
#include "version_str.hpp"
#endif
#endif

#ifndef INVADER_FORK
#define INVADER_FORK "Invader"
#endif

#ifndef INVADER_VERSION_STRING
#define INVADER_VERSION_STRING TOSTR(INVADER_VERSION_MAJOR) "." TOSTR(INVADER_VERSION_MINOR) "." TOSTR(INVADER_VERSION_PATCH) ".unknown"
#endif

#define INVADER_FULL_VERSION_STRING INVADER_FORK " " INVADER_VERSION_STRING

static_assert(sizeof(INVADER_FULL_VERSION_STRING) < sizeof(Invader::HEK::TagString), "version string " INVADER_FULL_VERSION_STRING " too long");

namespace Invader {
    void show_version_info() {
        oprintf("%s", full_version_and_credits());
    }

    const char *full_version() {
        return INVADER_FULL_VERSION_STRING;
    }

    const char *full_version_and_credits() {
        return INVADER_FULL_VERSION_STRING "\n\n"
               "This program is licensed under the GNU General Public License v3.0.\n"
               "\n"
               "Credits:\n"
               "  Kavawuvi                       - Lead Developer, Project owner\n"
               "  Vaporeon                       - Testing & QA, AUR maintainer, Development\n"
               "  MosesofEgypt                   - Tag data & model data research and code,\n"
               "                                   mouth data generation, ADPCM-XQ Xbox ADPCM\n"
               "                                   conversion\n"
               "\n"
               "Special thanks:\n"
               "  Tucker933                      - Hosting @ https://invader.opencarnage.net\n"
               "\n"
               "Software used in this program:\n"
               "  FreeType                       - https://www.freetype.org/\n"
               "  STB library                    - https://github.com/nothings/stb\n"
               "\n"
               "Other links:\n"
               "  Invader source code            - https://github.com/Kavawuvi/invader\n"
               "  Mo's Editing Kit               - https://github.com/MosesofEgypt/mek/\n";
    }
}
