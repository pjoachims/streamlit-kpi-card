/**
 * Format large numbers as K, M, B.
 * @param {number} val - The value to millify
 * @param {number} decimals - Number of decimal places
 * @returns {string}
 */
export function millifyValue(val, decimals = 2) {
  const absVal = Math.abs(val);
  const d = decimals;
  const trimRegex = d === 0 ? /$/ : new RegExp('\\.0{1,' + d + '}$');
  if (absVal >= 1e9) return (val / 1e9).toFixed(d).replace(trimRegex, '') + 'B';
  if (absVal >= 1e6) return (val / 1e6).toFixed(d).replace(trimRegex, '') + 'M';
  if (absVal >= 1e3) return (val / 1e3).toFixed(d).replace(trimRegex, '') + 'K';
  return val.toFixed(d).replace(trimRegex, '');
}

/**
 * Format a value according to type/decimals/currency.
 * @param {number} val
 * @param {{ type: string, decimals?: number, currency?: string }} format
 * @param {{ millify: boolean, millifyDecimals: number }} opts
 * @returns {string}
 */
export function formatValue(val, format = {}, opts = {}) {
  const formatType = format.type || "number";
  const decimals = format.decimals ?? 1;
  const currency = format.currency || "$";

  if (opts.millify && formatType !== "percentage") {
    const millified = millifyValue(val, opts.millifyDecimals ?? 2);
    if (formatType === "currency") {
      return `${currency}${millified}`;
    }
    return millified;
  }

  switch (formatType) {
    case "percentage":
      return `${val.toFixed(decimals)}%`;
    case "currency":
      return `${currency}${val.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`;
    case "integer":
      return Math.round(val).toLocaleString();
    case "decimal":
      return val.toFixed(decimals);
    default:
      return val.toLocaleString();
  }
}

/**
 * Format a delta value for display.
 * @param {number} delta - Absolute delta
 * @param {number} deltaPercent - Percentage delta
 * @param {boolean} showRelative - Whether to show relative (%) or absolute
 * @param {{ type: string, decimals?: number, currency?: string }} format
 * @param {{ millify: boolean, millifyDecimals: number }} opts
 * @returns {string}
 */
export function formatDelta(delta, deltaPercent, showRelative, format = {}, opts = {}) {
  const decimals = format.decimals ?? 1;
  if (showRelative) {
    return `${deltaPercent >= 0 ? "+" : ""}${deltaPercent.toFixed(decimals)}%`;
  } else if (format.type === "percentage") {
    return `${delta >= 0 ? "+" : ""}${Math.abs(delta).toFixed(decimals)} p.P.`;
  } else {
    return `${delta >= 0 ? "+" : ""}${formatValue(Math.abs(delta), format, opts)}`;
  }
}
