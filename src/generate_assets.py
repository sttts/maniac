"""Generate all pixel art assets via PixelLab API using concept art as style reference."""
import os
import sys
import json
import base64
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests

API_URL = "https://api.pixellab.ai"
API_KEY = os.environ.get("PIXELLAB_API_KEY", "27421c38-b9dc-4094-be53-80073c9b1677")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BG_DIR = os.path.join(ASSETS_DIR, "backgrounds")
SPRITE_DIR = os.path.join(ASSETS_DIR, "sprites")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images")


def ensure_dirs():
    os.makedirs(BG_DIR, exist_ok=True)
    os.makedirs(SPRITE_DIR, exist_ok=True)


def load_image_base64(path, max_size=256):
    """Load an image file, resize if needed, and return base64 string."""
    from PIL import Image
    import io

    img = Image.open(path)
    # Resize large images to keep payload small
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def save_image(b64_data, output_path):
    """Save base64 image data to file."""
    img_data = base64.b64decode(b64_data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"  Saved: {output_path} ({len(img_data)} bytes)")


def api_call(endpoint, payload, retries=2):
    """Make API call with retries."""
    url = f"{API_URL}{endpoint}"
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, headers=HEADERS, json=payload, timeout=120)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait = 10 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            else:
                print(f"  Error {resp.status_code}: {resp.text[:200]}")
                if attempt < retries:
                    time.sleep(5)
                    continue
                return None
        except requests.exceptions.Timeout:
            print(f"  Timeout on attempt {attempt + 1}")
            if attempt < retries:
                time.sleep(5)
                continue
            return None
        except (requests.exceptions.ConnectionError, requests.exceptions.ProxyError) as e:
            print(f"  Connection error on attempt {attempt + 1}: {e.__class__.__name__}")
            if attempt < retries:
                time.sleep(10)
                continue
            return None
    return None


def generate_background(description, filename, width=128, height=128,
                        style_image_path=None):
    """Generate a background image using PixFlux."""
    print(f"\nGenerating background: {filename}")
    print(f"  Prompt: {description[:80]}...")

    payload = {
        "description": description,
        "image_size": {"width": width, "height": height},
        "text_guidance_scale": 7.0,
    }

    # Add style reference if provided
    if style_image_path and os.path.exists(style_image_path):
        payload["color_image"] = {
            "type": "base64",
            "base64": load_image_base64(style_image_path),
        }

    result = api_call("/v1/generate-image-pixflux", payload)
    if result and "image" in result:
        output_path = os.path.join(BG_DIR, filename)
        save_image(result["image"]["base64"], output_path)
        return output_path
    else:
        print(f"  FAILED to generate {filename}")
        return None


def convert_to_pixelart(input_path, output_filename, width=160, height=100):
    """Convert a concept art image to pixel art at target resolution."""
    print(f"\nConverting to pixel art: {output_filename}")

    payload = {
        "image": {
            "type": "base64",
            "base64": load_image_base64(input_path),
        },
        "image_size": {"width": width, "height": height},
    }

    result = api_call("/v1/image-to-pixelart", payload)
    if result and "image" in result:
        output_path = os.path.join(BG_DIR, output_filename)
        save_image(result["image"]["base64"], output_path)
        return output_path
    else:
        print(f"  FAILED to convert {output_filename}")
        # Try via generate instead
        return None


def generate_character_sprite(description, filename, width=32, height=48):
    """Generate a single character sprite."""
    print(f"\nGenerating sprite: {filename}")

    payload = {
        "description": description,
        "image_size": {"width": width, "height": height},
        "text_guidance_scale": 8.0,
        "no_background": True,
    }

    result = api_call("/v1/generate-image-pixflux", payload)
    if result and "image" in result:
        output_path = os.path.join(SPRITE_DIR, filename)
        save_image(result["image"]["base64"], output_path)
        return output_path
    else:
        print(f"  FAILED to generate sprite {filename}")
        return None


