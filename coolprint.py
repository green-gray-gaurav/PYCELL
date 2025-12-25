import textwrap

WIDTH = 120
class C:
    # Reset / styles
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"
    ITALIC     = "\033[3m"
    UNDERLINE  = "\033[4m"
    BLINK      = "\033[5m"
    REVERSE    = "\033[7m"
    STRIKE     = "\033[9m"

    # Standard foreground colors
    BLACK      = "\033[30m"
    RED        = "\033[31m"
    GREEN      = "\033[32m"
    YELLOW     = "\033[33m"
    BLUE       = "\033[34m"
    MAGENTA   = "\033[35m"
    CYAN       = "\033[36m"
    WHITE      = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK   = "\033[90m"
    BRIGHT_RED     = "\033[91m"
    BRIGHT_GREEN   = "\033[92m"
    BRIGHT_YELLOW  = "\033[93m"
    BRIGHT_BLUE    = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN    = "\033[96m"
    BRIGHT_WHITE   = "\033[97m"

    # Background colors
    BG_BLACK   = "\033[40m"
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"
    BG_WHITE   = "\033[47m"

    # Bright background colors
    BG_BRIGHT_BLACK   = "\033[100m"
    BG_BRIGHT_RED     = "\033[101m"
    BG_BRIGHT_GREEN   = "\033[102m"
    BG_BRIGHT_YELLOW  = "\033[103m"
    BG_BRIGHT_BLUE    = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN    = "\033[106m"
    BG_BRIGHT_WHITE   = "\033[107m"

    # 256-color helpers
    @staticmethod
    def fg256(n):
        return f"\033[38;5;{n}m"

    @staticmethod
    def bg256(n):
        return f"\033[48;5;{n}m"

# class C:
#     RESET   = "\033[0m"

#     BOLD    = "\033[1m"
#     DIM     = "\033[2m"

#     RED     = "\033[31m"
#     GREEN   = "\033[32m"
#     YELLOW  = "\033[33m"
#     BLUE    = "\033[34m"
#     MAGENTA = "\033[35m"
#     CYAN    = "\033[36m"
#     GRAY    = "\033[90m"

def style(
    text,
    *,
    fg=None,
    bg=None,
    bold=False,
    dim=False,
    underline=False,
    italic=False,
    reverse=False,
):
    codes = []

    if fg:
        codes.append(fg)
    if bg:
        codes.append(bg)

    if bold:
        codes.append(C.BOLD)
    if dim:
        codes.append(C.DIM)
    if underline:
        codes.append(C.UNDERLINE)
    if italic:
        codes.append(C.ITALIC)
    if reverse:
        codes.append(C.REVERSE)

    return f"{''.join(codes)}{text}{C.RESET}"



def colorize(text, *, fg=None, bg=None, **styles):
    return style(text, fg=fg, bg=bg, **styles)


# ────────────── Core Helpers ──────────────

def hline(left, fill, right, width=WIDTH, fg=None, bg=None, **styles):
    line = f"{left}{fill * (width - 2)}{right}"
    return colorize(line, fg=fg, bg=bg, **styles)


def print_box_title(title, width=WIDTH, fg=C.BLACK , bg = C.BG_BRIGHT_WHITE , **styles):
    print(hline("╔", "═", "╗", width, fg=fg, bg = bg , bold=True , **styles))
    print(colorize(f"║ {title.center(width - 4)} ║", fg=fg, bg = bg, bold=True , **styles))
    print(hline("╚", "═", "╝", width, fg=fg, bg= bg, bold=True , **styles))



def print_box_text(title, width=WIDTH, fg=C.BRIGHT_BLACK , bg = None , **styles):
    print(hline("┌", "─", "┐", width, fg=fg, bg = bg , bold=True , **styles))
    print(colorize(f"║ {title.center(width - 4)} ║", fg=fg, bg = bg, bold=True , **styles))
    print(hline("└", "─", "┘", width, fg=fg, bg= bg, bold=True , **styles))



def print_content(text, width=WIDTH):
    if not text:
        print(f"│ {'':<{width - 4}} │")
        return

    for line in text.splitlines():
        wrapped = textwrap.wrap(
            line,
            width=width - 4,
            replace_whitespace=False,
            drop_whitespace=False,
        ) or [""]

        for wline in wrapped:
            print(f"│ {wline.ljust(width - 4)} │")

# ────────────── Public Blocks ──────────────

def print_section(title, content, width=WIDTH, fg=C.BRIGHT_BLACK , bg = None , **styles):
    print(hline("┌", "─", "┐", width, fg=fg, bg = bg , bold=True , **styles))
    print(colorize(f"│ {title.ljust(width - 4)} │", fg=fg, bg = bg , bold=True , **styles))
    print(hline("├", "─", "┤", width, fg=fg, bg = bg , bold=True , **styles))
    print_content(content, width)
    print(hline("└", "─", "┘", width, fg=fg, bg = bg , bold=True , **styles))





