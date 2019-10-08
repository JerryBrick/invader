// SPDX-License-Identifier: GPL-3.0-only

#ifndef INVADER__TAG__HEK__CLASS__LIGHTNING_HPP
#define INVADER__TAG__HEK__CLASS__LIGHTNING_HPP

#include "../../compiled_tag.hpp"
#include "../../../hek/data_type.hpp"
#include "../header.hpp"
#include "enum.hpp"
#include "bitfield.hpp"
#include "particle.hpp"

namespace Invader::HEK {
    struct LightningMarkerFlag {
        std::uint16_t not_connected_to_next_marker : 1;
    };

    ENDIAN_TEMPLATE(EndianType) struct LightningMarker {
        TagString attachment_marker;
        EndianType<LightningMarkerFlag> flags;
        PAD(0x2);
        EndianType<std::int16_t> octaves_to_next_marker;
        PAD(0x2);
        PAD(0x4C);
        Vector3D<EndianType> random_position_bounds;
        EndianType<float> random_jitter;
        EndianType<float> thickness;
        ColorARGB<EndianType> tint;
        PAD(0x4C);

        ENDIAN_TEMPLATE(NewType) operator LightningMarker<NewType>() const noexcept {
            LightningMarker<NewType> copy = {};
            COPY_THIS(attachment_marker);
            COPY_THIS(flags);
            COPY_THIS(octaves_to_next_marker);
            COPY_THIS(random_position_bounds);
            COPY_THIS(random_jitter);
            COPY_THIS(thickness);
            COPY_THIS(tint);
            return copy;
        }
    };
    static_assert(sizeof(LightningMarker<NativeEndian>) == 0xE4);

    ENDIAN_TEMPLATE(EndianType) struct LightningShader {
        PAD(0x24);
        LittleEndian<std::uint32_t> make_it_work;
        EndianType<ParticleShaderFlags> shader_flags;
        EndianType<FramebufferBlendFunction> framebuffer_blend_function;
        EndianType<FramebufferFadeMode> framebuffer_fade_mode;
        EndianType<IsUnfilteredFlag> map_flags;
        PAD(0x1C);
        PAD(0xC);
        LittleEndian<std::uint32_t> some_more_stuff_that_should_be_set_for_some_reason;
        PAD(0x2);
        PAD(0x2);
        PAD(0x38);
        PAD(0x1C);

        ENDIAN_TEMPLATE(NewType) operator LightningShader<NewType>() const noexcept {
            LightningShader<NewType> copy = {};
            COPY_THIS(make_it_work);
            COPY_THIS(shader_flags);
            COPY_THIS(framebuffer_blend_function);
            COPY_THIS(framebuffer_fade_mode);
            COPY_THIS(map_flags);
            COPY_THIS(some_more_stuff_that_should_be_set_for_some_reason);
            return copy;
        }
    };
    static_assert(sizeof(LightningShader<NativeEndian>) == 0xB4);

    ENDIAN_TEMPLATE(EndianType) struct Lightning {
        PAD(0x2);
        EndianType<std::int16_t> count;
        PAD(0x10);
        EndianType<float> near_fade_distance;
        EndianType<float> far_fade_distance;
        PAD(0x10);
        EndianType<FunctionOut> jitter_scale_source;
        EndianType<FunctionOut> thickness_scale_source;
        EndianType<FunctionNameNullable> tint_modulation_source;
        EndianType<FunctionOut> brightness_scale_source;
        TagDependency<EndianType> bitmap; // bitmap
        PAD(0x54);
        TagReflexive<EndianType, LightningMarker> markers;
        TagReflexive<EndianType, LightningShader> shader;
        PAD(0x58);

        ENDIAN_TEMPLATE(NewType) operator Lightning<NewType>() const noexcept {
            Lightning<NewType> copy = {};
            COPY_THIS(count);
            COPY_THIS(near_fade_distance);
            COPY_THIS(far_fade_distance);
            COPY_THIS(jitter_scale_source);
            COPY_THIS(thickness_scale_source);
            COPY_THIS(tint_modulation_source);
            COPY_THIS(brightness_scale_source);
            COPY_THIS(bitmap);
            COPY_THIS(markers);
            COPY_THIS(shader);
            return copy;
        }
    };
    static_assert(sizeof(Lightning<BigEndian>) == 0x108);

    void compile_lightning_tag(CompiledTag &compiled, const std::byte *data, std::size_t size);
}
#endif
