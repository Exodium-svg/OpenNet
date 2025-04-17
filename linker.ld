ENTRY(_entry)

SECTIONS {
    . = 0x7C00;

    .text : {
        *(.text)
    }

    .data : {
        *(.data)
    }

    .bss : {
        *(.bss)
    }

    /* Pad up to 510 bytes */
    . = 0x7C00 + 510;

    /* Write boot signature (0x55AA) */
    .sig : {
        SHORT(0xAA55)
    }
}