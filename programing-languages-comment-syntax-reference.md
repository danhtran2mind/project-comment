# Comment Syntax Reference Table 📝

Below is a comprehensive reference table of comment syntaxes for single-line and multi-line/block comments across various programming, scripting, and markup languages. This table is formatted as a Markdown code block, ready to be copied into a README, wiki, or any Markdown-aware document. 🚀

| Language / Family                              | Single-line Comment | Multi-line / Block Comment | Remarks / Variants 📜 |
|:---------------------------------------------:|:------------------:|:------------------------:|:-------------------:|
| **C / C++ / C# / Java / JavaScript / D / Go / Rust / Kotlin / Swift / Objective-C / TypeScript / Dart / Scala / Groovy / Clojure / F# / Julia** | `//` | `/* … */` | Some (C#, Kotlin, Swift, Scala, Groovy, Dart) support `///` or `/** */` for documentation comments 📚 |
| **C-style (Pascal, Delphi, FreePascal)**      | ⃠ | `{ … }` or `(* … *)` | Both block styles accepted; `{}` is most common 🛠️ |
| **Python**                                    | `#` | ⃠ | Triple-quoted strings `''' … '''` or `""" … """` are *doc-strings*, not true comments 🐍 |
| **Ruby**                                      | `#` | `=begin … =end` (must start at column 1) | ⃠ 💎 |
| **Perl / PHP / Bash / sh / ksh / zsh / awk / sed** | `#` | ⃠ | PHP also supports `/* … */` and `//` 🐘 |
| **PHP**                                       | `#` or `//` | `/* … */` | `#` works only when PHP code is not embedded in HTML 🌐 |
| **Lua**                                       | `--` | `--[[ … ]]` (or `--[=[ … ]=]` for nesting) | ⃠ 🌙 |
| **R**                                         | `#` | ⃠ | ⃠ 📊 |
| **MATLAB / Octave**                           | `%` | `%{ … %}` (MATLAB R2016b+) | Octave also accepts `#` 🔢 |
| **SQL (Standard, MySQL, PostgreSQL, SQLite, Oracle, etc.)** | `--` | `/* … */` | MySQL also allows `#` 🗄️ |
| **PL/SQL**                                    | `--` | `/* … */` | ⃠ 🗄️ |
| **T-SQL / Transact-SQL**                      | `--` | `/* … */` | ⃠ 🗄️ |
| **HTML / XML**                                | ⃠ | `<!-- … -->` | No line-comment syntax 🌍 |
| **SGML / DOCTYPE**                            | ⃠ | `<!-- … -->` | ⃠ 📜 |
| **LaTeX / TeX**                               | `%` | ⃠ | ⃠ 📝 |
| **Makefile**                                  | `#` | ⃠ | ⃠ 🛠️ |
| **Assembly (MASM / TASM)**                    | `;` | ⃠ | ⃠ 💻 |
| **GNU Assembler (GAS)**                       | `#` | `/* … */` (rare, via pseudo-ops) | ⃠ 💻 |
| **Haskell**                                   | `--` | `{- … -}` | Block comments can be nested 🧠 |
| **Elm**                                       | `--` | `{- … -}` | ⃠ 🌳 |
| **Clojure**                                   | `;` | `#| … |#` | `#_` skips next form (read-time comment) 🌟 |
| **Common Lisp**                               | `;` | `#| … |#` | ⃠ 🌟 |
| **Emacs Lisp**                                | `;` | `#| … |#` | ⃠ 🌟 |
| **OCaml**                                     | ⃠ | `(* … *)` | Single-line comment just a one-line block 🐫 |
| **Erlang**                                    | `%` | ⃠ | ⃠ 🛡️ |
| **Elixir**                                    | `#` | `""" … """` (doc-strings) | Not a true comment 🧪 |
| **Prolog**                                    | `%` | `/* … */` | ⃠ 🧠 |
| **Ada**                                       | `--` | ⃠ | ⃠ ✈️ |
| **COBOL**                                     | `*` (column 1) or `>` (column 7) | ⃠ | ⃠ 🏦 |
| **Fortran (90+)**                             | `!` | ⃠ | ⃠ 🔢 |
| **Visual Basic / VB.NET**                     | `'` | ⃠ | ⃠ 📜 |
| **PowerShell**                                | `#` | `<# … #>` | ⃠ 💻 |
| **Racket**                                    | `;` | `#| … |#` | ⃠ 🎾 |
| **CoffeeScript**                              | `#` | `### … ###` | ⃠ ☕ |
| **Sass (SCSS syntax)**                        | `//` | `/* … */` | ⃠ 🎨 |
| **Sass (indented syntax)**                    | `//` | ⃠ | ⃠ 🎨 |
| **Less**                                      | `//` | `/* … */` | ⃠ 🎨 |
| **CSS**                                       | ⃠ | `/* … */` | No line comment 🎨 |
| **JSON**                                      | ⃠ | ⃠ | Pure JSON has no comments (JSON5 allows `//` / `/* */`) 📋 |
| **YAML**                                      | `#` | ⃠ | ⃠ 📋 |
| **INI / .properties**                         | `#` or `;` | ⃠ | ⃠ ⚙️ |
| **Markdown**                                  | ⃠ | `<!-- … -->` | ⃠ 📝 |
| **Asciidoc**                                  | `//` | `//// … ////` | ⃠ 📝 |
| **Dockerfile**                                | `#` | ⃠ | ⃠ 🐳 |
| **CMake**                                     | `#` | ⃠ | ⃠ 🛠️ |
| **Gherkin (Cucumber)**                        | `#` | ⃠ | ⃠ 🥒 |
| **GraphQL SDL**                               | `#` | ⃠ | ⃠ 🕸️ |
| **RPGLE**                                     | `*` (in comment spec) | ⃠ | ⃠ 🏦 |
| **ABAP**                                      | `*` (first column) | `"` (after code) | ⃠ 🏢 |
| **Batch (Windows .bat/.cmd)**                 | `REM` or `::` | ⃠ | `::` is a common hack 🖥️ |
| **Shell (POSIX sh, Bash, Zsh, Ksh, etc.)**    | `#` | ⃠ | Block comment hack: `: <<'EOF' … EOF` 🐚 |
| **Tcl**                                       | `#` | ⃠ | ⃠ 🛠️ |
| **Nim**                                       | `#` | `#[ … ]#` | Also supports multiple `#` lines 🦋 |
| **Julia**                                     | `#` | `#= … =#` | ⃠ 🔢 |
| **Haxe**                                      | `//` | `/* … */` | ⃠ 🌟 |
| **Crystal**                                   | `#` | `#` … `#` or `=begin … =end` | ⃠ 💎 |
| **Forth**                                     | `\` | `( … )` | `\` is line comment, `( … )` is block comment 🛠️ |
| **Groff / Troff**                             | `\"` | ⃠ | ⃠ 📜 |
| **MIPS Assembly**                             | `#` (some assemblers) | `/* … */` (some assemblers) | ⃠ 💻 |
| **PL/I**                                      | `/* … */` | ⃠ | No line comment 🏦 |
| **VHDL**                                      | `--` | ⃠ | ⃠ ⚡️ |
| **Verilog / SystemVerilog**                   | `//` | `/* … */` | ⃠ ⚡️ |
| **SML / OCaml**                               | `(* … *)` | `(* … *)` | ⃠ 🐫 |
| **Vala**                                      | `//` | `/* … */` | ⃠ 🌟 |

## How to Read the Table 📖

| Column | Meaning |
|:------:|:-------:|
| **Language / Family** | Name of the language or family grouping 🗂️ |
| **Single-line Comment** | Characters that comment out the rest of the current line ➡️ |
| **Multi-line / Block Comment** | Opening and closing delimiters that may span multiple lines 📑 |
| **Remarks / Variants** | Noteworthy details: alternative forms, documentation comments, nesting support, etc. ℹ️ |

This table is designed to render beautifully in GitHub, GitLab, Bitbucket, MkDocs, Jekyll, or any Markdown-aware platform. Copy and paste it directly into your Markdown files! If you need a language not listed, let me know, and I’ll add it! 😊