def animate_character(reference_path, action, filename, n_frames=4,
                      width=32, height=48):
    """Generate animation frames for a character."""
    print(f"\nAnimating: {action} -> {filename}")

    payload = {
        "description": "man with glasses, gray-brown hair, beard, blue hoodie, "
                       "gray t-shirt, dark pants, brown shoes, pixel art game character, "
                       "SCUMM adventure game style, 3/4 perspective",
        "action": action,
        "reference_image": {
            "type": "base64",
            "base64": load_image_base64(reference_path),
        },
        "image_size": {"width": width, "height": height},
        "n_frames": n_frames,
        "view": "side",
        "direction": "right",
    }

    result = api_call("/v1/animate-with-text", payload)
    if result and "images" in result:
        paths = []
        for i, img in enumerate(result["images"]):
            frame_path = os.path.join(SPRITE_DIR, f"{filename}_{i:02d}.png")
            save_image(img["base64"], frame_path)
            paths.append(frame_path)
        return paths
    else:
        print(f"  FAILED to animate {filename}")
        return None


def generate_backgrounds_only():
    """Generate only the missing background assets from concept art."""
    ensure_dirs()

    living_room_ref = os.path.join(IMAGES_DIR, "b6ccc902-4e0b-4d5e-b703-ac734926361a.png")
    computer_ref = os.path.join(IMAGES_DIR, "00831472-58fc-4d50-aedd-e1879db96acb.png")
    switch_ref = os.path.join(IMAGES_DIR, "cf2d3ab8-f1d2-47b1-919d-60013e3402d5.png")
    crt_ref = os.path.join(IMAGES_DIR, "3e4618d1-e45c-4da8-8d94-698fc62c1d1c.png")

    print("=" * 60)
    print("Generating backgrounds from concept art")
    print("=" * 60)

    concept_backgrounds = {
        "living_room.png": (
            "pixel art SCUMM adventure game room interior, cozy living room, "
            "dark blue wallpaper, wooden staircase on left side, brown couch, "
            "floor lamp, framed pictures on wall (iceland landscape, lambda symbol), "
            "patterned carpet on floor, door on right side, warm lighting, "
            "Maniac Mansion LucasArts style, 16-bit retro pixel art, "
            "detailed interior scene with furniture and decorations",
            living_room_ref,
        ),
        "computer_room.png": (
            "pixel art SCUMM adventure game computer room, dark blue walls, "
            "wooden desk with CRT monitor and keyboard, microphone on desk, "
            "office chair, bookshelf with books, model airplane on stand, "
            "posters on wall, cables and wires, dim room lighting, "
            "Maniac Mansion LucasArts style, 16-bit retro pixel art, "
            "detailed room with 1990s computer setup",
            computer_ref,
        ),
        "switch_closeup.png": (
            "pixel art close-up of computer power switch, large toggle switch "
            "in center, gray computer case metal panel, ON/OFF label, "
            "small LED indicator light, visible screws and ventilation slots, "
            "Maniac Mansion LucasArts SCUMM style, 16-bit pixel art, "
            "detailed close-up mechanical switch view",
            switch_ref,
        ),
        "crt_inside.png": (
            "pixel art view from inside a CRT monitor looking out, "
            "circuit boards and electronic components on left and right sides, "
            "green PCB with capacitors resistors and chips visible, "
            "cables and wires, rounded CRT screen opening in center, "
            "Maniac Mansion LucasArts style, 16-bit retro pixel art, "
            "detailed electronics inside vintage computer monitor",
            crt_ref,
        ),
    }

    for filename, (prompt, ref_path) in concept_backgrounds.items():
        generate_background(prompt, filename, width=160, height=100, style_image_path=ref_path)


