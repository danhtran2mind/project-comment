"""
ASCII Comment‑Banner Generator (Gradio)

Features
--------
- Choose comment style (full list from the supplied table)
- Set total width (characters)
- Set total height (lines) → padding above / below the text
- Align the inner text: left / centre / right
- Returns a ready‑to‑paste multi‑line comment banner.
"""

import gradio as gr

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
    "/* … */ (C‑style block)":                   ("/*", "*/"),
    "\"\"\" … \"\"\" (Python doc‑string, Elixir multi‑line string)": ('"""', '"""'),
    "--[[ … ]]" + " (Lua block comment)":        ("--[[", "]]"),
    "#= … =# (Julia block comment)":             ("#=", "=#"),
    "#| … |# (Clojure / CLisp / Racket block)": ("#|", "|#"),
    "<# … #> (PowerShell block comment)":        ("<#", "#>"),
    "=begin … =end (Ruby block comment)":        ("=begin", "=end"),

    # ----- languages that have both line‑ and block‑styles -------------
    "# (Python line comment)":                   ("#", "#"),
    "\"\"\" (Python triple‑quote doc‑string)":   ('"""', '"""'),
    "# (Ruby line comment)":                     ("#", "#"),
    "=begin/=end (Ruby block comment)":          ("=begin", "=end"),
    "REM (PowerShell line comment)":             ("#", "#"),
    "<# … #> (PowerShell block comment)":        ("<#", "#>"),

    # ----- extra / special cases ---------------------------------------
    "' (SQL single‑quote comment – rarely used)": ("'", "'"),
    "-- (Ada line comment)":                     ("--", "--"),
    "-- (COBOL comment – column 7)":             ("--", "--"),
    "` (Tcl comment – hash is normal, back‑tick rarely)": ("`", "`"),
    "/* … */ (CSS / Less / Sass SCSS)":          ("/*", "*/"),
    "/* … */ (GraphQL SDL – same as C‑style)":   ("/*", "*/"),
    "# (PowerShell line comment – alias for '--')": ("#", "#"),
    "# (R doc comment – same as Python)":        ("#", "#"),
    "# (Julia line comment)":                    ("#", "#"),
    "# (Nim line comment)":                     ("#", "#"),
    "# (Haxe line comment)":                    ("#", "#"),
    "# (Crystal line comment)":                  ("#", "#"),
    "# (F# line comment)":                       ("#", "#"),
    "# (D line comment)":                        ("#", "#"),
    "# (Go line comment)":                       ("#", "#"),
    "# (Kotlin line comment)":                   ("#", "#"),
    "# (Swift line comment)":                    ("#", "#"),
    "# (Rust line comment)":                     ("#", "#"),
    "# (Dart line comment)":                     ("#", "#"),
    "# (Scala line comment)":                    ("#", "#"),
    "# (Groovy line comment)":                   ("#", "#"),
    "# (Clojure line comment)":                  ("#", "#"),
    "# (Julia line comment)":                    ("#", "#"),
    "# (Racket line comment)":                   ("#", "#"),
    "# (Elixir line comment)":                   ("#", "#"),

    # ----- more block‑style families (HTML‑like) -----------------------
    "<!-- … --> (Markdown – HTML comment inside MD)": ("<!--", "-->"),
    "<!-- … --> (Asciidoc comment)":                ("<!--", "-->"),

    # You can keep adding entries here as you discover new syntaxes.
}

