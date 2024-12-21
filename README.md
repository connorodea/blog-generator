# Blog Post Generator

Automatically generate SEO-optimized, location-specific blog posts using OpenAI's GPT-4.

## Setup

1. Clone this repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Copy `.env.template` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.template .env
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

## Usage

Generate a blog post:
```bash
python src/blog_generator.py --topic "Best Coffee Shops" --city "Portland"
```

Or run interactively:
```bash
python src/blog_generator.py
```

## Testing

Run tests:
```bash
pytest tests/
```

## Directory Structure

```
blog-generator/
├── .venv/
├── src/
│   └── blog_generator.py
├── tests/
│   └── test_blog_generator.py
├── posts/
│   └── # Generated blog posts will be saved here
├── config/
├── .env
└── README.md
```
