import os
import sys
from pathlib import Path
import subprocess

BIOS_SIZE = 512

NASM_FLAGS = ["-f", "elf"]
with open("compile_flags.txt") as f:
    FLAGS = f.read().split()

SRC_DIR = "src/"
INC_DIR = "header/"
OBJ_DIR = "obj/"
OUT_DIR = "bin/"

def exec(command: list[str], error_description: None|str = None, success_description: None|str = None) -> bool:
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] {error_description or ' '.join(command)}")
        print(result.stderr)
        return False
    else:
        print(f"[INFO] {success_description or ' '.join(command)}")

    return True

def link_objects(obj_folder: Path, output_executable: Path) -> bool:
    object_files = [str(p) for p in obj_folder.glob("*.o")]
    result = exec(
        ["ld", "-m", "elf_i386", "-T", "linker.ld", "-nostdlib", "-o", str(output_executable)] + object_files,
        "Linking failed",
        "Linked successfully"
    )

    if result is not True:
        return False
    
    # Convert to flat binary for boot
    result = exec(
        ["objcopy","-R", ".bss", "-O", "binary", str(output_executable), str(output_executable.with_suffix(".bin"))],
        "Objcopy failed",
        f"Created binary: {output_executable.with_suffix('.bin')}"
    )

    if(result is not True):
        return False
    
    final_binary = output_executable.with_suffix(".bin")

    binary_size = final_binary.stat().st_size
    if binary_size != BIOS_SIZE:
        print(f"[ERROR] Binary size is {binary_size} bytes, expected 512 bytes.")
        return False
    

def assemble_object(filePath:str, flags:str, output:str) -> bool:
    return exec(
        ["nasm", *NASM_FLAGS, filePath, "-o", output + Path(filePath).stem + ".0"],
        f"Failed to assemble {filePath}",
        f"Assembled {filePath} as translation unit"
    )

def compile_object(filePath:str, flags:str, output:str) -> bool:
    return exec(
        ["clang", "-c", filePath, "-o", output] + flags,
        f"Failed to compile {filePath}",
        f"Compiled {filePath} as translation unit"
    )

def get_source_files(directory: Path) -> list[Path]:
    return [p for p in directory.rglob("*") if p.is_file()]

def has_valid_translation_unit(src_file: Path, obj_file: Path) -> bool:
    if not obj_file.exists():
        return False
    
    return src_file.stat().st_mtime_ns == obj_file.stat().st_mtime_ns

def main():
    # --- not relevant yet ---
    # if(1 > len(sys.argv)):
    #     print("Missing parameter release mode, can either be RELEASE | DEBUG")
    #     return
     
    # release_mode = sys.argv[0].upper()
 
    # if("RELEASE" or "DEBUG" != release_mode):
    #     print("Invalid mode, can either be RELEASE | DEBUG")
    #     return

    for src_file in get_source_files(Path(SRC_DIR)):
        obj_file = OBJ_DIR + (src_file.stem + ".o")

        if has_valid_translation_unit(Path(src_file), Path(obj_file)):
            continue

        suffix = src_file.suffix

        if suffix == ".asm":
            if not assemble_object(src_file, NASM_FLAGS, OBJ_DIR):
                return
        elif suffix == ".c":
            if not compile_object(src_file, FLAGS, obj_file):
                return
        else:
            raise f"Unknown file type: {src_file.name}"
    
    link_objects(Path(OBJ_DIR), Path(OUT_DIR + "OpenNet.bin"))
    return

if __name__ == "__main__":
    main()