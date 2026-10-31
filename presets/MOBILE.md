# Bright Clean Wedding: Lightroom mobile

## Option A: install from the DNG (recommended)

1. Send `BrightClean_Wedding_Mobile.dng` to your phone (AirDrop, Google Drive, WhatsApp *as a document*, etc.).
2. Lightroom mobile → **+** (Add photos) → **From Files** → pick the DNG.
3. Open it. It shows a grey card with colour swatches, with all the settings already applied.
4. Tap **⋯** (top right) → **Create Preset**.
   - Name: `Bright Clean Wedding`, Group: `Bright Clean`
   - **Uncheck White Balance**. Set WB on each photo yourself.
   - Leave everything else checked (Light, Color, Effects, Detail, Optics, Calibration, Curve)
   - Tap ✓
5. The preset is now under **Presets → Yours → Bright Clean**. If you're signed in to Lightroom, it also syncs to desktop.

## Option B: import the .xmp directly

Newer versions of Lightroom mobile may offer **Presets → ⋯ → Import Presets**. If yours does, pick `BrightClean_Wedding.xmp`. If you don't see that option, use Option A.

## Option C: enter the settings by hand (mobile panel order)

### Light
| Slider | Value |
|---|---|
| Exposure | **+0.70** (adjust per photo, +0.5 to +1.0) |
| Contrast | −12 |
| Highlights | −55 |
| Shadows | +35 |
| Whites | +20 |
| Blacks | −12 |

**Curve** (white channel): 0→0 · 60→56 · 128→136 · 192→204 · 255→251
**Curve** (blue channel): 0→0 · 64→68 · 255→255

### Color
| Slider | Value |
|---|---|
| Temp / Tint | Use the WB eyedropper on a white dress, then Temp **+5 to +10**, Tint **+4** |
| Vibrance | +10 |
| Saturation | −5 |

**Mix** (Hue / Saturation / Luminance)
| Colour | Hue | Sat | Lum |
|---|---|---|---|
| Red | 0 | +5 | +5 |
| Orange | −4 | −10 | +12 |
| Yellow | −10 | −30 | +20 |
| Green | +25 | −30 | +10 |
| Aqua | 0 | −15 | +10 |
| Blue | −5 | +5 | −10 |
| Purple | 0 | −10 | 0 |
| Magenta | 0 | 0 | +5 |

**Grading**
| Wheel | Hue | Sat |
|---|---|---|
| Shadows | 220 | 6 |
| Midtones | 35 | 4 |
| Highlights | 45 | 3 |
Blending 60 · Balance −20

### Effects
Texture −10 · Clarity −8 · Dehaze +4 · Vignette 0 · Grain 0

### Detail
Sharpening 40 · Radius 1.0 · Detail 25 · Masking 60 · Noise Reduction 10 · Color Noise Reduction 25

### Optics
Enable Lens Corrections ✓ · Remove Chromatic Aberration ✓

### Calibration
Red primary: Hue +5, Sat +8 · Green primary: Sat −8 · Blue primary: Hue −8, Sat +15

## Per-photo finishing on mobile
- **Masking → Select Subject**: Exposure +0.15
- **Masking → People → Face Skin**: Texture −25, Clarity −10
- Backlit windows: **Linear gradient** or **Select Sky** mask, Highlights −30
- Black & white frames: Profile **B&W**, Contrast +20, Whites +20, Blacks −20

---

# Bright Clean Wedding B&W

Files: `BrightClean_Wedding_BW.xmp` (desktop) · `BrightClean_Wedding_BW_Mobile.dng` (mobile)

Install it the same way as the colour version (Option A above). Name it `Bright Clean Wedding B&W` and uncheck White Balance.

### Manual settings
| Panel | Settings |
|---|---|
| Profile | **B&W** (Adobe Monochrome) |
| Light | Exposure **+0.60** · Contrast +20 · Highlights −50 · Shadows +25 · Whites +20 · Blacks −20 |
| Curve (white) | 0→0 · 60→52 · 128→134 · 192→208 · 255→252 |
| B&W Mix | Red +10 · Orange **+20** · Yellow +10 · Green −10 · Aqua −10 · Blue −15 · Purple 0 · Magenta +5 |
| Effects | Texture −5 · Clarity 0 · Dehaze +3 · Vignette 0 · Grain 0 |
| Detail / Optics | Same as the colour version |

**Tuning tips**
- **Orange** controls skin brightness. Raise it for brighter, smoother faces and lower it for more character.
- **Blue −15** makes navy outfits and window light read deeper, which separates them from the white dress.
- For a moodier frame like the veil shot in the reference set, use Contrast +30 and Blacks −30.
