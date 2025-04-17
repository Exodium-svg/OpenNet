bits 16
section .text

global _entry
extern boot_main
%define boot_loader_section 0x7C00
_entry:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov sp, boot_loader_section

    ; Clear general purpose registers as well
    xor bx, bx
    xor cx, cx
    xor dx, dx
    xor si, si
    xor di, di
    xor bp, bp

    ; Call boot_main ( for this to work we need to be in the ELF format, or this will simply not work! )
    call boot_main
    ; Boot signature
