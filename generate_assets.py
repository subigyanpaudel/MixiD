#!/usr/bin/env python3
import os
import subprocess
from PIL import Image

def generate():
    sizes = [16, 32, 48, 64, 128, 256, 512]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(base_dir, 'Assets/logo/idlogo.svg')

    for s in sizes:
        d = os.path.join(base_dir, f'desktop/icons/hicolor/{s}x{s}/apps')
        os.makedirs(d, exist_ok=True)
        out_png = os.path.join(d, 'id-mixer.png')
        res = subprocess.run(['/snap/bin/inkscape', svg_path, '-o', out_png, '-w', str(s), '-h', str(s)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f'Error rendering {s}x{s}: {res.stderr}')
        else:
            print(f'Rendered {out_png} ({os.path.getsize(out_png)} bytes)')

    # Copy scalable svg
    sc_dir = os.path.join(base_dir, 'desktop/icons/hicolor/scalable/apps')
    os.makedirs(sc_dir, exist_ok=True)
    with open(svg_path, 'r') as src, open(os.path.join(sc_dir, 'id-mixer.svg'), 'w') as dst:
        dst.write(src.read())

    # Generate app_icon.h with RGBA arrays for 16, 32, 48, 64
    header_lines = [
        '// Generated application icon RGBA pixel arrays for GLFW',
        '#pragma once',
        '#include <GLFW/glfw3.h>',
        ''
    ]

    for s in [16, 32, 48, 64]:
        png_file = os.path.join(base_dir, f'desktop/icons/hicolor/{s}x{s}/apps/id-mixer.png')
        im = Image.open(png_file).convert('RGBA')
        raw_bytes = list(im.tobytes())
        header_lines.append(f'static const unsigned char icon_{s}_rgba[{len(raw_bytes)}] = {{')
        chunks = [', '.join(f'0x{b:02x}' for b in raw_bytes[i:i+16]) for i in range(0, len(raw_bytes), 16)]
        header_lines.append('    ' + ',\n    '.join(chunks))
        header_lines.append('};\n')

    header_lines.append('''inline void set_application_icon(GLFWwindow* window) {
    GLFWimage images[4];
    images[0].width = 16;
    images[0].height = 16;
    images[0].pixels = const_cast<unsigned char*>(icon_16_rgba);

    images[1].width = 32;
    images[1].height = 32;
    images[1].pixels = const_cast<unsigned char*>(icon_32_rgba);

    images[2].width = 48;
    images[2].height = 48;
    images[2].pixels = const_cast<unsigned char*>(icon_48_rgba);

    images[3].width = 64;
    images[3].height = 64;
    images[3].pixels = const_cast<unsigned char*>(icon_64_rgba);

    glfwSetWindowIcon(window, 4, images);
}
''')

    with open(os.path.join(base_dir, 'app_icon.h'), 'w') as f:
        f.write('\n'.join(header_lines))
    print('Generated app_icon.h successfully!')

if __name__ == '__main__':
    generate()
