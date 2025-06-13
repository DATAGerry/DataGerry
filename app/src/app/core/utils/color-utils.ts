/**
 * Determines whether black or white text is more readable on a given background color.
 * @param hexColor The background color in hex format (e.g., #RRGGBB).
 * @returns 'black' or 'white' depending on the contrast.
 */
export function getTextColorBasedOnBackground(hexColor: string): string {
    // Remove the hash if present
    hexColor = hexColor.replace('#', '');
  
    // Convert hex to RGB
    const r = parseInt(hexColor.substring(0, 2), 16);
    const g = parseInt(hexColor.substring(2, 4), 16);
    const b = parseInt(hexColor.substring(4, 6), 16);
  
    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
    // Return black for light backgrounds and white for dark backgrounds
    return luminance > 0.5 ? 'black' : 'white';
  }


  export function hexToRgb(hex: string): [number, number, number] {
    if (!hex.startsWith('#')) return [119, 119, 119];  // fallback grey
    const bigint = parseInt(hex.substring(1), 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return [r, g, b];
  }