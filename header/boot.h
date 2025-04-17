#include "defines.h"
volatile char* const VIDEO_MEMORY_16 = (char*)0xB8000;

const char SCREEN_WIDTH = 80;
const char SCREEN_HEIGHT = 25;
// x2 because each character has a color byte aswell.
const int VIDEO_MEMORY_SIZE = (80 * 25) * 2;

struct video_state_16 {
    int column_location;
    int row_location;
};

typedef short bios_char;

extern void scroll_up(int lines);
extern void print(const char* pBuff);
extern void boot_main(void);