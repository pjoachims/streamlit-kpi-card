import { describe, it, expect } from 'vitest';
import { millifyValue, formatValue, formatDelta } from './utils';

// ===========================================================================
// millifyValue (6 tests)
// ===========================================================================
describe('millifyValue', () => {
  it('formats thousands as K', () => {
    expect(millifyValue(1500, 1)).toBe('1.5K');
  });

  it('formats millions as M', () => {
    expect(millifyValue(2500000, 1)).toBe('2.5M');
  });

  it('formats billions as B', () => {
    expect(millifyValue(3200000000, 1)).toBe('3.2B');
  });

  it('leaves small numbers as-is (trailing zeros trimmed)', () => {
    expect(millifyValue(42, 2)).toBe('42');
  });

  it('handles negative values', () => {
    expect(millifyValue(-1500000, 1)).toBe('-1.5M');
  });

  it('trims trailing zeros', () => {
    expect(millifyValue(1000, 2)).toBe('1K');
  });
});

// ===========================================================================
// formatValue (4 tests)
// ===========================================================================
describe('formatValue', () => {
  it('formats percentage', () => {
    expect(formatValue(42.567, { type: 'percentage', decimals: 1 })).toBe('42.6%');
  });

  it('formats currency', () => {
    const result = formatValue(1234.5, { type: 'currency', decimals: 2, currency: '$' });
    expect(result).toContain('$');
    expect(result).toContain('1,234.50');
  });

  it('formats integer', () => {
    expect(formatValue(1234.7, { type: 'integer' })).toBe('1,235');
  });

  it('formats decimal', () => {
    expect(formatValue(3.14159, { type: 'decimal', decimals: 2 })).toBe('3.14');
  });
});

// ===========================================================================
// formatDelta (3 tests)
// ===========================================================================
describe('formatDelta', () => {
  it('formats positive relative delta', () => {
    const result = formatDelta(10, 25, true, { decimals: 1 });
    expect(result).toBe('+25.0%');
  });

  it('formats negative absolute delta (no + prefix, abs value)', () => {
    // Negative delta: no "+" prefix, value is Math.abs — arrow indicates direction
    const result = formatDelta(-50, -10, false, { type: 'integer' });
    expect(result).toBe('50');
  });

  it('formats zero delta', () => {
    const result = formatDelta(0, 0, true, { decimals: 1 });
    expect(result).toBe('+0.0%');
  });

  it('formats absolute delta as p.P. when format is percentage', () => {
    const result = formatDelta(2, 4.65, false, { type: 'percentage', decimals: 1 });
    expect(result).toBe('+2.0 p.P.');
  });

  it('formats negative absolute delta as p.P. when format is percentage', () => {
    const result = formatDelta(-3.5, -7.0, false, { type: 'percentage', decimals: 1 });
    expect(result).toBe('3.5 p.P.');
  });
});
