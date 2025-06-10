# Personal Website

A minimalistic personal website inspired by university professor pages. Clean, academic styling with three main content sections: Blog, Art, and Readings.

## Features

- **Minimalistic Design**: Clean, academic styling 
- **Three Content Sections**:
  - **Blog**: Technical posts and thoughts
  - **Art**: Gallery for showcasing art pieces
  - **Readings**: Book and media recommendations with ratings
- **Easy Content Management**: Simple Python script for adding content
- **Responsive Design**: Works well on desktop and mobile
- **No Dependencies**: Pure HTML, CSS, and vanilla JavaScript

## Quick Start

1. **Clone or download** this repository to your web server or local development environment

2. **View the website**: Open `index.html` in a web browser or serve it with a simple HTTP server:
   ```bash
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

## Adding Content

Use the `post.py` script to easily add content to any section:

### Blog Posts

```bash
# Simple blog post
python post.py blog "My First Post" "This is the content of my blog post. It supports **markdown** formatting!"

# Blog post with images
python post.py blog "Data Visualization Guide" "
# Creating Better Data Visualizations

Here's my process for creating effective visualizations:

![Sample Chart](chart.png)

## Key Principles
- Keep it simple
- Use appropriate colors
- Tell a story with your data
" --images chart.png diagram.jpg

