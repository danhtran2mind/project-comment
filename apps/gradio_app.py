"""
ASCII Comment‑Banner Generator (Gradio)

Features
--------
- Choose any comment style (full list from the supplied table)
- Set total width (characters) and total height (lines)
- Horizontal alignment   : left / centre / right
- Vertical   alignment   : top / centre / bottom
- Border filler          : '-', '=', '^' or any custom string
- Returns a ready‑to‑paste multi‑line comment banner.
"""

import gradio as gr
from itertools import cycle

# ----------------------------------------------------------------------
# 1️⃣  Mapping from UI‑friendly names → (start_delim, end_delim)
# ----------------------------------------------------------------------
COMMENT_STYLES: dict[str, tuple[str, str]] = {
    # ----- single‑line comment families ---------------------------------
    "# (sh, Python, Ruby, etc.)":                 ("#", "#"),
    "// (C‑family, JavaScript, Go, Rust…)":      ("//", "//"),
    "; (MASM/TASM, Lisp families)":               (";", ";"),
    "-- (SQL, Haskell, Ada, VHDL…)":              ("--", "--"),
    "% (MATLAB/Octave, LaTeX)":                   ("%", "%"),
    "' (VB, VBA, VB.NET)":                       ("'", "'"),
    "` (legacy shell)":                           ("`", "`"),
    "REM (Batch files)":                         ("REM", "REM"),
    ":: (Batch hack, works in PowerShell)":      ("::", "::"),
    ";; (Racket, Scheme, Clojure read‑time comment)": (";;", ";;"),

    # ----- block‑only comment families ---------------------------------
    "<!-- … --> (HTML / XML)":                   ("<!--", "-->"),
    "/* … */ (C‑style block)":                  ("/*", "*/"),
    "\"\"\" … \"\"\" (Python doc‑string, Elixir multi‑line string)": ('"""', '"""'),
    "--[[ … ]]" + " (Lua block comment)":        ("--[[", "]]"),
    "#= … =# (Julia block comment)":            ("#=", "=#"),
    "#| … |# (Clojure / CLisp / Racket block)": ("#|", "|#"),
    "<# … #> (PowerShell block comment)":       ("<#", "#>"),
    "=begin … =end (Ruby block comment)":       ("=begin", "=end"),

    # ----- languages that have both line‑ and block‑styles -------------
    "# (Python line comment)":                  ("#", "#"),
    "\"\"\" (Python triple‑quote doc‑string)":  ('"""', '"""'),
    "# (Ruby line comment)":                    ("#", "#"),
    "=begin/=end (Ruby block comment)":         ("=begin", "=end"),
    "REM (PowerShell line comment)":            ("#", "#"),
    "<# … #> (PowerShell block comment)":       ("<#", "#>"),

    # ----- extra / special cases ---------------------------------------
    "' (SQL single‑quote comment – rarely used)": ("'", "'"),
    "-- (Ada line comment)":                    ("--", "--"),
    "-- (COBOL comment – column 7)":            ("--", "--"),
    "` (Tcl comment – back‑tick rarely used)":  ("`", "`"),
    "/* … */ (CSS / Less / Sass SCSS)":         ("/*", "*/"),
    "/* … */ (GraphQL SDL – same as C‑style)":  ("/*", "*/"),
    "# (PowerShell line comment – alias for '--')": ("#", "#"),

    # ----- more block‑style families (HTML‑like) -----------------------
    "<!-- … --> (Markdown – HTML comment inside MD)": ("<!--", "-->"),
    "<!-- … --> (Asciidoc comment)":                ("<!--", "-->"),
}

# ----------------------------------------------------------------------
# 2️⃣  Helper – repeat a pattern so it exactly matches a given length
# ----------------------------------------------------------------------
def _repeat_pattern(pattern: str, length: int) -> str:
    """Return *pattern* repeated/cycled until *length* characters are filled."""
    if not pattern:
        pattern = "-"                     # safe fallback
    return "".join(c for _, c in zip(range(length), cycle(pattern)))


