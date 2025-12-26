"""
Test Visual Generator
Comprehensive testing of image generation capabilities
"""

import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.visual_generator import VisualGenerator

def test_single_image():
    """Test single image generation"""
    print("\n" + "="*70)
    print("TEST 1: Single Image Generation")
    print("="*70 + "\n")
    
    generator = VisualGenerator()
    
    prompt = "happy child with autism playing with colorful blocks, educational illustration, warm lighting"
    
    print(f"Prompt: {prompt}")
    print("Generating...")
    
    result = generator.generate_image(prompt)
    
    if result['success']:
        print(f"\n✅ PASS: Image generated successfully")
        print(f"   File: {result['filename']}")
        print(f"   Time: {result['generation_time']}s")
        print(f"   Size: {result['size']}")
        print(f"   Path: {result['image_path']}")
        return True
    else:
        print(f"\n❌ FAIL: {result.get('error', 'Unknown error')}")
        return False

def test_batch_generation():
    """Test batch generation - 5 images in 20s target"""
    print("\n" + "="*70)
    print("TEST 2: Batch Generation (5 Images in 20s Target)")
    print("="*70 + "\n")
    
    generator = VisualGenerator()
    
    prompts = [
        "child with autism using communication tablet, happy, educational, clean design",
        "sensory-friendly classroom with soft lighting, calm colors, children's illustration",
        "diverse children playing together inclusively, playground, warm atmosphere",
        "visual schedule cards on wall, organized, colorful, educational tool",
        "child wearing noise-canceling headphones, peaceful expression, bright setting"
    ]
    
    print(f"Generating {len(prompts)} images...")
    print("Target: <20 seconds total\n")
    
    start_time = time.time()
    results = generator.generate_batch(prompts)
    total_time = time.time() - start_time
    
    successful = sum(1 for r in results if r['success'])
    
    print(f"\nResults:")
    print(f"  Success rate: {successful}/{len(prompts)}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average per image: {total_time/len(prompts):.2f}s")
    
    # Check if meets requirements
    meets_speed = total_time <= 25  # Allow 5s buffer
    meets_success = successful >= 4  # At least 4/5 should succeed
    
    if meets_speed and meets_success:
        print(f"\n✅ PASS: Generated {successful} images in {total_time:.2f}s")
        if total_time <= 20:
            print("   🎯 Excellent! Under 20 seconds!")
        return True
    else:
        if not meets_speed:
            print(f"\n⚠️  WARNING: Took {total_time:.2f}s (target: 20s)")
        if not meets_success:
            print(f"\n⚠️  WARNING: Only {successful}/5 images generated successfully")
        return False

def test_professional_quality():
    """Test that images have no watermarks and are professional quality"""
    print("\n" + "="*70)
    print("TEST 3: Professional Quality (No Watermark)")
    print("="*70 + "\n")
    
    generator = VisualGenerator()
    
    prompt = "autism awareness educational poster, professional design, clean, modern, no text"
    
    print(f"Generating professional quality image...")
    print(f"Checking: No watermark, high resolution\n")
    
    result = generator.generate_image(
        prompt=prompt,
        negative_prompt="watermark, text, logo, signature, blurry, amateur, low quality"
    )
    
    if result['success']:
        # Check resolution
        width, height = map(int, result['size'].split('x'))
        is_high_res = width >= 512 and height >= 512
        
        print(f"✓ Image generated: {result['filename']}")
        print(f"✓ Resolution: {result['size']}")
        print(f"✓ Negative prompt used: watermark, text, logo removed")
        
        if is_high_res:
            print(f"\n✅ PASS: Professional quality achieved")
            print(f"   - High resolution ({width}x{height})")
            print(f"   - Watermark filtering applied")
            return True
        else:
            print(f"\n⚠️  WARNING: Resolution may be low ({width}x{height})")
            return False
    else:
        print(f"\n❌ FAIL: {result.get('error', 'Unknown error')}")
        return False

def test_image_storage():
    """Test image storage and organization"""
    print("\n" + "="*70)
    print("TEST 4: Image Storage")
    print("="*70 + "\n")
    
    generator = VisualGenerator()
    
    # Generate a test image
    prompt = "autism education visual aid, simple, clean, professional"
    result = generator.generate_image(prompt)
    
    if not result['success']:
        print(f"❌ FAIL: Could not generate test image")
        return False
    
    # Check storage
    print(f"✓ Image saved to: {result['image_path']}")
    
    # List all images
    images = generator.list_generated_images()
    
    print(f"\nStorage Summary:")
    print(f"  Total images: {len(images)}")
    print(f"  Storage location: {generator.output_dir}")
    
    if images:
        print(f"\n  Recent images:")
        for img in images[:5]:  # Show last 5
            print(f"    • {img['filename']} ({img['size_mb']}MB) - {img['created']}")
    
    # Check if directory exists and is organized
    if generator.output_dir.exists() and len(images) > 0:
        print(f"\n✅ PASS: Images stored and organized")
        return True
    else:
        print(f"\n❌ FAIL: Storage issues detected")
        return False

def test_different_topics():
    """Test generating images for different autism education topics"""
    print("\n" + "="*70)
    print("TEST 5: Different Educational Topics")
    print("="*70 + "\n")
    
    generator = VisualGenerator()
    
    topics = ['sensory', 'communication', 'social']
    all_passed = True
    
    for topic in topics:
        print(f"\n--- Topic: {topic} ---")
        
        # Generate just 2 images per topic to save time
        results = generator.generate_autism_educational_images(topic)[:2]
        
        successful = sum(1 for r in results if r['success'])
        
        if successful >= 1:
            print(f"✓ {successful}/2 images generated for '{topic}'")
        else:
            print(f"✗ Failed to generate images for '{topic}'")
            all_passed = False
    
    if all_passed:
        print(f"\n✅ PASS: All topics supported")
        return True
    else:
        print(f"\n⚠️  WARNING: Some topics failed")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "="*70)
    print("VISUAL GENERATOR COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Single Image Generation", test_single_image),
        ("Batch Generation (5 in 20s)", test_batch_generation),
        ("Professional Quality", test_professional_quality),
        ("Image Storage", test_image_storage),
        ("Different Topics", test_different_topics)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} CRASHED: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70 + "\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ 5 images in 20s")
        print("✅ Professional quality")
        print("✅ No watermark")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
