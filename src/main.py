print ("hello world")
# python
from textnode import TextNode, TextType
import sys
import os
import shutil
from mrkdwn_to_html import markdown_to_html_node
from extract_title import extract_title
def copy_static_to_docs(src_dir: str = "static", dst_dir: str = "docs") -> None:
    """
    Recursively copy contents of src_dir into dst_dir.
    Before copying, delete dst_dir if it exists to ensure a clean copy.
    """

    # 1. Zmaž cieľový adresár, ak existuje
    if os.path.exists(dst_dir):
        print(f"Removing existing destination directory: {dst_dir}")
        shutil.rmtree(dst_dir)

    # 2. Vytvor prázdny cieľový adresár
    os.mkdir(dst_dir)
    print(f"Created destination directory: {dst_dir}")

    # 3. Rekurzívna pomocná funkcia
    def _copy_dir(src: str, dst: str) -> None:
        for name in os.listdir(src):
            src_path = os.path.join(src, name)
            dst_path = os.path.join(dst, name)

            if os.path.isdir(src_path):
                # je to adresár → vytvor ho a rekurzívne kopíruj ďalej
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)
                    print(f"Created directory: {dst_path}")
                _copy_dir(src_path, dst_path)
            else:
                # je to súbor → skopíruj
                shutil.copy2(src_path, dst_path)
                print(f"Copied file: {src_path} -> {dst_path}")

    # spustenie rekurzie z koreňa
    _copy_dir(src_dir, dst_dir)
def generate_page(from_path, template_path, dest_path, basepath):
    # with open(from_path, "r") as f:
    #     markdown_content = f.read()
    """
    Generate a single HTML page from a markdown file and a template.

    - from_path: path to markdown file (e.g. 'content/index.md')
    - template_path: path to template HTML file (e.g. 'template.html')
    - dest_path: destination HTML path (e.g. 'public/index.html')
    """
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    # 1. Prečítaj markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # 2. Prečítaj HTML šablónu
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 3. Markdown -> HTML string
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    # 4. Získaj titulok z markdownu
    title = extract_title(markdown)

    # 5. Nahraď placeholdery v šablóne
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')


    # 6. Uisti sa, že cieľový adresár existuje
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        print(f"Created destination directory for page: {dest_dir}")

    # 7. Zapíš výsledný HTML súbor
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Wrote page to {dest_path}")
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    os.makedirs(dest_dir_path, exist_ok=True)

    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(entry_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, new_dest_dir, basepath)

        elif os.path.isfile(entry_path) and entry.endswith(".md"):
            name_without_ext, _ = os.path.splitext(entry)
            dest_file_name = name_without_ext + ".html"
            dest_file_path = os.path.join(dest_dir_path, dest_file_name)

            generate_page(entry_path, template_path, dest_file_path, basepath)

            # zavoláme už existujúcu funkciu
            generate_page(entry_path, template_path, dest_file_path, basepath)
def main():
    # a = TextNode("hi", TextType.TEXT, None)
    # b = TextNode("hi", TextType.TEXT, None)
    # c = TextNode("hi", TextType.LINK, "https://x.com")

    copy_static_to_docs("static", "docs")
    #
    # generate_page(
    #     from_path="content/index.md",
    #     template_path="template.html",
    #     dest_path="public/index.html",
    # )


    content_dir = "content"
    template_path = "template.html"
    docs_dir = "docs"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    # ak máš niekde funkciu na vymazanie public/, nechaj ju tu
    # clear_public_dir(public_dir)  # len ak ju Boot.dev zadal skôr

    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)
    # print(a)        # TextNode(hi, text, None)
    # print(a == b)   # True
    # print(a == c)   # False
    # print(a == 5)   # False (via NotImplemented)

if __name__ == "__main__":
    main()
