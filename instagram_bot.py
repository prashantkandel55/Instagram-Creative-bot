from instagrapi import Client
from PIL import Image, ImageDraw
import os
from dotenv import load_dotenv
import random
import schedule
import time
from datetime import datetime

# Load environment variables
load_dotenv()

INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

def generate_art(size=(1080, 1080)):
    """Generate a colorful abstract art piece"""
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Generate base colors
    primary_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
    
    # Draw multiple overlapping shapes
    for _ in range(20):
        # Create variations of the primary color
        color = (
            (primary_color[0] + random.randint(-50, 50)) % 255,
            (primary_color[1] + random.randint(-50, 50)) % 255,
            (primary_color[2] + random.randint(-50, 50)) % 255
        )
        
        # Random shape selection
        shape = random.choice(['circle', 'rectangle', 'line'])
        
        if shape == 'circle':
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            radius = random.randint(50, 300)
            draw.ellipse(
                [x-radius, y-radius, x+radius, y+radius],
                fill=color,
                outline=None
            )
        elif shape == 'rectangle':
            x1 = random.randint(0, size[0])
            y1 = random.randint(0, size[1])
            x2 = x1 + random.randint(100, 400)
            y2 = y1 + random.randint(100, 400)
            draw.rectangle([x1, y1, x2, y2], fill=color)
        else:  # line
            x1 = random.randint(0, size[0])
            y1 = random.randint(0, size[1])
            x2 = random.randint(0, size[0])
            y2 = random.randint(0, size[1])
            draw.line([x1, y1, x2, y2], fill=color, width=random.randint(5, 20))
    
    return image

def generate_profile_picture(size=(400, 400)):
    """Generate a smaller, simpler art piece for profile picture"""
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Create a distinctive pattern for profile
    color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
    
    # Draw a centered design
    center = (size[0]//2, size[1]//2)
    for i in range(8):
        radius = 150 - (i * 20)
        color_mod = (
            (color[0] + i * 20) % 255,
            (color[1] + i * 20) % 255,
            (color[2] + i * 20) % 255
        )
        draw.ellipse(
            [center[0]-radius, center[1]-radius, 
             center[0]+radius, center[1]+radius],
            fill=color_mod
        )
    
    return image

def post_content():
    """Generate and post art, occasionally update profile picture"""
    instagram = Client()
    try:
        # Login to Instagram
        instagram.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        print(f"Logged in successfully as {INSTAGRAM_USERNAME}")
        
        # Generate and save main post
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        post_filename = f"art_{timestamp}.jpg"
        art = generate_art()
        art.save(post_filename)
        
        # Post the art
        caption = """🎨 Daily Generated Art
.
.
.
#GenerativeArt #AbstractArt #DigitalArt #ArtOfTheDay #AbstractArtwork #ModernArt"""
        instagram.photo_upload(post_filename, caption)
        print(f"Posted new artwork: {timestamp}")
        
        # Update profile picture occasionally (every 10th post)
        if random.randint(1, 10) == 1:
            profile_filename = f"profile_{timestamp}.jpg"
            profile_art = generate_profile_picture()
            profile_art.save(profile_filename)
            
            instagram.account_change_picture(profile_filename)
            print("Updated profile picture")
            
            # Clean up profile picture file
            if os.path.exists(profile_filename):
                os.remove(profile_filename)
        
        # Clean up post file
        if os.path.exists(post_filename):
            os.remove(post_filename)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
def test_connection():
    """Test Instagram connection and post a single image"""
    instagram = Client()
    try:
        # Test login
        print("Testing Instagram connection...")
        instagram.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        print("Successfully logged in!")
        
        # Generate and post test image
        print("Generating test image...")
        test_filename = "test_art.jpg"
        art = generate_art()
        art.save(test_filename)
        
        # Post test image
        caption = "🎨 Test Post - Generated Art\n#GenerativeArt #Test"
        instagram.photo_upload(test_filename, caption)
        print("Successfully posted test image!")
        
        # Clean up
        if os.path.exists(test_filename):
            os.remove(test_filename)
            
    except Exception as e:
        print(f"Error during test: {str(e)}")

def main():
    """Main function to run the bot"""
    # Run initial test
    print("Running initial test...")
    test_connection()
    
    # Schedule regular posts
    schedule.every(5).minutes.do(post_content)
    
    print("\nBot started! Will post every 30 minutes...")
    print("Press Ctrl+C to stop the bot")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()