#!/usr/bin/env python3
"""
Seam Carving Simplified CLI
===========================
Usage: python cli_auto.py <image_path>
"""

import sys
import os
from pathlib import Path
from resizer import ContentAwareResizer

def display_banner():
    """Display application banner."""
    print("""
╔═══════════════════════════════════════════════╗
║    CONTENT-AWARE IMAGE RESIZER                ║
║    Simplified Matrix-based Seam Carving       ║
╚═══════════════════════════════════════════════╝
    """)

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python cli_auto.py <image_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    display_banner()

    print(f"\n📁 Loading image: {input_path}")
    
    try:
        resizer = ContentAwareResizer(image_path=input_path)
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        sys.exit(1)
    
    orig_h, orig_w = resizer.original.shape[:2]
    print(f"✓ Image loaded: {orig_w} × {orig_h}")
    
    # Automatic reduction of 20%
    target_w = int(orig_w * 0.8)
    target_h = orig_h
    print(f"\n🤖 Automatic mode: 20% width reduction")
    print(f"   {orig_w} → {target_w} pixels")
    print(f"🎯 Target: {target_w} × {target_h}")
    
    # Create result directory
    result_dir = Path("result")
    result_dir.mkdir(exist_ok=True)
    
    # Resize
    try:
        resizer.resize(target_w, target_h, verbose=True)
    except Exception as e:
        print(f"❌ Error during resizing: {e}")
        sys.exit(1)
    
    # Save result in the result folder
    input_file = Path(input_path)
    output_filename = f"{input_file.stem}_modified{input_file.suffix}"
    output_path = result_dir / output_filename
    
    resizer.save_result(str(output_path))
    
    # Statistics
    stats = resizer.get_statistics()
    print(f"\n📈 Statistics:")
    print(f"   Total time: {stats['total_time']:.2f}s")
    print(f"   Avg per seam: {stats['average_time_per_seam']*1000:.1f}ms")
    
    print(f"\n✅ Done! Result saved to: {output_path}")

if __name__ == '__main__':
    main()
