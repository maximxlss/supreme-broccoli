from PIL import Image


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

hues = (0, 30/360, 45/360, 60/360, 75/360, 90/360, 120/360, 180/360, 210/360, 240/360, 270/360, 300/360)
colors = []

for v in (0, 0.4, 0.6, 1):
    for s in (0, 0.75, 1):
        for h in hues:
            (r, g, b) = hsv_to_rgb(h, s, v);
            (r, g, b) = (int(r), int(g), int(b))
            if (r, g, b) in colors: continue
            img = Image.new("RGB", (1, 1), color=(r, g, b))
            img.save(f"files/{rgb_to_hex((r, g, b))}.jpg")
            colors.append((r, g, b))
            print(f"Progress {r} {g} {b}", end="\r")

print(colors)

print("Finished             ")
