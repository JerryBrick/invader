# SPDX-License-Identifier: GPL-3.0-only

import sys
import json
import os

if len(sys.argv) < 3:
    print("Usage: {} <definition.hpp> <parser.hpp> <json> [json [...]]".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

files = []
all_enums = []
all_bitfields = []
all_structs = []

for i in range(3, len(sys.argv)):
    def make_name_fun(name, ignore_numbers):
        name = name.replace(" ", "_").replace("'", "")
        if not ignore_numbers and name[0].isnumeric():
            name = "_{}".format(name)
        return name

    objects = None
    with open(sys.argv[i], "r") as f:
        objects = json.loads(f.read())
    name = os.path.basename(sys.argv[i]).split(".")[0]
    files.append(name)

    # Get all enums, bitfields, and structs
    for s in objects:
        if s["type"] == "enum":
            for o in range(len(s["options"])):
                s["options"][o] = make_name_fun(s["options"][o], True)
            all_enums.append(s)
        elif s["type"] == "bitfield":
            for f in range(len(s["fields"])):
                s["fields"][f] = make_name_fun(s["fields"][f], False)
            all_bitfields.append(s)
        elif s["type"] == "struct":
            for f in s["fields"]:
                if f["type"] != "pad":
                    f["name"] = make_name_fun(f["name"], False)
            all_structs.append(s)
        else:
            print("Unknown object type {}".format(s["type"]), file=sys.stderr)
            sys.exit(1)

# Basically, we're going to be rearranging structs so that structs that don't have dependencies get added first. Structs that do get added last, and they only get added once their dependencies are added
all_structs_arranged = []
def add_struct(name):
    # Make sure we aren't already added
    for s in all_structs_arranged:
        if s["name"] == name:
            return

    # Get all their dependencies
    dependencies = []

    # Get the struct
    struct_to_add = None
    for s in all_structs:
        if s["name"] == name:
            struct_to_add = s
            break

    if not struct_to_add:
        if name != "PredictedResource":
            print("Warning: Unknown struct {}".format(name), file=sys.stderr)
        return

    if "inherits" in struct_to_add:
        dependencies.append(struct_to_add["inherits"])

    for f in s["fields"]:
        if f["type"] == "TagReflexive":
            if f["struct"] not in dependencies:
                dependencies.append(f["struct"])

    for d in dependencies:
        add_struct(d)

    all_structs_arranged.append(struct_to_add)

for s in all_structs:
    add_struct(s["name"])

def to_hex(number):
    return "0x{:X}".format(number)

with open(sys.argv[1], "w") as f:
    f.write("// SPDX-License-Identifier: GPL-3.0-only\n\n// This file was auto-generated.\n// If you want to edit this, edit the .json definitions and rerun the generator script, instead.\n\n")
    header_name = "INVADER__TAG__HEK__CLASS__DEFINITION_HPP"
    f.write("#ifndef {}\n".format(header_name))
    f.write("#define {}\n\n".format(header_name))
    f.write("#include \"../../hek/data_type.hpp\"\n\n")
    f.write("namespace Invader::HEK {\n")

    # Write enums at the top first, then bitfields
    for e in all_enums:
        f.write("    enum {} : TagEnum {{\n".format(e["name"]))

        # Convert PascalCase to UPPER_SNAKE_CASE
        prefix = ""
        name_to_consider = e["name"].replace("HUD", "Hud").replace("UI", "Ui")
        for i in name_to_consider:
            if prefix != "" and i.isupper():
                prefix += "_"
            prefix += i.upper()

        for n in range(0,len(e["options"])):
            f.write("        {}_{}{}\n".format(prefix,e["options"][n].upper(), "," if n + 1 < len(e["options"]) else ""))

        f.write("    };\n")

    for b in all_bitfields:
        f.write("    struct {} {{\n".format(b["name"]))
        for q in b["fields"]:
            f.write("        std::uint{}_t {} : 1;\n".format(b["width"], q))
        f.write("    };\n")

    # Now the hard part
    padding_present = False

    for s in all_structs_arranged:
        f.write("    ENDIAN_TEMPLATE(EndianType) struct {} {}{{\n".format(s["name"], ": {}<EndianType> ".format(s["inherits"]) if "inherits" in s else ""))
        for n in s["fields"]:
            type_to_write = n["type"]

            if type_to_write.startswith("int") or type_to_write.startswith("uint"):
                type_to_write = "std::{}_t".format(type_to_write)
            elif type_to_write == "pad":
                f.write("        PAD(0x{:X});\n".format(n["size"]))
                continue

            if "flagged" in n and n["flagged"]:
                type_to_write = "FlaggedInt<{}>".format(type_to_write)

            name = n["name"]
            if "count" in n:
                name = "{}[{}]".format(name, n["count"])

            format_to_use = None

            default_endian = "EndianType"
            if "endian" in n:
                if n["endian"] == "little":
                    default_endian = "LittleEndian"
                elif n["endian"] == "big":
                    default_endian = "BigEndian"
                elif n["endian"] == None:
                    default_endian = None

            if type_to_write == "TagReflexive":
                f.write("        TagReflexive<{}, {}> {};\n".format(default_endian, n["struct"], name))
            else:
                if default_endian is None:
                    format_to_use = "{}"
                elif "compound" in n and n["compound"]:
                    format_to_use = "{{}}<{}>".format(default_endian)
                else:
                    format_to_use = "{}<{{}}>".format(default_endian)

                if "bounds" in n and n["bounds"]:
                    f.write("        Bounds<{}> {};\n".format(format_to_use.format(type_to_write), name))
                else:
                    f.write("        {} {};\n".format(format_to_use.format(type_to_write), name))

        # Make sure we have all of the structs we depend on, too
        depended_structs = []
        dependency = s
        padding_present = False

        while dependency is not None:
            depended_structs.append(dependency)
            if not padding_present:
                for n in dependency["fields"]:
                    if n["type"] == "pad":
                        padding_present = True
                        break
            if "inherits" in dependency:
                dependency_name = dependency["inherits"]
                dependency = None
                for ds in all_structs_arranged:
                    if ds["name"] == dependency_name:
                        dependency = ds
                        break
            else:
                break

        # And we can't forget the copy part
        f.write("        ENDIAN_TEMPLATE(NewEndian) operator {}<NewEndian>() const noexcept {{\n".format(s["name"]))
        f.write("            {}<NewEndian> copy{};\n".format(s["name"], " = {}" if padding_present else ""))

        for ds in depended_structs:
            for n in ds["fields"]:
                if n["type"] == "pad":
                    continue
                else:
                    f.write("            {}({});\n".format("COPY_THIS_ARRAY" if "count" in n else "COPY_THIS", n["name"]))
        f.write("            return copy;\n")
        f.write("        }\n")

        f.write("    };\n")
        f.write("    static_assert(sizeof({}<NativeEndian>) == 0x{:X});\n".format(s["name"], s["size"]))

    f.write("}\n\n")
    f.write("#endif\n")

with open(sys.argv[2], "w") as f:
    f.write("// SPDX-License-Identifier: GPL-3.0-only\n\n// This file was auto-generated.\n// If you want to edit this, edit the .json definitions and rerun the generator script, instead.\n\n")
    header_name = "INVADER__TAG__PARSER__PARSER_HPP"
    f.write("#ifndef {}\n".format(header_name))
    f.write("#define {}\n\n".format(header_name))
    f.write("#include <string>\n")
    f.write("#include \"../hek/definition.hpp\"\n\n")
    f.write("namespace Invader::Parser {\n")
    f.write("    struct Dependency {\n")
    f.write("        TagClassInt tag_class_int;\n")
    f.write("        std::string path;\n")
    f.write("    };\n")
    for s in all_structs:
        f.write("    class {} {{\n".format(s["name"]))
        def add_structs_from_struct(struct):
            if "inherits" in struct:
                for t in all_structs:
                    if t["name"] == struct["inherits"]:
                        add_structs_from_struct(t)
                        break
            for t in struct["fields"]:
                if t["type"] == "pad":
                    continue
                type_to_write = t["type"]
                if type_to_write.startswith("int") or type_to_write.startswith("uint"):
                    type_to_write = "std::{}_t".format(type_to_write)
                elif type_to_write == "float":
                    type_to_write = "float"
                elif type_to_write == "TagDependency":
                    type_to_write = "Dependency"
                elif type_to_write == "TagReflexive":
                    type_to_write = "std::vector<HEK::{}>".format(t["struct"])
                elif type_to_write == "TagDataOffset":
                    type_to_write = "std::vector<std::byte>"
                else:
                    type_to_write = "HEK::{}".format(type_to_write)
                if "compound" in t and t["compound"]:
                    type_to_write = "{}<NativeEndian>".format(type_to_write)
                if "bounds" in t and t["bounds"]:
                    type_to_write = "Bounds<{}>".format(type_to_write)
                f.write("        {} {};\n".format(type_to_write, t["name"]))
                continue
        add_structs_from_struct(s)
        f.write("    };\n")
    f.write("}\n")
    f.write("#endif\n")
    pass
