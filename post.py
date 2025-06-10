#!/usr/bin/env python3
"""
Personal Website Content Manager
Simple script to add blog posts, art pieces, and reading recommendations

Usage:
    python post.py blog "Title" "Content here..."
    python post.py art "Title" "path/to/image.jpg" "Description" --medium "Oil on canvas"
    python post.py reading "Book Title" "Author" "My thoughts..." --type "book" --rating 5
"""

import os
import sys
import json
import datetime
import argparse
import re
from pathlib import Path

def get_current_date():
    """Get current date in readable format."""
    return datetime.datetime.now().strftime('%B %d, %Y')

def sanitize_filename(title):
    """Convert title to safe filename."""
    # Remove special characters and replace spaces with hyphens
    filename = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    filename = re.sub(r'\s+', '-', filename.strip())
    return filename.lower()

def simple_md_to_html(markdown_text):
    """Convert basic markdown to HTML."""
    html = markdown_text
    
    # Convert headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Convert code blocks
    html = re.sub(r'```(.*?)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert images - ![alt text](image_path)
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" class="blog-image">', html)
    
    # Convert bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Convert links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Convert paragraphs
    paragraphs = []
    current_para = []
    in_list = False
    in_code_block = False
    
    for line in html.split('\n'):
        if line.startswith('<pre>') or in_code_block:
            if '</pre>' in line:
                in_code_block = False
            else:
                in_code_block = True
            paragraphs.append(line)
            continue
            
        if line.startswith('<h'):
            if current_para:
                paragraphs.append('<p>' + '<br>'.join(current_para) + '</p>')
                current_para = []
            paragraphs.append(line)
        elif line.strip().startswith(('- ', '* ')):
            if not in_list:
                in_list = True
                if current_para:
                    paragraphs.append('<p>' + '<br>'.join(current_para) + '</p>')
                    current_para = []
                paragraphs.append('<ul>')
            line = re.sub(r'^[*-] (.*?)$', r'<li>\1</li>', line.strip())
            paragraphs.append(line)
        elif line.strip() == '' and in_list:
            paragraphs.append('</ul>')
            in_list = False
        elif line.strip() == '':
            if current_para:
                paragraphs.append('<p>' + '<br>'.join(current_para) + '</p>')
                current_para = []
        else:
            current_para.append(line)
    
    if current_para:
        paragraphs.append('<p>' + '<br>'.join(current_para) + '</p>')
    
    if in_list:
        paragraphs.append('</ul>')
    
    return '\n'.join(paragraphs)

def create_blog_post(title, content, date=None, images=None):
    """Create a new blog post."""
    if date is None:
        date = get_current_date()
    
    filename = sanitize_filename(title) + '.html'
    filepath = Path('blog') / filename
    
    # Handle image copying if images are provided
    if images:
        import shutil
        os.makedirs('assets/blog', exist_ok=True)
        for img_path in images:
            if os.path.exists(img_path):
                img_filename = Path(img_path).name
                dest_path = Path('assets/blog') / img_filename
                shutil.copy2(img_path, dest_path)
                # Update content to use the new path
                content = content.replace(img_path, f"../assets/blog/{img_filename}")
    
    # Convert markdown to HTML
    html_content = simple_md_to_html(content)
    
    # Generate HTML page
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Mihir Pratap Sah</title>
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            max-width: 800px;
            margin: 40px auto;
            background-color: white;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .header {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2em;
            font-weight: normal;
            color: #2c3e50;
        }}
        
        .post-meta {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 30px;
        }}
        
        .content {{
            margin-bottom: 50px;
        }}
        
        .content h1, .content h2, .content h3 {{
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        .content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .content pre {{
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            border: 1px solid #e0e0e0;
        }}
        
        .content code {{
            font-family: 'Courier New', monospace;
            background-color: #f8f8f8;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        
        .content pre code {{
            background: none;
            padding: 0;
        }}
        
                 .content a {{
             color: #3498db;
             text-decoration: none;
         }}
         
         .content a:hover {{
             text-decoration: underline;
         }}
         
         .blog-image {{
             max-width: 100%;
             height: auto;
             margin: 20px 0;
             border-radius: 4px;
             box-shadow: 0 2px 8px rgba(0,0,0,0.1);
             display: block;
         }}
         
         .content ul, .content ol {{
             margin-bottom: 15px;
             padding-left: 30px;
         }}
         
         .content blockquote {{
             border-left: 4px solid #3498db;
             margin: 20px 0;
             padding: 10px 20px;
             background-color: #f8f9fa;
             font-style: italic;
         }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.85em;
            color: #666;
            text-align: center;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #3498db;
            text-decoration: none;
            font-size: 0.95em;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <a href="../" class="back-link">← Back to Home</a>
    
    <div class="header">
        <h1>{title}</h1>
        <div class="post-meta">Posted on {date}</div>
    </div>

    <div class="content">
        {html_content}
    </div>

    <div class="footer">
        <p>&copy; 2025 Mihir Pratap Sah</p>
    </div>
</body>
</html>'''
    
    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    # Update blog index
    update_blog_index(title, filename, date, content[:150] + '...' if len(content) > 150 else content)
    
    print(f"✅ Blog post created: {filepath}")
    return filepath

def update_blog_index(title, filename, date, excerpt):
    """Update the blog index page with new post."""
    index_path = Path('blog/index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create new blog post data
    new_post = f'''            {{
                title: "{title}",
                filename: "{filename}",
                date: "{date}",
                excerpt: "{excerpt.replace('"', '\\"')}"
            }}'''
    
    # Find existing posts array and add to it
    if 'const posts = [];' in content:
        # Empty array - replace with first item
        posts_data = f'''        const posts = [
{new_post}
        ];'''
        updated_content = re.sub(r'const posts = \[\];', posts_data, content)
    else:
        # Find the end of the existing array and add new item
        pattern = r'(const posts = \[.*?)(\s*\]\s*;)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            before_closing = match.group(1)
            closing = match.group(2)
            # Add comma and new item before closing bracket
            updated_content = content.replace(match.group(0), 
                                            f"{before_closing},\n{new_post}\n        {closing}")
        else:
            print("Warning: Could not find posts array to update")
            return
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def create_art_piece(title, image_path, description, medium=None, date=None, dimensions=None, year=None, artist=None):
    """Add a new art piece."""
    if date is None:
        date = get_current_date()
    
    # Copy image to assets if it's not already there
    if not image_path.startswith('assets/'):
        # Copy image to assets directory
        import shutil
        os.makedirs('assets/art', exist_ok=True)
        filename = Path(image_path).name
        dest_path = Path('assets/art') / filename
        shutil.copy2(image_path, dest_path)
        image_path = str(dest_path)
    
    # Create individual art page
    art_page_filename = sanitize_filename(title) + '.html'
    create_art_detail_page(title, image_path, description, medium, date, dimensions, year, art_page_filename, artist)
    
    # Update art index
    update_art_index(title, image_path, description, date, medium, art_page_filename, artist)
    
    print(f"✅ Art piece added: {title}")
    if artist:
        print(f"   Artist: {artist}")
    print(f"   Image: {image_path}")
    print(f"   Detail page: art/{art_page_filename}")

def create_art_detail_page(title, image_path, description, medium, date, dimensions, year, filename, artist=None):
    """Create a detailed page for an art piece."""
    filepath = Path('art') / filename
    
    # Adjust image path for the art subdirectory
    display_image_path = f"../{image_path}"
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Mihir Pratap Sah</title>
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            max-width: 1000px;
            margin: 40px auto;
            background-color: white;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .header {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2em;
            font-weight: normal;
            color: #2c3e50;
        }}
        
        .art-container {{
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 40px;
            margin-bottom: 40px;
        }}
        
        .art-image-container {{
            text-align: center;
        }}
        
        .art-image {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        
        .art-details {{
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        
        .detail-item {{
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px dotted #ddd;
        }}
        
        .detail-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}
        
        .detail-label {{
            font-weight: 600;
            color: #2c3e50;
            display: block;
            margin-bottom: 5px;
        }}
        
        .detail-value {{
            color: #555;
        }}
        
        .description {{
            margin-top: 30px;
            font-size: 1.05em;
            line-height: 1.7;
            text-align: justify;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #3498db;
            text-decoration: none;
            font-size: 0.95em;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.85em;
            color: #666;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .art-container {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <a href="./" class="back-link">← Back to Art Gallery</a>
    
    <div class="header">
        <h1>{title}</h1>
    </div>
    
    <div class="art-container">
        <div class="art-image-container">
            <img src="{display_image_path}" alt="{title}" class="art-image">
        </div>
        
        <div class="art-details">
            {f'<div class="detail-item"><span class="detail-label">Artist</span><span class="detail-value">{artist}</span></div>' if artist else ''}
            
            <div class="detail-item">
                <span class="detail-label">Created</span>
                <span class="detail-value">{year or date}</span>
            </div>
            
            {f'<div class="detail-item"><span class="detail-label">Medium</span><span class="detail-value">{medium}</span></div>' if medium else ''}
            
            {f'<div class="detail-item"><span class="detail-label">Dimensions</span><span class="detail-value">{dimensions}</span></div>' if dimensions else ''}
            
            <div class="detail-item">
                <span class="detail-label">Added to Gallery</span>
                <span class="detail-value">{date}</span>
            </div>
        </div>
    </div>
    
    <div class="description">
        <p>{description}</p>
    </div>
    
    <div class="footer">
        <p>&copy; 2025 Mihir Pratap Sah</p>
    </div>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)

def update_art_index(title, image_path, description, date, medium=None, art_page_filename=None, artist=None):
    """Update the art index page with new piece."""
    index_path = Path('art/index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create new art piece data
    new_art_piece = f'''            {{
                title: "{title}",
                image: "../{image_path}",
                description: "{description.replace('"', '\\"')}",
                date: "{date}",
                medium: "{medium or ''}",
                artist: "{artist or ''}",
                pageUrl: "{art_page_filename}"
            }}'''
    
    # Find existing artPieces array and add to it
    if 'const artPieces = [];' in content:
        # Empty array - replace with first item
        art_data = f'''        const artPieces = [
{new_art_piece}
        ];'''
        updated_content = re.sub(r'const artPieces = \[\];', art_data, content)
    else:
        # Find the end of the existing array and add new item
        pattern = r'(const artPieces = \[.*?)(\s*\]\s*;)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            before_closing = match.group(1)
            closing = match.group(2)
            # Add comma and new item before closing bracket
            updated_content = content.replace(match.group(0), 
                                            f"{before_closing},\n{new_art_piece}\n        {closing}")
        else:
            print("Warning: Could not find artPieces array to update")
            return
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def create_reading_recommendation(title, author, description, reading_type="book", rating=None, cover_image=None, date=None, link=None, youtube_id=None):
    """Add a new reading recommendation."""
    if date is None:
        date = get_current_date()
    
    # Handle cover image if provided
    if cover_image and not cover_image.startswith('assets/'):
        import shutil
        os.makedirs('assets/covers', exist_ok=True)
        filename = Path(cover_image).name
        dest_path = Path('assets/covers') / filename
        shutil.copy2(cover_image, dest_path)
        cover_image = str(dest_path)
    
    # Extract YouTube ID from URL if full URL is provided
    if youtube_id and 'youtube.com/watch?v=' in youtube_id:
        youtube_id = youtube_id.split('v=')[1].split('&')[0]
    elif youtube_id and 'youtu.be/' in youtube_id:
        youtube_id = youtube_id.split('youtu.be/')[1].split('?')[0]
    
    # Update readings index
    update_readings_index(title, author, description, reading_type, date, rating, cover_image, link, youtube_id)
    
    print(f"✅ Reading recommendation added: {title}")
    if link:
        print(f"   Link: {link}")
    if youtube_id:
        print(f"   YouTube: https://youtube.com/watch?v={youtube_id}")

def update_readings_index(title, author, description, reading_type, date, rating=None, cover_image=None, link=None, youtube_id=None):
    """Update the readings index page with new recommendation."""
    index_path = Path('readings/index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create new reading data
    cover_path = f"../{cover_image}" if cover_image else None
    new_reading = f'''            {{
                title: "{title}",
                author: "{author}",
                description: "{description.replace('"', '\\"')}",
                type: "{reading_type}",
                date: "{date}",
                rating: {rating if rating else 'null'},
                cover: {f'"{cover_path}"' if cover_path else 'null'},
                link: {f'"{link}"' if link else 'null'},
                youtubeId: {f'"{youtube_id}"' if youtube_id else 'null'}
            }}'''
    
    # Find existing readings array and add to it
    if 'const readings = [];' in content:
        # Empty array - replace with first item
        reading_data = f'''        const readings = [
{new_reading}
        ];'''
        updated_content = re.sub(r'const readings = \[\];', reading_data, content)
    else:
        # Find the end of the existing array and add new item
        pattern = r'(const readings = \[.*?)(\s*\]\s*;)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            before_closing = match.group(1)
            closing = match.group(2)
            # Add comma and new item before closing bracket
            updated_content = content.replace(match.group(0), 
                                            f"{before_closing},\n{new_reading}\n        {closing}")
        else:
            print("Warning: Could not find readings array to update")
            return
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def main():
    parser = argparse.ArgumentParser(description='Personal Website Content Manager')
    subparsers = parser.add_subparsers(dest='command', help='Content type to add')
    
    # Blog command
    blog_parser = subparsers.add_parser('blog', help='Add a blog post')
    blog_parser.add_argument('title', help='Blog post title')
    blog_parser.add_argument('content', help='Blog post content (supports markdown)')
    blog_parser.add_argument('--date', help='Custom date (default: today)')
    blog_parser.add_argument('--images', nargs='*', help='Paths to images to include in the post')
    
    # Art command
    art_parser = subparsers.add_parser('art', help='Add an art piece')
    art_parser.add_argument('title', help='Art piece title')
    art_parser.add_argument('image', help='Path to image file')
    art_parser.add_argument('description', help='Art piece description')
    art_parser.add_argument('--artist', help='Artist name')
    art_parser.add_argument('--medium', help='Art medium (e.g., "Oil on canvas")')
    art_parser.add_argument('--dimensions', help='Dimensions (e.g., "24x36 inches")')
    art_parser.add_argument('--year', help='Year created')
    art_parser.add_argument('--date', help='Custom date (default: today)')
    
    # Reading command
    reading_parser = subparsers.add_parser('reading', help='Add a reading recommendation')
    reading_parser.add_argument('title', help='Book/media title')
    reading_parser.add_argument('author', help='Author/creator name')
    reading_parser.add_argument('description', help='Your thoughts/review')
    reading_parser.add_argument('--type', default='book', help='Type: book, movie, documentary, etc.')
    reading_parser.add_argument('--rating', type=int, choices=range(1, 6), help='Rating (1-5 stars)')
    reading_parser.add_argument('--cover', help='Path to cover image')
    reading_parser.add_argument('--link', help='Web link (URL)')
    reading_parser.add_argument('--youtube', help='YouTube URL or video ID')
    reading_parser.add_argument('--date', help='Custom date (default: today)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'blog':
            create_blog_post(args.title, args.content, args.date, args.images)
        elif args.command == 'art':
            create_art_piece(args.title, args.image, args.description, args.medium, args.date, args.dimensions, args.year, args.artist)
        elif args.command == 'reading':
            create_reading_recommendation(
                args.title, args.author, args.description,
                args.type, args.rating, args.cover, args.date, args.link, args.youtube
            )
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 