def main():
    ensure_dirs()

    # Concept art files for style reference
    living_room_ref = os.path.join(IMAGES_DIR, "b6ccc902-4e0b-4d5e-b703-ac734926361a.png")
    computer_ref = os.path.join(IMAGES_DIR, "00831472-58fc-4d50-aedd-e1879db96acb.png")
    switch_ref = os.path.join(IMAGES_DIR, "cf2d3ab8-f1d2-47b1-919d-60013e3402d5.png")
    crt_ref = os.path.join(IMAGES_DIR, "3e4618d1-e45c-4da8-8d94-698fc62c1d1c.png")

    # ── Step 1: Generate all backgrounds ──
    print("=" * 60)
    print("STEP 1: Generating all backgrounds")
    print("=" * 60)

    # Backgrounds generated from concept art as style reference
    concept_backgrounds = {
        "living_room.png": (
            "pixel art SCUMM adventure game room interior, cozy living room, "
            "dark blue wallpaper, wooden staircase on left side, brown couch, "
            "floor lamp, framed pictures on wall (iceland landscape, lambda symbol), "
            "patterned carpet on floor, door on right side, warm lighting, "
            "Maniac Mansion LucasArts style, 16-bit retro pixel art, "
            "detailed interior scene with furniture and decorations",
            living_room_ref,
        ),
        "computer_room.png": (
            "pixel art SCUMM adventure game computer room, dark blue walls, "
            "wooden desk with CRT monitor and keyboard, microphone on desk, "
            "office chair, bookshelf with books, model airplane on stand, "
            "posters on wall, cables and wires, dim room lighting, "
            "Maniac Mansion LucasArts style, 16-bit retro pixel art, "
            "detailed room with 1990s computer setup",
            computer_ref,
        ),
        "switch_closeup.png": (
            "pixel art close-up of computer power switch, large toggle switch "
            "in center, gray computer case metal panel, ON/OFF label, "
            "small LED indicator light, visible screws and ventilation slots, "
            "Maniac Mansion LucasArts SCUMM style, 16-bit pixel art, "
            "detailed close-up mechanical switch view",
            switch_ref,
        ),
        "crt_inside.png": (
            "pixel art view from inside a CRT monitor looking out, "
            "circuit boards and electronic components on left and right sides, "
            "green PCB with capacitors resistors and chips visible, "
            "cables and wires, rounded CRT screen opening in center, "
            "Maniac Mansion LucasArts style, 16-bit retro pixel art, "
            "detailed electronics inside vintage computer monitor",
            crt_ref,
        ),
    }

    for filename, (prompt, ref_path) in concept_backgrounds.items():
        generate_background(prompt, filename, width=160, height=100, style_image_path=ref_path)

    # Additional backgrounds (CRT-based screens)
    bg_prompts = {
        "dos_boot.png": (
            "retro CRT computer monitor showing MS-DOS boot screen, "
            "black screen with white text, command prompt C:\\>, "
            "pixel art style, SCUMM adventure game, 16-bit, "
            "monitor bezel visible, scanlines on screen"
        ),
        "flight_sim.png": (
            "retro CRT monitor showing a top-down flight simulator game, "
            "blue ocean with green islands, small white airplane sprite, "
            "pixel art style, 16-bit DOS game screenshot, "
            "HUD with score display, monitor bezel frame"
        ),
        "rec_screen.png": (
            "retro CRT monitor showing recording software screen, "
            "black background with large red REC text and blinking dot, "
            "VU meter bars green yellow red, pixel art style, "
            "16-bit, monitor bezel frame"
        ),
    }

    for filename, prompt in bg_prompts.items():
        generate_background(prompt, filename, width=160, height=100, style_image_path=living_room_ref)

    # ── Step 2: Generate Stefan character sprites ──
    print("\n" + "=" * 60)
    print("STEP 2: Generating Stefan character sprites")
    print("=" * 60)

    stefan_desc = (
        "pixel art game character, man with glasses, gray-brown hair, "
        "short beard, wearing blue zip-up hoodie over gray t-shirt, "
        "dark pants, brown shoes, 3/4 perspective view facing right, "
        "Maniac Mansion SCUMM adventure game style, 16-bit pixel art, "
        "standing pose"
    )

    stefan_stand = generate_character_sprite(stefan_desc, "stefan_stand.png", width=32, height=48)

    # ── Step 3: Generate walk animation + pose variants ──
    if stefan_stand:
        print("\n" + "=" * 60)
        print("STEP 3: Generating walk animation + poses")
        print("=" * 60)

        # Walk animation at 64x64 (API minimum for animate-with-text)
        animate_character(stefan_stand, "walking right", "stefan_walk", n_frames=4, width=64, height=64)

        generate_character_sprite(
            stefan_desc.replace("standing pose", "sitting on a chair pose, side view"),
            "stefan_sit.png", width=32, height=48,
        )
        generate_character_sprite(
            stefan_desc.replace("standing pose", "waving right hand raised, friendly wave"),
            "stefan_wave.png", width=32, height=48,
        )

    print("\n" + "=" * 60)
    print("DONE! Generated assets in:", ASSETS_DIR)
    print("=" * 60)

    # List generated files
    for dirpath, _, filenames in os.walk(ASSETS_DIR):
        for f in sorted(filenames):
            if f.endswith(".png"):
                fpath = os.path.join(dirpath, f)
                size = os.path.getsize(fpath)
                rel = os.path.relpath(fpath, PROJECT_ROOT)
                print(f"  {rel} ({size} bytes)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--backgrounds":
        generate_backgrounds_only()
    else:
        main()
