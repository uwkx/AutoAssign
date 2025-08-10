import flet as ft
import subprocess
import os

userFtaPath = os.path.join(os.getcwd(), "AutoAssignHelper.exe")

fileTypes = {
    "Text": [".txt", ".log", ".md", ".diz", ".lst", ".nfo", ".ini", ".csv", ".cfg", ".json", ".xml", ".properties", ".conf", ".sh", ".yml", ".yaml"],
    "Code": [".c", ".cpp", ".cc", ".cxx", ".h", ".hh", ".hpp", ".hxx", ".ino", ".cs", ".vb", ".java", ".class", ".scala", ".kt", ".kts", ".groovy", ".py", ".pyw", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".rb", ".go", ".rs", ".swift", ".php", ".phtml", ".html", ".htm", ".xhtml", ".css", ".scss", ".sass", ".less", ".xml", ".xsd", ".json", ".jsonc", ".toml", ".yaml", ".yml", ".lua", ".sql", ".psql", ".pl", ".pm", ".r", ".Rmd", ".sh", ".bash", ".zsh", ".ksh", ".fish", ".bat", ".cmd", ".ps1", ".m", ".mm", ".asm", ".s", ".v", ".vh", ".vhd", ".vhdl", ".sv", ".svh", ".dart", ".erl", ".ex", ".exs", ".el", ".lisp", ".clj", ".cljs", ".edn", ".fs", ".fsi", ".fsx", ".fsscript", ".ml", ".mli", ".re", ".res", ".nim", ".d", ".cr", ".tscn", ".gd", ".cue", ".hx", ".hxsl", ".nix", ".build", ".gradle", ".bazel", ".bzl", ".WORKSPACE", ".gyp", ".gypi", ".cmake", ".make", ".mak", ".mk", ".Dockerfile", ".env", ".cfg", ".ini", ".conf", ".config", ".props", ".targets", ".csproj", ".vbproj", ".sln", ".vcxproj" ".tsx", ".vue", ".svelte", ".astro", ".njk", ".liquid", ".zig"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v", ".3gp", ".3g2", ".ts", ".mts", ".m2ts", ".divx", ".vob", ".rm", ".rmvb", ".ogv", ".asf", ".f4v", ".f4p", ".f4a", ".f4b"],
    "Photos": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif", ".raw", ".cr2", ".nef", ".arw", ".orf", ".sr2", ".dng", ".psd", ".svg", ".ico", ".jfif", ".avif"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".alac", ".aiff", ".opus"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".rtf", ".txt", ".csv", ".md", ".pages", ".key", ".numbers"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".pfb"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".cab", ".arj", ".lzma", ".z"],
    "EBooks": [".epub", ".mobi", ".azw", ".azw3", ".fb2", ".pdf", ".lit"],
    "3D Models": [".obj", ".fbx", ".stl", ".dae", ".3ds", ".blend", ".dwg", ".dxf", ".max", ".skp"],
    "Backup Files": [".bak", ".tmp", ".old", ".backup", ".sav"],
    "Game Files": [".pak", ".wad", ".bsp", ".vpk", ".iso", ".sav", ".mod", ".gam", ".rom", ".nes", ".sfc", ".gba", ".iso"],
    "System Files": [".sys", ".dll", ".drv", ".efi", ".bin", ".dat", ".log"],
    "Web Development": [".html", ".css", ".js", ".ts", ".jsx", ".tsx", ".json", ".xml", ".svg", ".php", ".vue", ".scss"],
    "Data Files": [".db", ".sqlite", ".sqlite3", ".mdb", ".accdb", ".csv", ".tsv", ".dat", ".json", ".xml"],
    "Code Build Files": [".csproj", ".sln", ".makefile", ".gradle", ".pom.xml", ".babelrc", ".eslintrc", ".prettierrc"]
}


def appSelector(page: ft.Page):
    exe_path = None
    selected_app_path = ft.Text("No app selected", color="grey")
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    page.title = "Auto Assign"
    page.scroll = "AUTO"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    checkboxes = {}
    extension_column = ft.Column()
    select_all_button = ft.ElevatedButton("Select All")

    file_type_dropdown = ft.Dropdown(
        label="Select File Type Category",
        options=[ft.dropdown.Option(key, key) for key in fileTypes.keys()],
        width=300
    )

    # Toggle logic for Select/Deselect All
    def toggle_select_all(e):
        all_selected = all(chk.value for chk in checkboxes.values())
        for chk in checkboxes.values():
            chk.value = not all_selected
        select_all_button.text = "Deselect All" if not all_selected else "Select All"
        page.update()

    select_all_button.on_click = toggle_select_all

    def on_file_type_change(e):
        selected_group = file_type_dropdown.value
        extension_column.controls.clear()
        checkboxes.clear()

        if selected_group:
            extensions = fileTypes[selected_group]
            num_per_column = 10
            columns = []

            for i in range(0, len(extensions), num_per_column):
                col_controls = []
                for ext in extensions[i:i+num_per_column]:
                    chk = ft.Checkbox(label=ext)
                    checkboxes[ext] = chk
                    col_controls.append(chk)
                columns.append(ft.Column(col_controls, spacing=5))

            checkbox_row = ft.Row(controls=columns, alignment=ft.MainAxisAlignment.START)
            extension_column.controls.append(select_all_button)
            extension_column.controls.append(checkbox_row)

        page.update()



    file_type_dropdown.on_change = on_file_type_change

    def browse_app(e):
        def on_dialog_result(result):
            nonlocal exe_path
            if result and result.files:
                exe_path = result.files[0].path
                selected_app_path.value = f"Selected: {os.path.basename(exe_path)}"
                selected_app_path.color = None
                page.update()

        file_picker.on_result = on_dialog_result
        file_picker.pick_files(
            dialog_title="Select an EXE",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["exe"]
        )

    def apply_defaults(e):
        if not os.path.isfile(userFtaPath):
            dialog = ft.AlertDialog(
                title=ft.Text("Verify App installation"),
                content=ft.Text("SetUserFTA.exe was not found."),
            )
            page.open(dialog)
            page.update()
            return

        if not exe_path:
            dialog = ft.AlertDialog(
                title=ft.Text("Please select an app"),
                content=ft.Text("Browse and select an app first."),
            )
            page.open(dialog)
            page.update()
            return

        selected_exts = [ext for ext, chk in checkboxes.items() if chk.value]
        if not selected_exts:
            dialog = ft.AlertDialog(
                title=ft.Text("Please select an extension"),
                content=ft.Text("Select at least one extension to set a default app."),
            )
            page.open(dialog)
            page.update()
            return

        prog_id = f"Applications\\{os.path.basename(exe_path)}"
        results = []

        for ext in selected_exts:
            cmd = f'"{userFtaPath}" {ext} {prog_id}'
            try:
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                results.append(f"{ext} → {prog_id}: SUCCESS")
            except subprocess.CalledProcessError as e:
                results.append(f"{ext} → {prog_id}: FAILED\n{e.stderr}")

        result_text = "\n".join(results)
        dialog = ft.AlertDialog(
            title=ft.Text("Results"),
            content=ft.Text(result_text),
        )
        page.open(dialog)
        page.update()

    #layout
    page.add(ft.Text("Select File Types to Assign:", size=30, weight=ft.FontWeight.BOLD))
    page.add(file_type_dropdown)
    page.add(extension_column)

    page.add(
        ft.Row([
            ft.ElevatedButton("Browse for an App (EXE)", on_click=browse_app),
            selected_app_path,
        ], alignment=ft.MainAxisAlignment.START)
    )

    page.add(
        ft.ElevatedButton("Apply Defaults", on_click=apply_defaults)
    )

    page.update()

ft.app(appSelector)
