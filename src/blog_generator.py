import os
from openai import OpenAI
import argparse
from typing import Optional
import json
import time
from datetime import datetime

def setup_client() -> OpenAI:
    """Initialize OpenAI client with error handling."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)

def generate_blog_post(
    topic: str,
    city: str,
    client: OpenAI,
    max_retries: int = 3,
    temperature: float = 0.7
) -> Optional[str]:
    """
    Generate an SEO-optimized blog post using OpenAI's API.
    
    Args:
        topic: Main topic of the blog post
        city: Target city for localization
        client: OpenAI client instance
        max_retries: Maximum number of retry attempts
        temperature: Creativity level (0.0 to 1.0)
    
    Returns:
        Generated blog post text or None if all retries fail
    """
    system_prompt = """You are an expert content writer specializing in local, SEO-optimized blog posts.
    Focus on providing valuable, actionable information while naturally incorporating local references."""
    
    user_prompt = f"""Write a detailed, SEO-optimized blog post about '{topic}' specifically for {city} residents.
    Include:
    - A compelling headline
    - Local landmarks and references
    - Practical, actionable tips
    - Relevant local statistics or data
    - A clear conclusion with a call to action
    
    Format the post with proper HTML heading tags and paragraphs."""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",  # You can modify this to use different models
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=4000
            )
            
            # Extract the content from the response
            content = response.choices[0].message.content
            
            # Save the generated content
            save_blog_post(topic, city, content)
            
            return content

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Max retries reached. Please try again later.")
                return None

def save_blog_post(topic: str, city: str, content: str) -> None:
    """Save the generated blog post to a file with metadata."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"blog_post_{timestamp}.html"
    
    # Create a posts directory if it doesn't exist
    os.makedirs("posts", exist_ok=True)
    
    metadata = {
        "topic": topic,
        "city": city,
        "generated_at": timestamp,
    }
    
    with open(f"posts/{filename}", "w", encoding="utf-8") as f:
        f.write("<!-- Metadata:\n")
        f.write(json.dumps(metadata, indent=2))
        f.write("\n-->\n\n")
        f.write(content)
    
    print(f"\nBlog post saved to: posts/{filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate a localized, SEO-optimized blog post")
    parser.add_argument("--topic", type=str, help="Blog post topic")
    parser.add_argument("--city", type=str, help="Target city")
    parser.add_argument("--temperature", type=float, default=0.7, help="Creativity level (0.0 to 1.0)")
    
    args = parser.parse_args()
    
    # If arguments aren't provided, prompt for them
    topic = args.topic or input("Enter your topic: ")
    city = args.city or input("Enter your city: ")
    
    try:
        client = setup_client()
        blog_post = generate_blog_post(
            topic=topic,
            city=city,
            client=client,
            temperature=args.temperature
        )
        
        if blog_post:
            print("\nBlog post generated successfully!")
            print("\nPreview of the first 200 characters:")
            print("-" * 50)
            print(blog_post[:200] + "...")
            print("-" * 50)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
