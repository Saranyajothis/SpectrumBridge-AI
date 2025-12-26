"""
Visual Generator Agent  
Generates autism-related educational images using LOCAL Stable Diffusion
- Runs on your Mac (CPU mode for reliability)
- Completely FREE and unlimited
- No black image issues
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import torch
from PIL import Image
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv

load_dotenv()

class VisualGenerator:
    """Generates educational images using local Stable Diffusion"""
    
    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5"):
        """Initialize Visual Generator"""
        print("Initializing Local Stable Diffusion...")
        print(f"Model: {model_id}")
        
        self.output_dir = Path(__file__).parent.parent / "output" / "generated_images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Use CPU to avoid MPS black image bug
        self.device = "cpu"
        print("✓ Using CPU (avoids black image issues)")
        
        # Load pipeline
        print("Loading model (first time: ~2GB download)...")
        
        hf_token = os.getenv("HF_TOKEN")
        
        try:
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32,  # CPU uses float32
                safety_checker=None,
                token=hf_token
            )
            
            self.pipeline = self.pipeline.to(self.device)
            self.pipeline.enable_attention_slicing()
            
            print("✓ Stable Diffusion ready!\n")
            self.model_loaded = True
            
        except Exception as e:
            print(f"✗ Model load failed: {e}")
            print("  Using placeholders...\n")
            self.model_loaded = False
    
    def _generate_with_sd(self, prompt: str) -> Optional[Image.Image]:
        """Generate image with local SD"""
        if not self.model_loaded:
            return None
        
        try:
            enhanced_prompt = f"{prompt}, high quality, professional, educational, detailed, vibrant"
            negative_prompt = "watermark, text, signature, blurry, ugly, low quality"
            
            with torch.no_grad():
                output = self.pipeline(
                    prompt=enhanced_prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=15,  # Fewer steps for CPU speed
                    guidance_scale=7.5,
                    height=512,
                    width=512
                )
            
            return output.images[0]
            
        except Exception as e:
            print(f"  SD failed: {e}")
            return None
    
    def _generate_placeholder(self, prompt: str, width: int = 512, height: int = 512) -> Image.Image:
        """Generate placeholder"""
        from PIL import ImageDraw, ImageFont
        
        image = Image.new('RGB', (width, height), color='#E8F4F8')
        draw = ImageDraw.Draw(image)
        
        for y in range(height):
            color_value = int(232 + (255 - 232) * (y / height))
            draw.line([(0, y), (width, y)], fill=(color_value, 244, 248))
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        words = prompt.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            try:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] > width - 80:
                    current_line.pop()
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            except:
                pass
        
        if current_line:
            lines.append(' '.join(current_line))
        
        y_offset = (height - len(lines) * 40) // 2
        for line in lines:
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, y_offset), line, fill='#2C5F7F', font=font)
                y_offset += 40
            except:
                pass
        
        watermark = "Educational Placeholder"
        try:
            bbox = draw.textbbox((0, 0), watermark, font=small_font)
            text_width = bbox[2] - bbox[0]
            draw.text(((width - text_width) // 2, height - 30), watermark, 
                     fill='#7FA8C0', font=small_font)
        except:
            pass
        
        return image
    
    def generate_image(self, prompt: str, filename: Optional[str] = None) -> Dict:
        """Generate image"""
        start_time = time.time()
        
        if self.model_loaded:
            print(f"  Generating with Stable Diffusion...")
            image = self._generate_with_sd(prompt)
            method = "stable_diffusion_local" if image else "placeholder"
        else:
            image = None
            method = "placeholder"
        
        if image is None:
            print(f"  Using placeholder...")
            image = self._generate_placeholder(prompt)
            method = "placeholder"
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')
            filename = f"{timestamp}_{safe_prompt}.png"
        
        if not filename.endswith('.png'):
            filename += '.png'
        
        image_path = self.output_dir / filename
        image.save(image_path, 'PNG', optimize=True)
        
        generation_time = time.time() - start_time
        
        return {
            'success': True,
            'image_path': str(image_path),
            'filename': filename,
            'prompt': prompt,
            'generation_time': round(generation_time, 2),
            'size': f"{image.width}x{image.height}",
            'method': method
        }
    
    def generate_batch(self, prompts: List[str]) -> List[Dict]:
        """Generate multiple images"""
        results = []
        start_time = time.time()
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}] {prompt[:50]}...")
            result = self.generate_image(prompt)
            results.append(result)
            print(f"✓ {result['generation_time']}s - {result['method']}")
        
        total_time = time.time() - start_time
        print(f"\n{'='*70}")
        print(f"Complete: {len(prompts)} images in {total_time:.2f}s")
        print(f"{'='*70}\n")
        
        return results
    
    def generate_autism_educational_images(self, topic: str = "general") -> List[Dict]:
        """Generate autism education images"""
        prompts = [
            "diverse children playing together in classroom",
            "happy child building with colorful blocks",
            "teacher helping student with cards",
            "children working on art project",
            "calm sensory-friendly classroom"
        ]
        return self.generate_batch(prompts)
    
    def list_generated_images(self) -> List[Dict]:
        """List generated images"""
        images = []
        for img_path in self.output_dir.glob("*.png"):
            stat = img_path.stat()
            images.append({
                'filename': img_path.name,
                'path': str(img_path),
                'size_mb': round(stat.st_size / (1024 * 1024), 2)
            })
        return images


if __name__ == "__main__":
    print("="*70)
    print("VISUAL GENERATOR - Local Stable Diffusion")
    print("="*70 + "\n")
    
    generator = VisualGenerator()
    
    if generator.model_loaded:
        print("\nGenerating test image (will take ~30-60s on CPU)...\n")
        result = generator.generate_image("happy child playing with blocks")
        print(f"\n✓ Done! Method: {result['method']}")
        print(f"  Time: {result['generation_time']}s")
        print(f"  Saved: {result['filename']}")
    else:
        print("Model not loaded - using placeholders")
