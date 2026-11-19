#!/usr/bin/env python3
"""Layout verifier: re-runs the renderer with ImageDraw instrumented, then
reports every text run's bbox, overlaps between runs, and margin violations."""
import importlib.util, sys
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location("rend", "render.py")
rend = importlib.util.module_from_spec(spec)
sys.modules["rend"] = rend
spec.loader.exec_module(rend)

runs = []
_zones = []

orig_text = ImageDraw.ImageDraw.text
orig_rect = ImageDraw.ImageDraw.rectangle


def text(self, xy, s, *a, **kw):
    f = kw.get("font")
    if f is not None and s:
        bb = f.getbbox(s)
        runs.append(dict(text=str(s)[:60], x=xy[0], y=xy[1],
                         box=(xy[0] + bb[0], xy[1] + bb[1], xy[0] + bb[2], xy[1] + bb[3]),
                         fill=kw.get("fill"), size=getattr(f, "size", None)))
    return orig_text(self, xy, s, *a, **kw)


def rect(self, xy, *a, **kw):
    _zones.append((tuple(xy), kw.get("fill")))
    return orig_rect(self, xy, *a, **kw)


ImageDraw.ImageDraw.text = text
ImageDraw.ImageDraw.rectangle = rect
rend.main()
ImageDraw.ImageDraw.text = orig_text
ImageDraw.ImageDraw.rectangle = orig_rect

print("text runs:", len(runs))
W = H = 1024
M = 24
viol = [r for r in runs if r["box"][0] < M - 4 or r["box"][2] > W - M + 4
        or r["box"][1] < 0 or r["box"][3] > H - 2]
print("\n-- margin/edge violations:", len(viol))
for r in viol:
    print("   %-8s %-24s box=%s" % (r["fill"], r["text"][:34], tuple(int(v) for v in r["box"])))


def overlap(a, b):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ox = min(ax1, bx1) - max(ax0, bx0)
    oy = min(ay1, by1) - max(ay0, by0)
    return ox, oy


print("\n-- text/text overlaps (>=2px both axes):")
seen = set()
n = 0
for i in range(len(runs)):
    for j in range(i + 1, len(runs)):
        ox, oy = overlap(runs[i]["box"], runs[j]["box"])
        if ox >= 2 and oy >= 2:
            key = (runs[i]["text"], runs[j]["text"])
            if key in seen:
                continue
            seen.add(key)
            n += 1
            if n <= 40:
                print("   %-30r x %-30r  ox=%d oy=%d" % (runs[i]["text"][:28], runs[j]["text"][:28], ox, oy))
print("   total overlapping pairs:", n)

print("\n-- vertical extents by band:")
for lo, hi, name in [(0, 62, "topbar/masthead"), (62, 146, "date"), (146, 202, "numbers"),
                     (202, 512, "leads"), (512, 886, "briefs"), (886, 1024, "footer")]:
    band = [r for r in runs if r["box"][1] >= lo and r["box"][1] < hi]
    if band:
        top = min(r["box"][1] for r in band)
        bot = max(r["box"][3] for r in band)
        print("   %-16s runs=%3d  y=%0.1f..%0.1f" % (name, len(band), top, bot))
