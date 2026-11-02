# Skin retouch add-on (Colour + B&W presets)

These settings use Lightroom's **People** masks. Lightroom finds the faces and skin on each photo automatically, so the retouch adapts to every image. Add them once to each preset and save. The steps work in Lightroom desktop/Classic and Lightroom mobile.

## Mask settings

### 1. Skin smoothing: People → **Face Skin + Body Skin** (one mask)
| Setting | Colour preset | B&W preset |
|---|---|---|
| Texture | **−40** | **−40** |
| Clarity | −12 | −10 |
| Sharpness | −15 | −15 |
| Exposure | +0.05 | +0.05 |
| Saturation | −5 (calms redness) | — |
| Highlights | −5 | −5 |

Strength guide:
- **Light** (men, close-ups at f/1.8): Texture −25, Clarity −5
- **Standard** (above)
- **Strong** (heavy makeup, harsh light): Texture −60, Clarity −20

### 2. Eyes: People → **Iris and Pupil**
Exposure +0.20 · Clarity +15 · Saturation +10 (colour only)

### 3. Whites of eyes: People → **Eye Sclera**
Exposure +0.15 · Saturation −20

### 4. Teeth: People → **Teeth**
Exposure +0.15 · Saturation −30 (colour only)

### 5. Lips (optional, colour only): People → **Lips**
Saturation +5 · Exposure +0.05

## Saving the retouch into each preset

### Lightroom desktop / Classic
1. Open a portrait and apply **Bright Clean Wedding** (or the B&W preset).
2. Open **Masking → People**, wait for the person to be detected, select **All People** (or the person), tick **Face Skin + Body Skin**, then **Create Mask**. Enter the skin settings above.
3. Repeat for Iris & Pupil, Eye Sclera, Teeth and Lips, each as its own mask.
4. Click **+** in the Presets panel → **Create Preset**. Use the same name as before with ` + Retouch` added.
   - Tick **Masking** and all the develop groups. Untick **White Balance**.
5. Do the same with the B&W preset (skip the colour-only settings).

### Lightroom mobile
1. Apply the preset to a portrait, then tap **Masking → +** → **People** → select the person.
2. Tick **Face Skin + Body Skin** → **Create** and set the sliders above. Add the other masks the same way.
3. Tap **⋯ → Create Preset**, tick **Masking** and untick White Balance, then save as `… + Retouch`.

## Tips
- With several people in the photo, choose **All People** before you save the preset so everyone gets retouched.
- The masks only smooth skin. Use the **Healing / Remove** tool for spots and stray hairs.
- For magazine-level skin on close-ups, finish in Photoshop with frequency separation or Portraiture.