# ----------------------------------------------------------------------
# 2️⃣  Helper – build the banner
# ----------------------------------------------------------------------
def make_banner(
    text: str,
    width: int = 80,
    height: int = 5,
    align: str = "both",
    style: str = "# (sh, Python, Ruby, etc.)",
) -> str:
    """
    Build a comment banner according to the requested options.

    Parameters
    ----------
    text : str
        Caption that will appear inside the banner.
    width : int
        Desired total line width (including comment delimiters). Must be ≥ 20.
    height : int
        Desired total line count (≥ 3). Extra lines become empty padding.
    align : {"left", "both", "right"}
        Horizontal alignment of the caption.
    style : str
        Human‑readable comment style name – must exist in ``COMMENT_STYLES``.

    Returns
    -------
    str
        Multi‑line string containing the banner (including newline characters).
    """
    # ------------------------------------------------------------------
    # 1️⃣ Resolve comment delimiters
    # ------------------------------------------------------------------
    try:
        start, end = COMMENT_STYLES[style]
    except KeyError as exc:
        raise ValueError(f"Unsupported comment style: {style!r}") from exc

    # ------------------------------------------------------------------
    # 2️⃣ Compute usable width (space for dashes / text)
    # ------------------------------------------------------------------
    # Every line looks like: <start>␣<content>␣<end>
    usable = width - (len(start) + len(end) + 4)   # 4 = two spaces + two delimiters
    if usable < 1:                               # safety – expand if needed
        usable = 1
        width = len(start) + len(end) + 5

    # ------------------------------------------------------------------
    # 3️⃣ Build the three basic line types
    # ------------------------------------------------------------------
    border_line = f"{start} " + ("-" * usable) + f" {end}"

    if align == "left":
        inner = text.ljust(usable)
    elif align == "right":
        inner = text.rjust(usable)
    else:                     # centre (default)
        inner = text.center(usable)

    text_line  = f"{start} " + inner + f" {end}"
    empty_line = f"{start} " + (" " * usable) + f" {end}"

    # ------------------------------------------------------------------
    # 4️⃣ Vertical padding (height)
    # ------------------------------------------------------------------
    if height < 3:
        height = 3
    pad_total = height - 3               # lines that are not border / text
    pad_top   = pad_total // 2
    pad_bottom = pad_total - pad_top

    # ------------------------------------------------------------------
    # 5️⃣ Assemble everything
    # ------------------------------------------------------------------
    lines = [border_line]
    lines += [empty_line] * pad_top
    lines.append(text_line)
    lines += [empty_line] * pad_bottom
    lines.append(border_line)

    return "\n".join(lines)


# ----------------------------------------------------------------------
# 3️⃣  Gradio UI definition – offers every style from the table
# ----------------------------------------------------------------------
demo = gr.Interface(
    fn=make_banner,
    inputs=[
        gr.Textbox(
            label="Banner text",
            placeholder="Enter your caption here…",
            lines=1,
        ),
        gr.Slider(
            minimum=20,
            maximum=200,
            step=2,
            value=80,
            label="Total width (characters)",
        ),
        gr.Slider(
            minimum=3,
            maximum=30,
            step=1,
            value=5,
            label="Total height (lines)",
        ),
        gr.Dropdown(
            choices=["left", "both", "right"],
            value="both",
            label="Text alignment",
        ),
        gr.Dropdown(
            choices=sorted(COMMENT_STYLES.keys()),
            value="# (sh, Python, Ruby, etc.)",
            label="Comment style",
        ),
    ],
    outputs=gr.Textbox(
        label="Generated ASCII banner",
        lines=12,
        interactive=False,
    ),
    title="🖼️ ASCII Comment‑Banner Generator",
    description=(
        "Create ready‑to‑paste comment blocks for dozens of programming languages. "
        "Pick the width, height, alignment, and any comment style from the full list."
    ),
    examples=[
        [
            "DATA & TRAINING CONFIGURATION PROCESSING",
            80,
            5,
            "both",
            "# (sh, Python, Ruby, etc.)",
        ],
        [
            "WELCOME TO MY PROJECT",
            60,
            7,
            "left",
            "// (C‑family, JavaScript, Go, Rust…)",
        ],
        [
            "⚡️ QUICK START",
            70,
            4,
            "right",
            "/* … */ (C‑style block)",
        ],
        [
            "HTML HEADER",
            70,
            5,
            "both",
            "<!-- … --> (HTML / XML)",
        ],
        [
            "POWER‑SHELL MODULE",
            70,
            5,
            "both",
            "<# … #> (PowerShell block comment)",
        ],
        [
            "RUBY BLOCK DOC",
            70,
            5,
            "both",
            "=begin … =end (Ruby block comment)",
        ],
    ],
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch()
