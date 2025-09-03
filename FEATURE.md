# md2conf Image Formatting Issue Report

## Issue Summary
The md2conf library produces inconsistent image rendering in Confluence pages. Standard Markdown image syntax results in oversized, non-responsive images that overflow containers, while HTML img tags with explicit dimensions render correctly with responsive behavior.

## Problem Analysis

### Current Behavior
1. **Standard Markdown Images**: `![alt](src)` → Images overflow, not responsive
2. **HTML img (no dimensions)**: `<img src="...">` → Clickable but not responsive  
3. **HTML img (width only)**: `<img width="700" src="...">` → Partially responsive
4. **HTML img (width + height)**: `<img width="700" height="400" src="...">` → ✅ **Works correctly**

### Root Cause
Analysis of the generated Confluence HTML reveals the issue:

**Non-working output (Markdown → Confluence):**
```html
<img class="confluence-embedded-image image-center" 
     src="..." 
     data-image-width="1475" 
     data-image-height="807"
     loading="lazy">
```

**Working output (HTML with dimensions → Confluence):**
```html
<img class="confluence-embedded-image image-center" 
     width="700" 
     src="..." 
     data-width="700" 
     data-height="400"
     loading="lazy">
```

### Key Differences
The working version includes:
- `width` attribute (for immediate sizing)
- `data-width` attribute (Confluence responsive framework)
- `data-height` attribute (aspect ratio preservation)

The non-working version only has:
- `data-image-width` / `data-image-height` (original dimensions, not display dimensions)

## Technical Solution Required

### Primary Fix: Enhanced Image Processing
The library needs to modify its image conversion logic to:

1. **For Markdown images** (`![alt](src)`):
   - Convert to HTML with default responsive width (suggest 700px)
   - Calculate proportional height if original dimensions known
   - Add required Confluence attributes

2. **For HTML images without dimensions**:
   - Apply default responsive sizing
   - Add missing Confluence attributes

3. **Always ensure these attributes are present**:
   ```html
   width="[display-width]"
   data-width="[display-width]" 
   data-height="[calculated-height]"
   style="max-width: 100%; height: auto;"
   ```

### Implementation Location
Look for the image processing function in md2conf, likely in:
- HTML/Markdown parser modules
- Image conversion/transformation functions
- Confluence-specific formatters


## Expected Outcome
After fix implementation:
- All images (Markdown and HTML) should render responsively
- Images should not overflow containers
- Images should maintain aspect ratios
- Behavior should match the current "HTML with width+height" example

## Testing Verification
Test the `--image-width` feature with:

1. **Default behavior**: `md2conf test.md` → All images get 700px width
2. **Custom width**: `md2conf --image-width 500 test.md` → All images get 500px width
3. **Markdown images**: `![Test](1200x800.png)` → Should output `width="700" height="467"`
4. **HTML images**: `<img src="1200x800.png">` → Should output `width="700" height="467"`
5. **Pre-sized HTML**: `<img width="1200" height="800" src="img.png">` → Should override to `width="700" height="467"`
6. **Unknown dimensions**: Images without detectable size → Should output `width="700"` (height auto-calculated by Confluence)

**Verification**: All test cases should produce consistent, responsive images that don't overflow containers.
