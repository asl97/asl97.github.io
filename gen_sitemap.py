#!/usr/bin/env python3
"""
Generate a static sitemap.html from json_index.json
This is a Python-powered static site generator for the sitemap,
based on the existing JavaScript implementation in sitemap_js.html
"""

import json
import os
import html

def create_icon_html(name, icon):
    """Create HTML for an icon item (folder or file)"""
    escaped_name = html.escape(name)
    return f'''
                <div class="item">
                    <div class="icon">{icon}</div>
                    <span>{escaped_name}</span>
                </div>'''

def create_folder_html(folder_name, folder_path):
    """Create HTML for a folder link"""
    escaped_name = html.escape(folder_name)
    # Create the hash path
    hash_path = folder_path + folder_name + '/'

    return f'''
                <a href="./index.html#{hash_path}" style="cursor: pointer;">
                    <div class="item">
                        <div class="icon">📁</div>
                        <span>{escaped_name}</span>
                    </div>
                </a>
'''.lstrip("\n")

def create_file_html(file_name, folder_path):
    """Create HTML for a file link"""
    escaped_name = html.escape(file_name)
    file_path = folder_path + file_name

    return f'''
                <a href="{html.escape(file_path)}">
                    <div class="item">
                        <div class="icon">📄</div>
                        <span>{escaped_name}</span>
                    </div>
                </a>
'''.lstrip("\n")

def render_folder_html(dirs, files, folder_path):
    """Render all folders and files for a given path"""
    html_content = ''
    
    # Add folders first
    for folder in dirs:
        html_content += create_folder_html(folder, folder_path)

    # Add files
    for file in files:
        html_content += create_file_html(file, folder_path)
    return html_content.rstrip()

def generate_sitemap():
    """Generate the static sitemap.html file"""
    
    # Read json_index.json
    if not os.path.exists('json_index.json'):
        print("Error: json_index.json not found. Run index_dirfiles_to_json.py first.")
        return False
    
    with open('json_index.json', 'r') as f:
        index_data = json.load(f)
    
    # Build the folders HTML
    folders_content = ''
    
    for folder_path, (dirs, files) in index_data.items():
        # Create main content div
        items_html = render_folder_html(dirs, files, folder_path + '/')
        
        escaped_path = html.escape(folder_path)
        folders_content += f'''
            <label>{escaped_path}</label>
            <div class="main">
{items_html}
            </div>
'''

    folders_content = folders_content.strip("\n")

    # Create the complete HTML file
    html_template = f'''<html>
    <head>
        <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
        <meta content="utf-8" http-equiv="encoding">
        <style>
            a {{
                color: inherit;
                text-decoration: none;
            }}

            #main, .main {{
                display: flex;
                gap: 1vh 1vw;
            }}

            #folders {{
                display: grid;
                grid-template-columns: 10vw auto;
                grid-row-gap: 2px;
                padding: 10px;
            }}

            #folders > label, #folders > .main {{
                border: 2px solid black;
                padding: 10px;
            }}

            #folders > .main {{
                border-left: none;
            }}

            #folders > label {{
                font-size: min(2vw, 2vh);
                border-right: none;
                align-content: center;
            }}

            .item {{
                place-items: center;
                display: grid;
                border: gray solid 2px;
                padding: 1vh 1vw;
            }}
 
            .icon {{
                font-size: 5vw;
            }}
        </style>
    </head>
    <body>
        <div id="folders">
{folders_content}
        </div>
    </body>
</html>
'''

    # Write the sitemap.html file
    with open('sitemap.html', 'w') as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_sitemap()