# ----------------------------------------------------------------------
# 3️⃣  Core – create the banner
# ----------------------------------------------------------------------
def make_banner(
    text: str,
    width: int = 80,
    height: int = 5,
    h_align: str = "both",          # left / both / right
    v_align: str = "both",          # top / both / bottom
    style: str = "# (sh, Python, Ruby, etc.)",
    filler: str = "-",              # what to repeat on the top/bottom border
) -> str:
    """
    Build a comment banner.

    Parameters
    ----------
    text, width, height, h_align, v_align, style – see docstring above.
    filler : str
        String that will be repeated (cycled) on the top and bottom border.
        Any length is accepted.
    """
    # ------------------- 1️⃣ Resolve comment delimiters -------------------
    try:
        start, end = COMMENT_STYLES[style]
    except KeyError as exc:
        raise ValueError(f"Unsupported comment style: {style!r}") from exc

    # ------------------- 2️⃣ Usable width ---------------------------------
    # pattern: <start>␣<content>␣<end>
    usable = width - (len(start) + len(end) + 4)   # 4 = two spaces + two delimiters
    if usable < 1:                                 # safety – enlarge if needed
        usable = 1
        width = len(start) + len(end) + 5

    # ------------------- 3️⃣ Build line types ----------------------------
    border_line = f"{start} " + _repeat_pattern(filler, usable) + f" {end}"

    # horizontal alignment of the inner text
    if h_align == "left":
        inner = text.ljust(usable)
    elif h_align == "right":
        inner = text.rjust(usable)
    else:   # centre (default)
        inner = text.center(usable)

    text_line  = f"{start} " + inner + f" {end}"
    empty_line = f"{start} " + (" " * usable) + f" {end}"

    # ------------------- 4️⃣ Vertical padding ---------------------------
    if height < 3:
        height = 3
    pad_total = height - 3            # lines that are not border / text

    if v_align == "top":
        pad_top, pad_bottom = 0, pad_total
    elif v_align == "bottom":
        pad_top, pad_bottom = pad_total, 0
    else:  # centre (default)
        pad_top = pad_total // 2
        pad_bottom = pad_total - pad_top

    # ------------------- 5️⃣ Assemble -------------------------------
    lines = [border_line]                     # top border
    lines += [empty_line] * pad_top           # upper padding
    lines.append(text_line)                   # caption line
    lines += [empty_line] * pad_bottom        # lower padding
    lines.append(border_line)                 # bottom border

    return "\n".join(lines)


# ----------------------------------------------------------------------
# 4️⃣  Helper – decide which filler string to actually use
# ----------------------------------------------------------------------
def _resolve_filler(preset: str, custom: str) -> str:
    """Return the string that should be repeated on the border."""
    if preset == "custom":
        return custom or "-"          # fall back to dash if custom empty
    return preset                    # '-', '=', '^', …


# ----------------------------------------------------------------------
# 5️⃣  Gradio UI
# ----------------------------------------------------------------------
# First we build the component list – this is needed so we can refer to it
# later when we wrap the function that handles the custom filler.
input_components = [
    gr.Textbox(label="Banner text",
               placeholder="Enter your caption here…",
               lines=1),

    gr.Slider(minimum=20, maximum=200, step=2, value=80,
              label="Total width (characters)"),

    gr.Slider(minimum=3, maximum=30, step=1, value=5,
              label="Total height (lines)"),

    gr.Dropdown(choices=["left", "both", "right"],
                value="both",
                label="Horizontal alignment"),

    gr.Dropdown(choices=["top", "both", "bottom"],
                value="both",
                label="Vertical alignment"),

    gr.Dropdown(choices=sorted(COMMENT_STYLES.keys()),
                value="# (sh, Python, Ruby, etc.)",
                label="Comment style"),

    gr.Dropdown(choices=["-", "=", "^", "custom"],
                value="-",
                label="Border filler (preset)"),

    gr.Textbox(label="Custom filler (used only when preset = ‘custom’)",
               placeholder="e.g. *~*   – leave empty for default ‘-’",
               lines=1),
]

output_component = gr.Textbox(label="Generated ASCII banner",
                             lines=14,
                             interactive=False)

def _gradio_wrapper(
    text, width, height,
    h_align, v_align, style,
    filler_preset, filler_custom
):
    """Wrapper called by Gradio – resolves the custom filler first."""
    filler = _resolve_filler(filler_preset, filler_custom)
    return make_banner(
        text=text,
        width=width,
        height=height,
        h_align=h_align,
        v_align=v_align,
        style=style,
        filler=filler,
    )

demo = gr.Interface(
    fn=_gradio_wrapper,
    inputs=input_components,
    outputs=output_component,
    title="🖼️ ASCII Comment‑Banner Generator",
    description=(
        "Create ready‑to‑paste comment blocks for dozens of programming languages. "
        "Pick width, height, horizontal & vertical alignment, any comment style, "
        "and the character(s) that will form the top/bottom border (preset ‘-’, ‘=’, ‘^’, "
        "or a custom string)."
    ),
    examples=[
        #   text                               w  h  h‑align v‑align style                                   filler preset custom
        [
            "DATA & TRAINING CONFIGURATION PROCESSING",
            80, 5, "both", "both", "# (sh, Python, Ruby, etc.)",   "-",      "",
        ],
        [
            "WELCOME TO MY PROJECT",
            60, 7, "left", "top", "// (C‑family, JavaScript, Go, Rust…)", "=",      "",
        ],
        [
            "⚡️ QUICK START",
            70, 4, "right", "bottom", "/* … */ (C‑style block)", "^",      "",
        ],
        [
            "CUSTOM FILLER EXAMPLE",
            70, 5, "both", "both", "# (sh, Python, Ruby, etc.)",   "custom", "*~*",
        ],
        [
            "HTML HEADER",
            70, 5, "both", "top", "<!-- … --> (HTML / XML)",    "-",      "",
        ],
        [
            "POWER‑SHELL MODULE",
            70, 5, "both", "bottom", "<# … #> (PowerShell block comment)", "-", "",
        ],
    ],
    allow_flagging="never",
)

if __name__ == "__main__":
    # `share=True` will give you a public URL (optional)
    demo.launch()
