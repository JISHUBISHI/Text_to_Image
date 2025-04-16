from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import time
from huggingface_hub import InferenceClient
import requests

# Load environment variables
load_dotenv()

# Set your Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def generate_image(prompt, timeout=60):  # Increased timeout to 60 seconds
    """
    Generate an image using Hugging Face's inference API
    with a specified timeout in seconds.
    """
    try:
        # Initialize the Hugging Face client
        client = InferenceClient(token=HUGGINGFACEHUB_API_TOKEN)
        
        # Start timer
        start_time = time.time()

        # Generate the image using Stable Diffusion with retry mechanism
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                image = client.text_to_image(
                    prompt=prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0",
                    parameters={
                        "num_inference_steps": 20,  # Reduced steps for faster generation
                        "guidance_scale": 7.5
                    }
                )
                break
            except requests.exceptions.Timeout:
                retry_count += 1
                if retry_count == max_retries:
                    raise TimeoutError("Maximum retries reached")
                print(f"Retry {retry_count}/{max_retries}...")
                time.sleep(5)  # Wait before retrying

        # Check if timeout was exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(f"Image generation took longer than {timeout} seconds")

        return image

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    prompt = "A beautiful sunset over mountains, high quality, detailed"
    result = generate_image(prompt)
    if result:
        print("Image generated successfully!")
        # Save the image
        result.save("generated_image.png")
        print("Image saved as generated_image.png") 