# Blog post with custom date
python post.py blog "Data Engineering Best Practices" "Here are some thoughts on data engineering..." --date "March 15, 2025"
```

**Enhanced Markdown Support**: The blog supports:
- Headers (`# ## ###`)
- **Bold** and *italic* text
- `inline code` and code blocks
- [Links](https://example.com)
- Lists with `- ` or `* `
- **Images**: `![alt text](image.png)` - automatically copied to assets/blog/
- Blockquotes with `>`
- Automatic image styling with shadows and responsive sizing

### Art Pieces

```bash
# Add an art piece with full details including artist
python post.py art "Sunset Landscape" "/path/to/image.jpg" "A peaceful sunset over the mountains captured during my trip to the Rocky Mountains. The interplay of light and shadow creates a dramatic atmosphere." --artist "John Smith" --medium "Oil on canvas" --dimensions "24x36 inches" --year "2024"

# Simple art piece
python post.py art "Digital Abstract" "artwork.png" "Experimenting with geometric forms and color theory" --artist "Jane Doe"

# Classic artwork reproduction
python post.py art "Starry Night" "starry-night.jpg" "Van Gogh's masterpiece depicting a swirling night sky over a village" --artist "Vincent van Gogh" --medium "Oil on canvas" --dimensions "73.7 cm × 92.1 cm" --year "1889"

# Art piece with custom date
python post.py art "Watercolor Study" "study.jpg" "Quick study of light on water" --artist "Local Artist" --medium "Watercolor" --date "February 20, 2025"
```

**New Features**:
- **Clickable Gallery**: Each art piece becomes a clickable tile leading to a detailed page
- **Individual Art Pages**: Dedicated pages with larger images and complete artwork information
- **Enhanced Details**: Support for artist name, dimensions, creation year, medium, and detailed descriptions
- **Professional Attribution**: Artist names are prominently displayed in both gallery and detail views

### Reading Recommendations

```bash
# Book recommendation with link
python post.py reading "Designing Data-Intensive Applications" "Martin Kleppmann" "Excellent deep dive into distributed systems and data architecture. Essential reading for any data engineer." --type "book" --rating 5 --link "https://dataintensive.net/"

# Movie recommendation with cover image
python post.py reading "Blade Runner 2049" "Denis Villeneuve" "Stunning visuals and thoughtful exploration of AI and humanity." --type "movie" --rating 4 --cover "/path/to/cover.jpg" --link "https://www.imdb.com/title/tt1856101/"

# YouTube video recommendation with embedded player
python post.py reading "Building Microservices" "Sam Newman" "Great talk on microservices architecture patterns and when to use them." --type "talk" --rating 5 --youtube "https://www.youtube.com/watch?v=wgdBVIX9ifA"

# Documentary with both link and YouTube
python post.py reading "AlphaGo" "Greg Kohs" "Fascinating look at AI beating humans at Go. Available on Netflix and YouTube." --type "documentary" --rating 5 --link "https://www.netflix.com/title/80190844" --youtube "dQw4w9WgXcQ"
```

**Enhanced Features**:
- **Web Links**: Add direct links to books, movies, articles, or any web content
- **YouTube Integration**: Embed YouTube videos directly in recommendations
- **Multiple Link Types**: Support both general web links and YouTube videos on the same item
- **Auto YouTube Detection**: Accepts full YouTube URLs or just video IDs

## Content Management Details

### File Structure

```
/
├── index.html              # Homepage
├── blog/                   # Blog section
│   └── index.html         # Blog listing
├── art/                   # Art section
│   └── index.html         # Art gallery
├── readings/              # Readings section
│   └── index.html         # Reading recommendations
├── assets/                # Static assets
│   ├── pfp/              # Profile pictures
│   ├── art/              # Art images (auto-created)
│   └── covers/           # Book/media covers (auto-created)
├── posts/                 # Markdown files (optional, for backup)
├── post.py               # Content management script
└── README.md             # This file
```

### How the Posting System Works

1. **Automatic File Management**: The script automatically:
   - Creates HTML files for blog posts
   - Copies images to appropriate asset directories
   - Updates index pages with new content
   - Handles markdown to HTML conversion

2. **Image Handling**: 
   - Art images are copied to `assets/art/`
   - Book/media covers are copied to `assets/covers/`
   - Original file names are preserved

3. **Content Updates**: Each section's index page is automatically updated with new content using JavaScript arrays

### Customization

#### Styling
- Edit the CSS in any HTML file to customize the appearance
- All sections use consistent styling variables for easy theming
- Responsive design works across devices

#### Content Structure
- Blog posts are stored as individual HTML files in `blog/`
- Art and reading data is stored in JavaScript arrays within their respective index files
- Easy to backup and version control

## Deployment

### Static Hosting (Recommended)
Perfect for static hosting services:
- **Netlify**: Drag and drop the entire folder
- **GitHub Pages**: Push to a GitHub repository and enable Pages
- **Vercel**: Connect your repository for automatic deploys
- **Amazon S3**: Upload files and configure for static website hosting

### Traditional Web Hosting
- Upload all files to your web server's public directory
- Ensure the web server can serve static HTML files
- No server-side processing required

### Local Development
```bash
# Python 3
python -m http.server 8000

# Node.js (if you have it)
npx serve .

# PHP (if available)
php -S localhost:8000
```

## Examples

### Complete Workflow Example

```bash
# Add a blog post about a new project
python post.py blog "Building a Data Pipeline with Apache Airflow" "
# Building a Data Pipeline with Apache Airflow

Today I want to share my experience building a robust data pipeline using Apache Airflow.

## Why Airflow?

- **Workflow Management**: DAG-based approach
- **Scheduling**: Built-in cron-like scheduling
- **Monitoring**: Web UI for pipeline visibility

## Key Lessons Learned

1. Start simple with basic operators
2. Use XComs sparingly
3. Design for idempotency

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def extract_data():
    # Your extraction logic here
    pass
```

The pipeline has been running successfully in production for 6 months now.
"

# Add an art piece
python post.py art "Data Visualization" "dataviz.png" "Interactive visualization of user engagement metrics" --medium "Digital art, D3.js"

# Add a book recommendation
python post.py reading "Clean Code" "Robert C. Martin" "Essential reading for any software developer. Changed how I think about writing maintainable code." --type "book" --rating 5
```

## Troubleshooting

### Common Issues

1. **Script not executable**: Run `chmod +x post.py`
2. **Images not displaying**: Check file paths and ensure images are copied to assets
3. **Content not updating**: Verify the script completed successfully and refresh the browser

### Getting Help

Check the script output for error messages:
```bash
python post.py blog "Test Post" "Test content"
```

Look for:
- ✅ Success messages
- ❌ Error messages with details

## License

This is a personal website template. Feel free to use and modify for your own personal website.

---

Built with ❤️ by Mihir Pratap Sah 