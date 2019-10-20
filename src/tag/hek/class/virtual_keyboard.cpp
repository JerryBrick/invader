// SPDX-License-Identifier: GPL-3.0-only

#include "invader/tag/hek/compile.hpp"
#include "invader/tag/hek/class/virtual_keyboard.hpp"

namespace Invader::HEK {
    void compile_virtual_keyboard_tag(CompiledTag &compiled, const std::byte *data, std::size_t size) {
        BEGIN_COMPILE(VirtualKeyboard);
        ADD_DEPENDENCY_ADJUST_SIZES(tag.display_font);
        ADD_DEPENDENCY_ADJUST_SIZES(tag.background_bitmap);
        ADD_DEPENDENCY_ADJUST_SIZES(tag.special_key_labels_string_list);
        ADD_REFLEXIVE_START(tag.virtual_keys) {
            ADD_DEPENDENCY_ADJUST_SIZES(reflexive.unselected_background_bitmap);
            ADD_DEPENDENCY_ADJUST_SIZES(reflexive.selected_background_bitmap);
            ADD_DEPENDENCY_ADJUST_SIZES(reflexive.active_background_bitmap);
            ADD_DEPENDENCY_ADJUST_SIZES(reflexive.sticky_background_bitmap);
        } ADD_REFLEXIVE_END
        FINISH_COMPILE
    }
}
