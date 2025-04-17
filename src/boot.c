#include "boot.h"

static struct video_state_16 console_state;


void scroll_up(int lines) {
    __asm__ __volatile__ (
        "mov ah, 0x06\n"
        "mov al, %0\n" 
        "mov bh, 0x07\n"
        "mov ch, 0\n"
        "mov cl, 0\n"
        "mov dh, 24\n"
        "mov dl, 79\n"
        "int 0x10\n"
        :
        : "r" ((char)lines) // first input
        : "ah", "al", "bh", "ch", "cl", "dh", "dl" // Tell compiler which registers we changed.
    );
}

void print(const char* pBuff) {

    // if we are on row 25 we should implement scrolling.
    if(SCREEN_HEIGHT == console_state.row_location && SCREEN_WIDTH == console_state.column_location) {
        // we need to clean the first line and move everything up?
        scroll_up(1);
        console_state.row_location = --console_state.row_location;
        console_state.column_location = 0;
    }

    const int offset = (console_state.row_location * SCREEN_WIDTH + console_state.column_location);
    
    // Each entry in the memory exists out of 2 bytes, character and color.
    for(int i = 0; '\0' != pBuff[i]; i +=2) {
        char character = pBuff[i];

        if(console_state.column_location >= SCREEN_WIDTH) {
            console_state.column_location = 0;
            console_state.row_location++;

            if(console_state.row_location >= SCREEN_HEIGHT)
                scroll_up(1);
        }

        VIDEO_MEMORY_16[i + offset] = character;
        // Set color black on white
        VIDEO_MEMORY_16[i + offset+1] = 0x0F;

        console_state.column_location++;
    }
}

// Ensure that fastcall or stdcalls have not been made.
__attribute__((cdecl)) void boot_main(void) {
    {
        // null it's memory in a different stack.
        char* p_text_state = (char*)&console_state;

        for(unsigned long i = 0; i < sizeof(struct video_state_16); ++i)
            p_text_state[i] = 0;
    }
    
    print("Hello world\n");
}