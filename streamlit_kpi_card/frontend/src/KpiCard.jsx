import React, { useState, useEffect, useMemo } from "react";
import { LineChart, Line, BarChart, Bar, AreaChart, Area, ComposedChart, ResponsiveContainer, Tooltip, ReferenceLine, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid } from "recharts";
import { millifyValue as millifyValueUtil, formatValue as formatValueUtil, formatDelta as formatDeltaUtil } from "./utils";

// Design Token System
const tokens = {
  spacing: {
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 20,
    xxl: 24,
  },
  colors: {
    light: {
      background: "#ffffff",
      foreground: "#171717",
      muted: "#737373",
      success: "#22c55e",
      successContrast: "#16a34a",
      error: "#ef4444",
      border: "#e5e5e5",
      hover: "rgba(0, 0, 0, 0.05)",
    },
    dark: {
      background: "#0a0a0a",
      foreground: "#fafafa",
      muted: "#a3a3a3",
      success: "#22c55e",
      successContrast: "#4ade80",
      error: "#ef4444",
      border: "#262626",
      hover: "rgba(255, 255, 255, 0.1)",
    },
  },
  shadows: {
    sm: "0 0 0 1px rgba(0,0,0,.03), 0 2px 4px rgba(0,0,0,.05), 0 12px 24px rgba(0,0,0,.05)",
    md: "0 0 0 1px rgba(0,0,0,.03), 0 4px 8px rgba(0,0,0,.08), 0 16px 32px rgba(0,0,0,.08)",
    dark: {
      sm: "0 0 0 1px rgba(255,255,255,.05), 0 2px 4px rgba(0,0,0,.2), 0 12px 24px rgba(0,0,0,.2)",
      md: "0 0 0 1px rgba(255,255,255,.05), 0 4px 8px rgba(0,0,0,.3), 0 16px 32px rgba(0,0,0,.3)",
    },
    focus: "0 0 0 2px #fff, 0 0 0 4px #3b82f6",
    focusDark: "0 0 0 2px #0a0a0a, 0 0 0 4px #3b82f6",
  },
  transitions: {
    default: "200ms cubic-bezier(0.4, 0, 0.2, 1)",
    fast: "150ms cubic-bezier(0.4, 0, 0.2, 1)",
  },
  radii: {
    sm: 6,
    md: 8,
    lg: 12,
    xl: 16,
  },
  fontFamily: "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",

  // --- Extended tokens ---

  sizeScale: {
    small:  { name: 9,  value: 22, delta: 10, spacing: 0.8 },
    medium: { name: 11, value: 32, delta: 12, spacing: 1 },
    large:  { name: 13, value: 42, delta: 14, spacing: 1.2 },
  },

  chart: {
    margins: {
      axes:         { top: 2, right: 4, left: -5, bottom: 0 },
      yLabels:      { top: 2, right: 0,  left: 0, bottom: 0 },
      default:      { top: 2, right: 2,  left: 0, bottom: 2 },
      dots:         { top: 5, right: 5,  left: 5, bottom: 5 },
      sparklineDot: { top: 5, right: 8,  left: 0, bottom: 5 },
    },
    animationDuration: 300,
    strokeWidth: 2,
    barRadius: 4,
    barDimmedOpacity: 0.25,
    sparklineDot: { radius: 5, strokeWidth: 2 },
    referenceLine: { strokeWidth: 1.5, dashArray: "5 5" },
    axis: { fontSize: 10, yAxisWidth: 35, minTickGap: 30, gridDash: "3 3" },
    yLabel: { fontSize: 8, rowHeight: 12, rightPad: 28 },
    gradient: { topOpacity: 0.4, bottomOpacity: 0.05 },
    placeholder: { light: "rgba(0,0,0,0.02)", dark: "rgba(255,255,255,0.03)" },
  },

  tooltip: {
    fontSize: 11,
    labelFontSize: 10,
    zIndex: 10,
  },

  delta: {
    fontSize: { text: 12, badge: 11, pill: 12, icon: 14, label: 11 },
    opacity: { hovered: 0.8 },
    hoverScale: { badge: "scale(1.05)", icon: "scale(1.05)", pill: "scale(1.02)" },
    bg: {
      light:      { success: 0.1,  error: 0.1 },
      dark:       { success: 0.15, error: 0.15 },
      hoverLight: { success: 0.15, error: 0.15 },
      hoverDark:  { success: 0.25, error: 0.25 },
    },
  },

  arrows: {
    small: { size: 12, margin: 2 },
    large: { size: 24, margin: 4 },
  },

  layouts: {
    mini: {
      padding: "6px 12px",
      height: "44px",
      nameFontSize: 13,
      valueFontSize: 15,
      deltaFontSize: 11,
      arrowSize: 9,
      chartMaxHeight: "30px",
      nameWidth: "30%",
    },
    compact: {
      nameFontSize: 11,
      valueFontSize: 18,
      deltaFontSize: 12,
      arrowSize: 10,
      chartWidth: "120px",
      chartHeight: "30px",
    },
    horizontal: {
      chartHeight: "40px",
    },
    valueFocus: {
      chartHeight: "30px",
      chartOpacity: 0.7,
    },
    chartFocus: {
      overlayNameFontSize: 10,
      overlayValueFontSize: 22,
      overlayDeltaFontSize: 11,
      overlayArrowSize: 10,
      overlayDeltaGap: 3,
      overlayDeltaMarginTop: 2,
      bgOpacity: { light: 0.75, dark: 0.65 },
      defaultHeight: "180px",
    },
  },

  detail: {
    transition: "300ms ease",
    statLabelFontSize: 10,
    statValueFontSize: 14,
    buttonSize: 14,
    buttonPadding: 4,
    zIndex: 5,
    collapsedOpacity: 0.5,
  },

  info: {
    iconSize: 14,
    opacity: 0.6,
  },

  hover: {
    translateY: -1,
  },
};

// Arrow SVG components for delta indicator
const ArrowUp = ({ size = tokens.arrows.small.size }) => (
  <svg width={size} height={size} viewBox="0 0 12 12" fill="none" style={{ marginRight: tokens.arrows.small.margin }}>
    <path d="M6 2.5L10 6.5H7V9.5H5V6.5H2L6 2.5Z" fill="currentColor" />
  </svg>
);

const ArrowDown = ({ size = tokens.arrows.small.size }) => (
  <svg width={size} height={size} viewBox="0 0 12 12" fill="none" style={{ marginRight: tokens.arrows.small.margin }}>
    <path d="M6 9.5L2 5.5H5V2.5H7V5.5H10L6 9.5Z" fill="currentColor" />
  </svg>
);

// Large arrow icons for "icon" delta style
const LargeArrowUp = () => (
  <svg width={tokens.arrows.large.size} height={tokens.arrows.large.size} viewBox="0 0 24 24" fill="none" style={{ marginRight: tokens.arrows.large.margin }}>
    <path d="M12 4L20 14H14V20H10V14H4L12 4Z" fill="currentColor" />
  </svg>
);

const LargeArrowDown = () => (
  <svg width={tokens.arrows.large.size} height={tokens.arrows.large.size} viewBox="0 0 24 24" fill="none" style={{ marginRight: tokens.arrows.large.margin }}>
    <path d="M12 20L4 10H10V4H14V10H20L12 20Z" fill="currentColor" />
  </svg>
);

const KpiCard = ({
  // === Core data ===
  name,
  value,
  valueBefore,
  delta,
  deltaPercent,
  relativeChange = false,
  isInverse = false,
  timeSeriesData,
  averageValue = null,
  format = { type: "number", decimals: 1, currency: "$" },
  extraDeltas = null,
  // === Style dicts ===
  cardStyle = {},
  chartStyle = {},
  textStyle = {},
  deltaStyle = {},
  // === Layout ===
  layout = "vertical",
  size = "medium",
  theme = "auto",
  // === Mini layout (kpi_cards) ===
  miniColumns = "auto",
  selectable = false,
  selected = null,
  onSelect = null,
  // === Controlled expand ===
  isExpanded: isExpandedProp = null,
  onToggleExpand = null,
}) => {
  // Extract from cardStyle (with defaults)
  const {
    padding: cardPadding,
    borderRadius = "12px",
    backgroundColor,
    shadow: shadowStyle = "subtle",
    border: borderStyle = "hairline",
    backgroundStyle = "solid",
    accentColor = null,
    height = null,
    showHeader = true,
    showDetail: showDetailButton = false,
    detailHeight = 300,
    overlayPosition = "auto",
    overlayOpacity = null,
  } = cardStyle;

  // Extract from chartStyle (with defaults)
  const {
    type: chartType = "line",
    lineColor = null,
    height: chartHeight,
    maxHeight: maxChartHeight = null,
    margin: chartMargin,
    fill: chartFill = false,
    fillOpacity: chartFillOpacity,
    show: showChart = true,
    showAverage = false,
    axis = "none",
    gridX = false,
    gridY = false,
    yStartAtZero = false,
    xLabels = null,
    markers = null,
    focusLastN = null,
    referenceLine = null,
  } = chartStyle;

  // Extract from textStyle (with defaults)
  const {
    nameSize,
    nameColor,
    nameWeight,
    nameMarginBottom,
    nameLetterSpacing,
    nameTransform,
    valueSize,
    valueColor,
    valueWeight,
    millify = false,
    millifyDecimals = 2,
    infoText = null,
  } = textStyle;

  // Extract from deltaStyle (with defaults)
  const {
    format: deltaFormat = "pill",
    position: deltaPosition = "below-value",
    stack: deltaStack = "horizontal",
    label: deltaLabel = "vs previous",
    positiveColor: deltaPositiveColor,
    negativeColor: deltaNegativeColor,
    fontSize: deltaFontSize,
    arrowSize: deltaArrowSize,
    padding: deltaPadding,
    borderRadius: deltaBorderRadius,
    labelSize: deltaLabelSize,
    gap: deltaGap,
  } = deltaStyle;

  const [showRelative, setShowRelative] = useState(relativeChange);
  const [isCardHovered, setIsCardHovered] = useState(false);
  const [isDeltaHovered, setIsDeltaHovered] = useState(false);
  const [isDeltaFocused, setIsDeltaFocused] = useState(false);
  const [infoHovered, setInfoHovered] = useState(false);
  const [resolvedTheme, setResolvedTheme] = useState("light");
  const [chartReady, setChartReady] = useState(false);
  const [isExpandedInternal, setIsExpandedInternal] = useState(false);

  // Controlled vs uncontrolled expand
  const isExpanded = isExpandedProp != null ? isExpandedProp : isExpandedInternal;
  const setIsExpanded = onToggleExpand || setIsExpandedInternal;

  // Stable unique ID for SVG gradients (sanitize name + use value hash)
  const gradientId = useMemo(() => {
    const sanitized = name.replace(/[^a-zA-Z0-9]/g, '_');
    const hash = Math.abs(value * 1000).toString(36).substr(0, 6);
    return `gradient-${sanitized}-${hash}`;
  }, [name, value]);

  // Defer chart rendering - show numbers first, charts after idle
  useEffect(() => {
    if (!showChart || !timeSeriesData?.length) {
      setChartReady(true);
      return;
    }
    // Use requestIdleCallback if available, otherwise setTimeout
    const schedule = window.requestIdleCallback || ((cb) => setTimeout(cb, 16));
    const cancel = window.cancelIdleCallback || clearTimeout;
    const id = schedule(() => setChartReady(true), { timeout: 100 });
    return () => cancel(id);
  }, [showChart, timeSeriesData]);

  // Resolve theme (auto detects system preference)
  useEffect(() => {
    if (theme === "auto") {
      const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
      setResolvedTheme(mediaQuery.matches ? "dark" : "light");

      const handler = (e) => setResolvedTheme(e.matches ? "dark" : "light");
      mediaQuery.addEventListener("change", handler);
      return () => mediaQuery.removeEventListener("change", handler);
    } else {
      setResolvedTheme(theme);
    }
  }, [theme]);

  const isDark = resolvedTheme === "dark";
  const colors = isDark ? tokens.colors.dark : tokens.colors.light;

  const sizes = tokens.sizeScale[size] || tokens.sizeScale.medium;

  const formatType = format?.type || "number";
  const decimals = format?.decimals ?? 1;
  const currency = format?.currency || "$";

  const millifyValue = (val) => millifyValueUtil(val, millifyDecimals);
  const formatValue = (val) => formatValueUtil(val, format, { millify, millifyDecimals });
  const formatDelta = () => formatDeltaUtil(delta, deltaPercent, showRelative, format, { millify, millifyDecimals });

  const toggleDeltaMode = () => {
    setShowRelative(!showRelative);
  };

  const handleDeltaKeyDown = (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      toggleDeltaMode();
    }
  };

  const isPositive = delta >= 0;
  const actuallyGood = isInverse ? !isPositive : isPositive;
  const deltaColor = actuallyGood ? colors.successContrast : colors.error;

  const deltaBgTokens = isDark ? tokens.delta.bg.dark : tokens.delta.bg.light;
  const deltaBgHoverTokens = isDark ? tokens.delta.bg.hoverDark : tokens.delta.bg.hoverLight;
  const deltaBgColor = actuallyGood
    ? `rgba(34, 197, 94, ${deltaBgTokens.success})`
    : `rgba(239, 68, 68, ${deltaBgTokens.error})`;
  const deltaBgHover = actuallyGood
    ? `rgba(34, 197, 94, ${deltaBgHoverTokens.success})`
    : `rgba(239, 68, 68, ${deltaBgHoverTokens.error})`;
  const statusColor = actuallyGood ? colors.success : colors.error;
  const chartLineColor = lineColor || statusColor;

  // Derive axis flags from the axis prop
  // All axis modes now use HTML labels for compact, clean rendering
  const showAxes = false; // Never use Recharts built-in axes
  const showXAxis = false;
  const showYAxis = false;
  const showYLabels = axis === "y" || axis === "both";
  const showXLabels = axis === "x" || axis === "both" || (xLabels && xLabels.length > 0); // HTML labels

  // Derive grid flags
  const hasGridX = gridX === true || (Array.isArray(gridX) && gridX.length > 0);
  const hasGridY = gridY === true || (Array.isArray(gridY) && gridY.length > 0);
  const showGrid = hasGridX || hasGridY;

  // Marker set for O(1) lookup
  const markerSet = useMemo(() => {
    if (!Array.isArray(markers) || markers.length === 0) return null;
    return new Set(markers);
  }, [markers]);

  // Render dot only at marker indices (× cross marker)
  const markerDot = markerSet ? (props) => {
    const { cx, cy, index } = props;
    if (!markerSet.has(index)) return null;
    const s = 3; // half-size of the ×
    return (
      <g key={`marker-${index}`}>
        <line x1={cx - s} y1={cy - s} x2={cx + s} y2={cy + s} stroke={colors.muted} strokeWidth={1.5} />
        <line x1={cx - s} y1={cy + s} x2={cx + s} y2={cy - s} stroke={colors.muted} strokeWidth={1.5} />
      </g>
    );
  } : false;

  // Mini layout always uses tight domain (sparkline shows trend, not scale)
  const effectiveYZero = layout === "mini" ? false : yStartAtZero;

  const placeholderBg = isDark ? tokens.chart.placeholder.dark : tokens.chart.placeholder.light;

  // Shadow styles
  const getShadowStyle = () => {
    if (shadowStyle) {
      switch (shadowStyle) {
        case "none":
          return "none";
        case "subtle":
          return isDark
            ? "0 1px 2px rgba(0,0,0,.2)"
            : "0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.03)";
        case "sharp":
          return isDark
            ? "4px 4px 0 rgba(255,255,255,.1)"
            : "4px 4px 0 rgba(0,0,0,.1)";
        case "glow":
          if (accentColor) {
            // Parse hex to rgb for glow
            const hex = accentColor.replace('#', '');
            const r = parseInt(hex.substring(0, 2), 16);
            const g = parseInt(hex.substring(2, 4), 16);
            const b = parseInt(hex.substring(4, 6), 16);
            return `0 0 8px rgba(${r}, ${g}, ${b}, ${isDark ? 0.25 : 0.2}), 0 0 20px rgba(${r}, ${g}, ${b}, ${isDark ? 0.15 : 0.1})`;
          }
          return actuallyGood
            ? `0 0 8px rgba(34, 197, 94, ${isDark ? 0.25 : 0.2}), 0 0 20px rgba(34, 197, 94, ${isDark ? 0.15 : 0.1})`
            : `0 0 8px rgba(239, 68, 68, ${isDark ? 0.25 : 0.2}), 0 0 20px rgba(239, 68, 68, ${isDark ? 0.15 : 0.1})`;
        case "inset":
          return isDark
            ? "inset 0 2px 4px rgba(0,0,0,.3)"
            : "inset 0 2px 4px rgba(0,0,0,.06)";
        default:
          return isDark ? tokens.shadows.dark.sm : tokens.shadows.sm;
      }
    }
    if (!shadow) return "none";
    if (isDark) {
      return isCardHovered ? tokens.shadows.dark.md : tokens.shadows.dark.sm;
    }
    return isCardHovered ? tokens.shadows.md : tokens.shadows.sm;
  };

  // Border styles
  const getBorderStyle = () => {
    const borderAccentColor = accentColor || statusColor;
    if (borderStyle) {
      switch (borderStyle) {
        case "none":
          return { border: "none" };
        case "hairline":
          return { border: `0.5px solid ${colors.border}` };
        case "left-accent":
          return {
            border: `1px solid ${colors.border}`,
            borderLeft: `4px solid ${borderAccentColor}`
          };
        case "top-accent":
          return {
            border: `1px solid ${colors.border}`,
            borderTop: `4px solid ${borderAccentColor}`
          };
        case "full":
          return { border: `2px solid ${borderAccentColor}` };
        default:
          return { border: border || "none" };
      }
    }
    // Legacy border handling
    const effectiveBorder = border === "1px solid #e5e7eb" && isDark
      ? `1px solid ${colors.border}`
      : border;
    return { border: effectiveBorder || "none" };
  };

  // Background styles
  const getBackgroundStyle = () => {
    const effectiveBackground = backgroundColor === "#ffffff" && isDark
      ? colors.background
      : backgroundColor;

    if (backgroundStyle) {
      switch (backgroundStyle) {
        case "solid":
          return { background: effectiveBackground };
        case "gradient":
          return {
            background: isDark
              ? `linear-gradient(180deg, ${colors.background} 0%, #151515 100%)`
              : `linear-gradient(180deg, #ffffff 0%, #f9fafb 100%)`
          };
        case "glass":
          return {
            background: isDark
              ? "rgba(26, 26, 26, 0.8)"
              : "rgba(255, 255, 255, 0.8)",
            backdropFilter: "blur(10px)",
            WebkitBackdropFilter: "blur(10px)",
          };
        case "tinted":
          return {
            background: actuallyGood
              ? (isDark ? "rgba(34, 197, 94, 0.08)" : "rgba(34, 197, 94, 0.05)")
              : (isDark ? "rgba(239, 68, 68, 0.08)" : "rgba(239, 68, 68, 0.05)")
          };
        case "transparent":
          return { background: "transparent" };
        default:
          return { background: effectiveBackground };
      }
    }
    return { background: effectiveBackground };
  };

  // Tooltip styles
  const tooltipStyles = {
    backgroundColor: isDark ? "#171717" : "#ffffff",
    border: `1px solid ${colors.border}`,
    borderRadius: `${tokens.radii.sm}px`,
    color: colors.foreground,
    fontSize: `${tokens.tooltip.fontSize}px`,
    padding: `${tokens.spacing.xs}px ${tokens.spacing.sm}px`,
    boxShadow: isDark ? tokens.shadows.dark.sm : tokens.shadows.sm,
    zIndex: tokens.tooltip.zIndex,
  };

  // Determine effective chart type (chartType is already extracted from chartStyle.type with default "line")

  // Render chart based on chartStyle. withAxes overrides showAxes/showGrid for detail view.
  const renderChart = (withAxes = false) => {
    if (!timeSeriesData || timeSeriesData.length === 0) return null;

    // Merge flexible reference line values into chart data
    const refValues = referenceLine?.values;
    const hasRefSeries = Array.isArray(refValues) && refValues.length > 0;
    const chartData = hasRefSeries
      ? timeSeriesData.map((d, i) => ({ ...d, ref: i < refValues.length ? refValues[i] : null }))
      : timeSeriesData;

    const refSeriesColor = referenceLine?.color || (isDark ? "#e5e5e5" : colors.muted);
    const refSeriesStyle = referenceLine?.style === "solid" ? "0" : tokens.chart.referenceLine.dashArray;
    // Marker dot for ref series (small circle in ref color)
    const refMarkerDot = markerSet ? (props) => {
      const { cx, cy, index } = props;
      if (!markerSet.has(index)) return null;
      return <circle key={`ref-marker-${index}`} cx={cx} cy={cy} r={2.5} fill={refSeriesColor} />;
    } : false;

    const refSeriesLine = hasRefSeries ? (
      <Line
        type="monotone"
        dataKey="ref"
        stroke={refSeriesColor}
        strokeWidth={tokens.chart.referenceLine.strokeWidth}
        strokeDasharray={refSeriesStyle}
        dot={refMarkerDot}
        animationDuration={tokens.chart.animationDuration}
      />
    ) : null;

    const xAxis = withAxes || showXAxis;
    const yAxis = withAxes || showYAxis;
    const grid = withAxes || showGrid;
    const yLabels = !yAxis && showYLabels && !withAxes;
    const anyAxis = xAxis || yAxis || showYLabels || showXLabels;
    const axisMargin = anyAxis
      ? tokens.chart.margins.axes
      : yLabels
        ? tokens.chart.margins.yLabels
        : tokens.chart.margins.default;

    const axisTickStyle = { fontSize: tokens.chart.axis.fontSize, fill: colors.muted, fontFamily: tokens.fontFamily };
    // Format Y axis ticks using the card's format
    const formatYTick = (val) => {
      if (millify) return millifyValue(val);
      if (formatType === "currency") return `${currency}${val.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
      if (formatType === "percentage") return `${val.toFixed(1)}%`;
      return val.toLocaleString(undefined, { maximumFractionDigits: 1 });
    };

    const yDomain = effectiveYZero ? [0, 'dataMax'] : ['dataMin', 'dataMax'];

    // Grid rendering
    const gridColor = isDark ? "rgba(255,255,255,0.12)" : "rgba(0,0,0,0.12)";
    const gridElements = [];

    // Auto grid lines (boolean true)
    if (gridX === true || gridY === true) {
      gridElements.push(
        <CartesianGrid
          key="auto-grid"
          strokeDasharray={tokens.chart.axis.gridDash}
          stroke={gridColor}
          horizontal={gridY === true}
          vertical={gridX === true}
        />
      );
    }
    // Explicit gridY positions → horizontal ReferenceLine at each Y value
    if (Array.isArray(gridY)) {
      gridY.forEach((yVal, i) => {
        gridElements.push(
          <ReferenceLine key={`gy-${i}`} y={yVal} stroke={gridColor} strokeDasharray={tokens.chart.axis.gridDash} />
        );
      });
    }
    // Explicit gridX positions → vertical ReferenceLine at data indices
    if (Array.isArray(gridX) && chartData.length > 0) {
      gridX.forEach((idx, i) => {
        if (idx >= 0 && idx < chartData.length) {
          gridElements.push(
            <ReferenceLine key={`gx-${i}`} x={chartData[idx].index} stroke={gridColor} strokeDasharray={tokens.chart.axis.gridDash} />
          );
        }
      });
    }

    // Shared axis elements
    const axisElements = (
      <>
        {gridElements}
        {xAxis && <XAxis dataKey="index" tick={axisTickStyle} axisLine={false} tickLine={false} interval="preserveStartEnd" minTickGap={tokens.chart.axis.minTickGap} />}
        {yAxis ? (
          <YAxis tick={axisTickStyle} axisLine={false} tickLine={false} tickFormatter={formatYTick} domain={effectiveYZero ? [0, 'auto'] : ['auto', 'auto']} tickCount={4} allowDecimals={false} width={30} />
        ) : (
          <YAxis domain={yDomain} hide />
        )}
      </>
    );

    const commonTooltipProps = {
      position: anyAxis ? undefined : { y: -30 },
      cursor: anyAxis ? { stroke: colors.muted, strokeDasharray: tokens.chart.axis.gridDash } : false,
      separator: "",
      contentStyle: tooltipStyles,
      labelStyle: { color: colors.muted, fontWeight: 500, marginBottom: "2px", fontSize: `${tokens.tooltip.labelFontSize}px` },
      itemStyle: { color: colors.foreground, fontWeight: 600, padding: "0", listStyle: "none" },
      labelFormatter: (label, payload) => {
        if (payload && payload.length > 0) {
          return payload[0].payload.index;
        }
        return "";
      },
      formatter: (value) => [formatValue(value), ""],
      ...((referenceLine && (referenceLine.value != null || hasRefSeries)) ? {
        content: ({ payload, label }) => {
          if (!payload || payload.length === 0) return null;
          const dataPoint = payload.find(p => p.dataKey === "value") || payload[0];
          const refPoint = hasRefSeries ? payload.find(p => p.dataKey === "ref") : null;
          const refLabel = referenceLine.label || "Ref";
          const refColor = referenceLine.color || (isDark ? "#e5e5e5" : colors.muted);
          const refVal = hasRefSeries ? refPoint?.value : referenceLine.value;
          return (
            <div style={tooltipStyles}>
              <div style={{ color: colors.muted, fontWeight: 500, marginBottom: "2px", fontSize: `${tokens.tooltip.labelFontSize}px` }}>
                {dataPoint.payload.index}
              </div>
              <div style={{ color: colors.foreground, fontWeight: 600, fontSize: `${tokens.tooltip.fontSize}px` }}>
                {formatValue(dataPoint.value)}
              </div>
              {refVal != null && (
                <div style={{ color: refColor, fontSize: `${tokens.tooltip.labelFontSize}px`, marginTop: "2px", borderTop: `1px solid ${isDark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.08)"}`, paddingTop: "2px" }}>
                  {refLabel}: {formatValue(refVal)}
                </div>
              )}
            </div>
          );
        },
      } : {}),
    };

    const averageLine = showAverage && averageValue !== null && (
      <ReferenceLine
        y={averageValue}
        stroke={colors.muted}
        strokeDasharray={tokens.chart.referenceLine.dashArray}
        strokeWidth={tokens.chart.referenceLine.strokeWidth}
      />
    );

    const refLineColor = referenceLine?.color || (isDark ? "#e5e5e5" : colors.muted);
    const refLine = referenceLine && referenceLine.value != null && (
      <ReferenceLine
        y={referenceLine.value}
        stroke={refLineColor}
        strokeDasharray={referenceLine.style === "solid" ? "0" : tokens.chart.referenceLine.dashArray}
        strokeWidth={tokens.chart.referenceLine.strokeWidth}
      />
    );

    switch (chartType) {
      case "line":
        return (
          <LineChart data={chartData} margin={axisMargin}>
            {axisElements}
            <Tooltip {...commonTooltipProps} />
            {averageLine}
            {refLine}
            <Line
              type="monotone"
              dataKey="value"
              stroke={chartLineColor}
              strokeWidth={tokens.chart.strokeWidth}
              dot={markerDot}
              animationDuration={tokens.chart.animationDuration}
            />
            {refSeriesLine}
          </LineChart>
        );

      case "gradient-area":
        return (
          <ComposedChart data={chartData} margin={axisMargin}>
            <defs>
              <linearGradient id={withAxes ? `${gradientId}-detail` : gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={chartLineColor} stopOpacity={tokens.chart.gradient.topOpacity} />
                <stop offset="100%" stopColor={chartLineColor} stopOpacity={tokens.chart.gradient.bottomOpacity} />
              </linearGradient>
            </defs>
            {axisElements}
            <Tooltip {...commonTooltipProps} />
            {averageLine}
            {refLine}
            <Area
              type="monotone"
              dataKey="value"
              stroke={chartLineColor}
              fill={`url(#${withAxes ? `${gradientId}-detail` : gradientId})`}
              strokeWidth={tokens.chart.strokeWidth}
              animationDuration={tokens.chart.animationDuration}
              dot={markerDot}
            />
            {refSeriesLine}
          </ComposedChart>
        );

      case "dots":
        return (
          <ComposedChart data={chartData} margin={anyAxis ? tokens.chart.margins.axes : tokens.chart.margins.dots}>
            {axisElements}
            <Tooltip {...commonTooltipProps} />
            {averageLine}
            {refLine}
            <Scatter
              dataKey="value"
              fill={chartLineColor}
              animationDuration={tokens.chart.animationDuration}
            />
            {refSeriesLine}
          </ComposedChart>
        );

      case "bar":
      case "rounded-bar": {
        const isRounded = chartType === "rounded-bar";
        const r = isRounded ? tokens.chart.barRadius : 0;
        return (
          <ComposedChart data={chartData} margin={axisMargin}>
            {axisElements}
            <Tooltip {...commonTooltipProps} />
            {averageLine}
            {refLine}
            <Bar
              dataKey="value"
              fill={chartLineColor}
              animationDuration={tokens.chart.animationDuration}
              radius={[r, r, 0, 0]}
              shape={(props) => {
                const { x, y, width, height, index } = props;
                const isHighlighted = focusLastN === null || index >= chartData.length - focusLastN;
                return (
                  <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    fill={chartLineColor}
                    opacity={isHighlighted ? 1 : tokens.chart.barDimmedOpacity}
                    rx={r}
                    ry={r}
                  />
                );
              }}
            />
            {refSeriesLine}
          </ComposedChart>
        );
      }

      case "sparkline-dot":
        const lastPoint = chartData[chartData.length - 1];
        return (
          <LineChart data={chartData} margin={anyAxis ? axisMargin : yLabels ? { ...axisMargin, top: tokens.chart.margins.sparklineDot.top, bottom: tokens.chart.margins.sparklineDot.bottom } : tokens.chart.margins.sparklineDot}>
            {axisElements}
            <Tooltip {...commonTooltipProps} />
            {averageLine}
            {refLine}
            <Line
              type="monotone"
              dataKey="value"
              stroke={chartLineColor}
              strokeWidth={tokens.chart.strokeWidth}
              dot={(props) => {
                const { cx, cy, index } = props;
                const elements = [];
                if (index === chartData.length - 1) {
                  elements.push(
                    <circle
                      key={`dot-${index}`}
                      cx={cx}
                      cy={cy}
                      r={tokens.chart.sparklineDot.radius}
                      fill={chartLineColor}
                      stroke={isDark ? "none" : "#fff"}
                      strokeWidth={isDark ? 0 : tokens.chart.sparklineDot.strokeWidth}
                    />
                  );
                }
                if (markerSet && markerSet.has(index)) {
                  const s = 3;
                  elements.push(
                    <g key={`marker-${index}`}>
                      <line x1={cx - s} y1={cy - s} x2={cx + s} y2={cy + s} stroke={colors.muted} strokeWidth={1.5} />
                      <line x1={cx - s} y1={cy + s} x2={cx + s} y2={cy - s} stroke={colors.muted} strokeWidth={1.5} />
                    </g>
                  );
                }
                return elements.length > 0 ? <g>{elements}</g> : null;
              }}
              animationDuration={tokens.chart.animationDuration}
            />
            {refSeriesLine}
          </LineChart>
        );

      default:
        return (
          <LineChart data={chartData} margin={axisMargin}>
            {axisElements}
            <Tooltip {...commonTooltipProps} />
            {averageLine}
            {refLine}
            <Line
              type="monotone"
              dataKey="value"
              stroke={chartLineColor}
              strokeWidth={tokens.chart.strokeWidth}
              dot={markerDot}
              animationDuration={tokens.chart.animationDuration}
            />
            {refSeriesLine}
          </LineChart>
        );
    }
  };

  // Render delta indicator based on deltaStyle
  const renderDelta = () => {
    // Effective styling values (custom or defaults)
    const effectiveArrowSize = deltaArrowSize || tokens.arrows.small.size;
    const effectiveLabelSize = deltaLabelSize || `${tokens.delta.fontSize.label}px`;
    const effectiveGap = deltaGap || `${tokens.spacing.xs}px`;

    const deltaContent = (
      <>
        {isPositive ? <ArrowUp size={effectiveArrowSize} /> : <ArrowDown size={effectiveArrowSize} />}
        {formatDelta()}
      </>
    );

    const vsPrevious = deltaLabel ? (
      <span style={{ fontSize: effectiveLabelSize, color: colors.muted }}>
        {deltaLabel}
      </span>
    ) : null;

    const commonProps = {
      role: "button",
      tabIndex: 0,
      "aria-label": `Change indicator: ${formatDelta()} vs previous. Click or press Enter to toggle between relative and absolute change.`,
      onClick: toggleDeltaMode,
      onKeyDown: handleDeltaKeyDown,
      onFocus: () => setIsDeltaFocused(true),
      onBlur: () => setIsDeltaFocused(false),
      onMouseEnter: () => setIsDeltaHovered(true),
      onMouseLeave: () => setIsDeltaHovered(false),
      title: "Click to toggle between relative and absolute change",
    };

    switch (deltaFormat) {
      case "text":
        return (
          <div
            {...commonProps}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: effectiveGap,
              cursor: "pointer",
              userSelect: "none",
              padding: deltaPadding || `${tokens.spacing.xs}px 0`,
              width: "fit-content",
              flexShrink: 0,
              outline: "none",
              opacity: isDeltaHovered ? tokens.delta.opacity.hovered : 1,
              transition: `opacity ${tokens.transitions.fast}`,
            }}
          >
            <span style={{ display: "flex", alignItems: "center", fontSize: deltaFontSize || `${tokens.delta.fontSize.text}px`, fontWeight: 500, color: deltaColor }}>
              {deltaContent}
            </span>
            {vsPrevious}
          </div>
        );

      case "badge":
        return (
          <div
            {...commonProps}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: effectiveGap,
              cursor: "pointer",
              userSelect: "none",
              width: "fit-content",
              flexShrink: 0,
              outline: "none",
            }}
          >
            <span
              style={{
                display: "flex",
                alignItems: "center",
                fontSize: deltaFontSize || `${tokens.delta.fontSize.badge}px`,
                fontWeight: 600,
                color: "#fff",
                backgroundColor: deltaColor,
                padding: deltaPadding || `${tokens.spacing.xs}px ${tokens.spacing.sm}px`,
                borderRadius: deltaBorderRadius || "9999px",
                transform: isDeltaHovered ? tokens.delta.hoverScale.badge : "scale(1)",
                transition: `transform ${tokens.transitions.fast}`,
                boxShadow: isDeltaFocused ? (isDark ? tokens.shadows.focusDark : tokens.shadows.focus) : "none",
              }}
            >
              {deltaContent}
            </span>
            {vsPrevious}
          </div>
        );

      case "inline":
        // This returns null - the delta will be rendered inline with the value
        return null;

      case "icon":
        return (
          <div
            {...commonProps}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: effectiveGap,
              cursor: "pointer",
              userSelect: "none",
              width: "fit-content",
              flexShrink: 0,
              outline: "none",
              color: deltaColor,
              transform: isDeltaHovered ? tokens.delta.hoverScale.icon : "scale(1)",
              transition: `transform ${tokens.transitions.fast}`,
              boxShadow: isDeltaFocused ? (isDark ? tokens.shadows.focusDark : tokens.shadows.focus) : "none",
            }}
          >
            {isPositive ? <LargeArrowUp /> : <LargeArrowDown />}
            <div style={{ display: "flex", flexDirection: "column" }}>
              <span style={{ fontSize: deltaFontSize || `${tokens.delta.fontSize.icon}px`, fontWeight: 600 }}>{formatDelta()}</span>
              {vsPrevious}
            </div>
          </div>
        );

      case "pill":
      default:
        return (
          <div
            {...commonProps}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: effectiveGap,
              marginBottom: "0",
              cursor: "pointer",
              userSelect: "none",
              padding: deltaPadding || `${tokens.spacing.xs}px ${tokens.spacing.sm}px`,
              borderRadius: deltaBorderRadius || `${tokens.radii.sm}px`,
              backgroundColor: isDeltaHovered ? deltaBgHover : deltaBgColor,
              transition: `background-color ${tokens.transitions.default}, transform ${tokens.transitions.fast}`,
              transform: isDeltaHovered ? tokens.delta.hoverScale.pill : "scale(1)",
              width: "fit-content",
              flexShrink: 0,
              outline: "none",
              boxShadow: isDeltaFocused ? (isDark ? tokens.shadows.focusDark : tokens.shadows.focus) : "none",
            }}
          >
            <span style={{ display: "flex", alignItems: "center", fontSize: deltaFontSize || `${tokens.delta.fontSize.pill}px`, fontWeight: 500, color: deltaColor }}>
              {deltaContent}
            </span>
            {vsPrevious}
          </div>
        );
    }
  };

  // Render a single delta item (for extra deltas)
  const renderSingleDelta = (d, idx) => {
    const dIsPositive = d.delta >= 0;
    const dActuallyGood = d.isInverse ? !dIsPositive : dIsPositive;
    const dColor = dActuallyGood ? colors.successContrast : colors.error;
    const dBgColor = dActuallyGood
      ? `rgba(34, 197, 94, ${deltaBgTokens.success})`
      : `rgba(239, 68, 68, ${deltaBgTokens.error})`;

    const formatExtraDelta = () => {
      if (showRelative) {
        return `${d.deltaPercent >= 0 ? "+" : ""}${d.deltaPercent.toFixed(format?.decimals || 1)}%`;
      } else {
        return `${d.delta >= 0 ? "+" : ""}${Math.abs(d.delta).toLocaleString()}`;
      }
    };

    return (
      <div
        key={idx}
        role="button"
        tabIndex={0}
        onClick={toggleDeltaMode}
        onKeyDown={handleDeltaKeyDown}
        title="Click to toggle"
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: `${tokens.spacing.xs}px`,
          cursor: "pointer",
          userSelect: "none",
          padding: `${tokens.spacing.xs}px ${tokens.spacing.sm}px`,
          borderRadius: `${tokens.radii.sm}px`,
          backgroundColor: dBgColor,
          width: "fit-content",
          flexShrink: 0,
        }}
      >
        <span style={{ display: "flex", alignItems: "center", fontSize: `${tokens.delta.fontSize.pill}px`, fontWeight: 500, color: dColor }}>
          {dIsPositive ? <ArrowUp /> : <ArrowDown />}
          {formatExtraDelta()}
        </span>
        {d.label && (
          <span style={{ fontSize: `${tokens.delta.fontSize.label}px`, color: colors.muted }}>{d.label}</span>
        )}
      </div>
    );
  };

  // Render all deltas (primary + extra) with stacking
  const renderAllDeltas = () => {
    const allDeltas = [];

    // Primary delta
    allDeltas.push(
      <div key="primary">{renderDelta()}</div>
    );

    // Extra deltas
    if (extraDeltas && extraDeltas.length > 0) {
      extraDeltas.forEach((d, idx) => {
        allDeltas.push(renderSingleDelta(d, idx));
      });
    }

    if (allDeltas.length === 1) {
      return renderDelta();
    }

    return (
      <div style={{
        display: "flex",
        flexDirection: deltaStack === "vertical" ? "column" : "row",
        flexWrap: "wrap",
        gap: `${tokens.spacing.xs}px`,
        alignItems: deltaStack === "vertical" ? "flex-start" : "center",
      }}>
        {allDeltas}
      </div>
    );
  };

  // Render name section
  // Compute effective name margin
  const effectiveNameMargin = nameMarginBottom != null
    ? nameMarginBottom
    : (layout === "compact" || axis === "y" ? 0 : `${tokens.spacing.sm}px`);

  const renderName = () => (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: effectiveNameMargin,
        flexShrink: 0,
      }}
    >
      <div
        style={{
          fontSize: nameSize || `${sizes.name}px`,
          fontWeight: nameWeight ?? 500,
          color: nameColor || colors.muted,
          textTransform: nameTransform || "uppercase",
          letterSpacing: nameLetterSpacing || "0.05em",
        }}
      >
        {name}
      </div>
      {infoText && (
        <div
          title={infoText}
          style={{
            cursor: "help",
            color: colors.muted,
            display: "flex",
            alignItems: "center",
            opacity: infoHovered ? 1 : tokens.info.opacity,
            transition: `opacity ${tokens.transitions.fast}`,
          }}
          onMouseEnter={() => setInfoHovered(true)}
          onMouseLeave={() => setInfoHovered(false)}
        >
          <svg
            width={tokens.info.iconSize}
            height={tokens.info.iconSize}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </div>
      )}
    </div>
  );

  // Render value section
  const renderValue = (variant = "normal") => {
    // Use custom valueSize if provided, otherwise size scale with variant modifier
    let fontSize;
    if (valueSize) {
      fontSize = valueSize;
    } else {
      const baseSize = sizes.value;
      const variantMultiplier = variant === "large" ? 1.25 : variant === "small" ? 0.75 : 1;
      fontSize = `${Math.round(baseSize * variantMultiplier)}px`;
    }
    const effectiveValueColor = valueColor || colors.foreground;
    const effectiveValueWeight = valueWeight ?? 600;

    if (deltaFormat === "inline") {
      return (
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            gap: `${tokens.spacing.sm}px`,
            marginBottom: `${tokens.spacing.xs}px`,
            flexShrink: 0,
          }}
        >
          <span
            style={{
              fontSize,
              fontWeight: effectiveValueWeight,
              color: effectiveValueColor,
              lineHeight: 1,
            }}
          >
            {formatValue(value)}
          </span>
          <span
            role="button"
            tabIndex={0}
            onClick={toggleDeltaMode}
            onKeyDown={handleDeltaKeyDown}
            style={{
              display: "flex",
              alignItems: "center",
              fontSize: `${tokens.delta.fontSize.icon}px`,
              fontWeight: 500,
              color: deltaColor,
              cursor: "pointer",
            }}
            title="Click to toggle between relative and absolute change"
          >
            {isPositive ? <ArrowUp size={tokens.delta.fontSize.icon} /> : <ArrowDown size={tokens.delta.fontSize.icon} />}
            {formatDelta()}
          </span>
        </div>
      );
    }

    return (
      <div
        style={{
          fontSize,
          fontWeight: effectiveValueWeight,
          color: effectiveValueColor,
          marginBottom: deltaPosition === "right-of-value" ? 0 : `${tokens.spacing.xs}px`,
          lineHeight: 1,
          flexShrink: 0,
        }}
      >
        {formatValue(value)}
      </div>
    );
  };

  // Render chart section. compact=true skips outer margins (used by chart-focus).
  const renderChartSection = (chartHeight = "50px", compact = false) => {
    if (!showChart || !timeSeriesData || timeSeriesData.length === 0) return null;

    const yLabelsHtml = showYLabels;
    const xLabelsHtml = showXLabels;

    // HTML labels mode: chart with overlaid Y/X labels
    if (yLabelsHtml || xLabelsHtml) {
      const vals = timeSeriesData.map(d => d.value);
      const dataMin = Math.min(...vals);
      const dataMax = Math.max(...vals);

      const formatCompact = (val) => {
        const abs = Math.abs(val);
        if (abs >= 1e6) return (val / 1e6).toFixed(1) + "M";
        if (abs >= 1e3) return (val / 1e3).toFixed(1) + "K";
        if (abs < 1) return val.toFixed(2);
        if (abs < 100) return val.toFixed(1);
        return Math.round(val).toLocaleString();
      };

      const dataLen = timeSeriesData.length;

      // X labels: use explicit xLabels or auto-generate from data for axis="x"
      const resolvedXLabels = (xLabels && xLabels.length > 0)
        ? xLabels
        : (xLabelsHtml && dataLen > 0)
          ? (() => {
              const first = timeSeriesData[0].index;
              const last = timeSeriesData[dataLen - 1].index;
              if (dataLen > 2) {
                const midIdx = Math.floor(dataLen / 2);
                return [[0, first], [midIdx, timeSeriesData[midIdx].index], [dataLen - 1, last]];
              }
              return [[0, first], [dataLen - 1, last]];
            })()
          : null;
      const hasXRow = resolvedXLabels && resolvedXLabels.length > 0;

      const maxLabelText = formatCompact(dataMax);
      const minLabelText = formatCompact(effectiveYZero ? 0 : dataMin);

      const labelStyle = {
        fontSize: tokens.chart.yLabel.fontSize,
        color: isDark ? "#d4d4d4" : colors.muted,
        fontFamily: "system-ui, sans-serif",
        lineHeight: 1,
        userSelect: "none",
        whiteSpace: "nowrap",
      };

      if (!chartReady) {
        return (
          <div style={{
            ...(!compact && { marginTop: tokens.spacing.xs }),
            flexGrow: 1,
            // When card has fixed height, let flex fill; otherwise use explicit chartHeight
            ...(compact
              ? (chartHeight ? { height: chartHeight } : {})
              : (height ? {} : { height: chartHeight })),
            background: placeholderBg,
            borderRadius: `${tokens.radii.sm}px`,
          }} />
        );
      }

      return (
        <div style={{
          display: "grid",
          gridTemplateColumns: yLabelsHtml ? "1fr auto" : "1fr",
          gridTemplateRows: hasXRow ? "1fr auto" : "1fr",
          ...(!compact && { marginTop: tokens.spacing.xs }),
          flexGrow: 1,
          // When card has fixed height or compact without chartHeight, omit minHeight to let flex fill
          ...((height || (compact && !chartHeight)) ? {} : { minHeight: "30px" }),
          // When card has fixed height, let flex fill; otherwise use explicit chartHeight
          ...(compact
            ? (chartHeight ? { height: chartHeight } : {})
            : (height ? {} : { height: chartHeight })),
        }}>
          {/* Chart — row 1, col 1 */}
          <div style={{ minWidth: 0, position: "relative" }}>
            <ResponsiveContainer width="100%" height="100%">
              {renderChart()}
            </ResponsiveContainer>
            {/* Vertical grid lines (HTML overlay for gridX in labels mode) */}
            {Array.isArray(gridX) && gridX.map((idx, i) => {
              const pct = dataLen > 1 ? (idx / (dataLen - 1)) * 100 : 50;
              return (
                <div key={`vline-${i}`} style={{
                  position: "absolute",
                  left: `${pct}%`,
                  top: 0,
                  bottom: 0,
                  width: 0,
                  borderLeft: `1px dashed ${isDark ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.12)"}`,
                  pointerEvents: "none",
                }} />
              );
            })}
          </div>
          {/* Y-labels — row 1, col 2 (only when axis="y") */}
          {yLabelsHtml && (
            <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between", alignItems: "flex-end", paddingLeft: 4 }}>
              <span style={labelStyle}>{maxLabelText}</span>
              <span style={labelStyle}>{minLabelText}</span>
            </div>
          )}
          {/* X-labels — row 2, col 1 */}
          {hasXRow && (
            <div style={{ position: "relative", marginTop: 2, height: tokens.chart.yLabel.rowHeight, minWidth: 0 }}>
              {resolvedXLabels.map(([idx, label], i) => {
                const pct = dataLen > 1 ? (idx / (dataLen - 1)) * 100 : 50;
                const isFirst = pct <= 0;
                const isLast = pct >= 100;
                return (
                  <span key={i} style={{
                    ...labelStyle,
                    position: "absolute",
                    left: `${pct}%`,
                    transform: isFirst ? "none" : isLast ? "translateX(-100%)" : "translateX(-50%)",
                  }}>
                    {label}
                  </span>
                );
              })}
            </div>
          )}
        </div>
      );
    }

    // Standard mode
    // When axes are shown, enforce a minimum height so labels don't overwhelm the chart
    // But skip minHeight when card has fixed height - let chart shrink to fit
    const axesMinHeight = (showXAxis || showYAxis || showGrid) ? "100px" : "40px";
    const effectiveChartHeight = (showXAxis || showYAxis || showGrid) ? `max(${chartHeight}, 100px)` : chartHeight;
    // chartFill: extend chart to card edges with negative margins
    const containerStyle = compact ? {
      flexGrow: 1,
      height: effectiveChartHeight,
      width: "100%",
    } : chartFill ? {
      marginTop: `${tokens.spacing.sm}px`,
      marginBottom: `-${tokens.spacing.lg}px`,
      marginLeft: `-${tokens.spacing.lg}px`,
      marginRight: `-${tokens.spacing.lg}px`,
      flexGrow: 1,
      flexShrink: 1,
      minHeight: height ? 0 : axesMinHeight,
      height: height ? "auto" : effectiveChartHeight,
    } : {
      marginTop: `${tokens.spacing.md}px`,
      marginBottom: "2px",
      flexGrow: 1,
      flexShrink: 1,
      minHeight: height ? 0 : axesMinHeight,
      height: height ? "auto" : effectiveChartHeight,
    };

    // Show placeholder while chart loads
    if (!chartReady) {
      return (
        <div style={{
          ...containerStyle,
          background: placeholderBg,
          borderRadius: chartFill ? 0 : `${tokens.radii.sm}px`,
        }} />
      );
    }

    return (
      <div style={containerStyle}>
        <ResponsiveContainer width="100%" height="100%">
          {renderChart()}
        </ResponsiveContainer>
      </div>
    );
  };

  // Expand/detail button
  const renderDetailButton = () => {
    if (!showDetailButton) return null;
    return (
      <div
        role="button"
        tabIndex={0}
        onClick={(e) => { e.stopPropagation(); setIsExpanded(!isExpanded); }}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setIsExpanded(!isExpanded); } }}
        title={isExpanded ? "Collapse detail" : "Expand detail"}
        style={{
          position: "absolute",
          top: `${tokens.spacing.sm}px`,
          right: infoText ? `${tokens.spacing.sm + tokens.info.iconSize + tokens.spacing.sm}px` : `${tokens.spacing.sm}px`,
          cursor: "pointer",
          color: colors.muted,
          opacity: isExpanded ? 1 : tokens.detail.collapsedOpacity,
          transition: `opacity ${tokens.transitions.fast}`,
          padding: `${tokens.detail.buttonPadding}px`,
          borderRadius: `${tokens.radii.sm}px`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: tokens.detail.zIndex,
        }}
        onMouseEnter={(e) => e.currentTarget.style.opacity = 1}
        onMouseLeave={(e) => e.currentTarget.style.opacity = isExpanded ? 1 : tokens.detail.collapsedOpacity}
      >
        <svg width={tokens.detail.buttonSize} height={tokens.detail.buttonSize} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          {isExpanded ? (
            <>
              <polyline points="4 14 10 14 10 20" />
              <polyline points="20 10 14 10 14 4" />
              <line x1="14" y1="10" x2="21" y2="3" />
              <line x1="3" y1="21" x2="10" y2="14" />
            </>
          ) : (
            <>
              <polyline points="15 3 21 3 21 9" />
              <polyline points="9 21 3 21 3 15" />
              <line x1="21" y1="3" x2="14" y2="10" />
              <line x1="3" y1="21" x2="10" y2="14" />
            </>
          )}
        </svg>
      </div>
    );
  };

  // Detail expanded section with professional chart
  const renderDetailSection = () => {
    if (!isExpanded || !timeSeriesData || timeSeriesData.length === 0) return null;

    // Compute stats
    const values = timeSeriesData.map(d => d.value);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const avg = values.reduce((a, b) => a + b, 0) / values.length;
    const latest = values[values.length - 1];

    return (
      <div style={{
        marginTop: `${tokens.spacing.md}px`,
        borderTop: `1px solid ${colors.border}`,
        paddingTop: `${tokens.spacing.md}px`,
        overflow: "hidden",
        transition: `max-height ${tokens.detail.transition}, opacity ${tokens.detail.transition}`,
      }}>
        {/* Stats row */}
        <div style={{
          display: "flex",
          gap: `${tokens.spacing.lg}px`,
          marginBottom: `${tokens.spacing.md}px`,
          flexWrap: "wrap",
        }}>
          {[
            { label: "Min", val: min },
            { label: "Max", val: max },
            { label: "Avg", val: avg },
            { label: "Latest", val: latest },
          ].map(({ label, val }) => (
            <div key={label} style={{ display: "flex", flexDirection: "column" }}>
              <span style={{ fontSize: `${tokens.detail.statLabelFontSize}px`, color: colors.muted, textTransform: "uppercase", letterSpacing: "0.05em", fontWeight: 500 }}>{label}</span>
              <span style={{ fontSize: `${tokens.detail.statValueFontSize}px`, fontWeight: 600, color: colors.foreground }}>{formatValue(val)}</span>
            </div>
          ))}
        </div>
        {/* Detailed chart with axes */}
        <div style={{ height: `${detailHeight}px`, width: "100%" }}>
          <ResponsiveContainer width="100%" height="100%">
            {renderChart(true)}
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  // Build resolved card style (combining props with computed values)
  const resolvedCardStyle = {
    ...getBackgroundStyle(),
    ...getBorderStyle(),
    borderRadius: borderStyle === "left-accent" || borderStyle === "top-accent" ? borderRadius : borderRadius,
    padding: cardPadding || (axis === "y" ? `${tokens.spacing.md}px ${tokens.spacing.md}px ${tokens.spacing.sm}px ${tokens.spacing.md}px` : `${tokens.spacing.lg}px`),
    boxShadow: getShadowStyle(),
    fontFamily: tokens.fontFamily,
    maxWidth: "100%",
    height: height || "auto",
    display: "flex",
    overflow: "hidden",
    position: showDetailButton ? "relative" : undefined,
    transition: `box-shadow ${tokens.transitions.default}, transform ${tokens.transitions.default}`,
    transform: isCardHovered && shadowStyle !== "inset" ? `translateY(${tokens.hover.translateY}px)` : "translateY(0)",
  };

  // Render based on layout
  const renderLayout = () => {
    switch (layout) {
      case "horizontal":
        return (
          <div style={{ ...resolvedCardStyle, flexDirection: "column" }}>
            {renderDetailButton()}
            <div style={{ display: "flex", flexDirection: "row", alignItems: "center", gap: `${tokens.spacing.lg}px` }}>
              <div style={{ flex: "0 0 auto" }}>
                {renderName()}
                {renderValue("normal")}
                {renderAllDeltas()}
              </div>
              {showChart && timeSeriesData && timeSeriesData.length > 0 && (
                <div style={{ flex: 1, minWidth: 0, height: tokens.layouts.horizontal.chartHeight }}>
                  {chartReady ? (
                    <ResponsiveContainer width="100%" height="100%">
                      {renderChart()}
                    </ResponsiveContainer>
                  ) : (
                    <div style={{ width: "100%", height: "100%", background: placeholderBg, borderRadius: `${tokens.radii.sm}px` }} />
                  )}
                </div>
              )}
            </div>
            {renderDetailSection()}
          </div>
        );

      case "value-focus":
        return (
          <div style={{ ...resolvedCardStyle, flexDirection: "column" }}>
            {renderName()}
            {renderValue("large")}
            {renderAllDeltas()}
            {showChart && timeSeriesData && timeSeriesData.length > 0 && (
              <div style={{ marginTop: `${tokens.spacing.md}px`, height: tokens.layouts.valueFocus.chartHeight, opacity: tokens.layouts.valueFocus.chartOpacity }}>
                {chartReady ? (
                  <ResponsiveContainer width="100%" height="100%">
                    {renderChart()}
                  </ResponsiveContainer>
                ) : (
                  <div style={{ width: "100%", height: "100%", background: placeholderBg, borderRadius: `${tokens.radii.sm}px` }} />
                )}
              </div>
            )}
          </div>
        );

      case "chart-focus": {
        const pos = overlayPosition === "auto" ? "bottom-left" : overlayPosition;
        const isTop = pos.startsWith("top");
        const isRight = pos.endsWith("right");
        const effectiveOverlayOpacity = overlayOpacity != null
          ? overlayOpacity
          : (isDark ? tokens.layouts.chartFocus.bgOpacity.dark : tokens.layouts.chartFocus.bgOpacity.light);
        return (
          <div style={{ ...resolvedCardStyle, flexDirection: "column", position: "relative" }}>
            {/* Value overlay (hidden when showHeader=false) */}
            {showHeader && (
            <div style={{
              position: "absolute",
              ...(isTop ? { top: `${tokens.spacing.md}px` } : { bottom: `${tokens.spacing.md}px` }),
              ...(isRight ? { right: `${tokens.spacing.md}px` } : { left: `${tokens.spacing.md}px` }),
              zIndex: 2,
              background: isDark ? `rgba(10,10,10,${effectiveOverlayOpacity})` : `rgba(255,255,255,${effectiveOverlayOpacity})`,
              padding: `${tokens.spacing.sm}px ${tokens.spacing.md}px`,
              borderRadius: `${tokens.radii.md}px`,
              backdropFilter: "blur(4px)",
              WebkitBackdropFilter: "blur(4px)",
              ...(isRight ? { textAlign: "right" } : {}),
            }}>
              <div style={{ fontSize: `${tokens.layouts.chartFocus.overlayNameFontSize}px`, fontWeight: 500, color: colors.muted, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                {name}
              </div>
              <div style={{ fontSize: `${tokens.layouts.chartFocus.overlayValueFontSize}px`, fontWeight: 600, color: colors.foreground, lineHeight: 1.2 }}>
                {formatValue(value)}
              </div>
              {valueBefore !== null && valueBefore !== undefined && (
                <div
                  role="button"
                  tabIndex={0}
                  onClick={toggleDeltaMode}
                  onKeyDown={handleDeltaKeyDown}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: `${tokens.layouts.chartFocus.overlayDeltaGap}px`,
                    marginTop: `${tokens.layouts.chartFocus.overlayDeltaMarginTop}px`,
                    fontSize: `${tokens.layouts.chartFocus.overlayDeltaFontSize}px`,
                    fontWeight: 500,
                    color: deltaColor,
                    cursor: "pointer",
                  }}
                  title="Click to toggle"
                >
                  {isPositive ? <ArrowUp size={tokens.layouts.chartFocus.overlayArrowSize} /> : <ArrowDown size={tokens.layouts.chartFocus.overlayArrowSize} />}
                  <span>{formatDelta()}</span>
                  {deltaLabel && (
                    <span style={{ color: colors.muted, fontWeight: 400 }}>{deltaLabel}</span>
                  )}
                </div>
              )}
            </div>
            )}
            {/* Chart - when card has explicit height, let flex fill remaining space */}
            {renderChartSection(height ? null : tokens.layouts.chartFocus.defaultHeight, true)}
          </div>
        );
      }

      case "mini": {
        const isSelected = selectable && selected === name;
        const miniClickable = selectable && onSelect;
        const useGrid = miniColumns && miniColumns !== "auto";
        return (
          <div style={{
            display: useGrid ? "grid" : "flex",
            ...(useGrid
              ? { gridTemplateColumns: miniColumns, alignItems: "center" }
              : { flexDirection: "row", alignItems: "center" }),
            padding: tokens.layouts.mini.padding,
            fontFamily: tokens.fontFamily,
            borderBottom: isSelected
              ? `1px solid ${isDark ? "rgba(59,130,246,0.3)" : "rgba(59,130,246,0.2)"}`
              : `1px solid ${isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)"}`,
            background: isSelected
              ? (isDark ? "rgba(59,130,246,0.10)" : "rgba(59,130,246,0.06)")
              : "transparent",
            gap: `${tokens.spacing.md}px`,
            height: height || tokens.layouts.mini.height,
            boxSizing: "border-box",
            cursor: miniClickable ? "pointer" : "default",
            borderLeft: isSelected ? `3px solid #3b82f6` : "3px solid transparent",
            transition: `background ${tokens.transitions.fast}, border-color ${tokens.transitions.fast}`,
          }}
          onClick={() => { if (miniClickable) onSelect(name); }}
          >
            {/* Name - left */}
            <div style={{
              ...(useGrid ? {} : { flex: `0 0 ${tokens.layouts.mini.nameWidth}` }),
              minWidth: 0,
            }}>
              <div style={{
                fontSize: `${tokens.layouts.mini.nameFontSize}px`,
                fontWeight: 600,
                color: colors.foreground,
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
                lineHeight: 1.2,
              }}>
                {name}
              </div>
            </div>
            {/* Chart - center (pointerEvents none so row click works through chart) */}
            {showChart && timeSeriesData && timeSeriesData.length > 0 && (
              <div style={{ ...(useGrid ? {} : { flex: 1 }), height: "100%", maxHeight: maxChartHeight || tokens.layouts.mini.chartMaxHeight, minWidth: 0, alignSelf: "center", pointerEvents: "none" }}>
                {chartReady ? (
                  <ResponsiveContainer width="100%" height="100%">
                    {renderChart()}
                  </ResponsiveContainer>
                ) : (
                  <div style={{ width: "100%", height: "100%", background: placeholderBg, borderRadius: "2px" }} />
                )}
              </div>
            )}
            {/* Value + delta - right */}
            <div style={{
              ...(useGrid ? {} : { flex: "0 0 auto" }),
              textAlign: "right",
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-end",
            }}>
              <span style={{
                fontSize: `${tokens.layouts.mini.valueFontSize}px`,
                fontWeight: 600,
                color: colors.foreground,
                lineHeight: 1.2,
              }}>
                {formatValue(value)}
              </span>
              <span
                role="button"
                tabIndex={0}
                onClick={(e) => { e.stopPropagation(); toggleDeltaMode(); }}
                onKeyDown={handleDeltaKeyDown}
                style={{
                  display: "flex",
                  alignItems: "center",
                  fontSize: `${tokens.layouts.mini.deltaFontSize}px`,
                  fontWeight: 500,
                  color: deltaColor,
                  cursor: "pointer",
                  lineHeight: 1.2,
                }}
                title="Click to toggle"
              >
                {isPositive ? <ArrowUp size={tokens.layouts.mini.arrowSize} /> : <ArrowDown size={tokens.layouts.mini.arrowSize} />}
                {formatDelta()}
              </span>
            </div>
          </div>
        );
      }

      case "compact":
        return (
          <div style={{ ...resolvedCardStyle, flexDirection: "row", alignItems: "center", padding: `${tokens.spacing.sm}px ${tokens.spacing.md}px` }}>
            <div style={{ flex: 1, display: "flex", alignItems: "baseline", gap: `${tokens.spacing.sm}px` }}>
              <span style={{ fontSize: `${tokens.layouts.compact.nameFontSize}px`, fontWeight: 500, color: colors.muted, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                {name}
              </span>
              <span style={{ fontSize: `${tokens.layouts.compact.valueFontSize}px`, fontWeight: 600, color: colors.foreground }}>
                {formatValue(value)}
              </span>
              <span
                role="button"
                tabIndex={0}
                onClick={toggleDeltaMode}
                onKeyDown={handleDeltaKeyDown}
                style={{
                  display: "flex",
                  alignItems: "center",
                  fontSize: `${tokens.layouts.compact.deltaFontSize}px`,
                  fontWeight: 500,
                  color: deltaColor,
                  cursor: "pointer",
                }}
                title="Click to toggle"
              >
                {isPositive ? <ArrowUp size={tokens.layouts.compact.arrowSize} /> : <ArrowDown size={tokens.layouts.compact.arrowSize} />}
                {formatDelta()}
              </span>
            </div>
            {showChart && timeSeriesData && timeSeriesData.length > 0 && (
              <div style={{ width: tokens.layouts.compact.chartWidth, height: tokens.layouts.compact.chartHeight }}>
                {chartReady ? (
                  <ResponsiveContainer width="100%" height="100%">
                    {renderChart()}
                  </ResponsiveContainer>
                ) : (
                  <div style={{ width: "100%", height: "100%", background: placeholderBg, borderRadius: "2px" }} />
                )}
              </div>
            )}
          </div>
        );

      case "vertical":
      default:
        // Handle delta position
        const deltasEl = renderAllDeltas();
        return (
          <div style={{ ...resolvedCardStyle, flexDirection: "column" }}
            onMouseEnter={() => setIsCardHovered(true)}
            onMouseLeave={() => setIsCardHovered(false)}
          >
            {renderDetailButton()}
            {renderName()}
            {deltaPosition === "right-of-value" ? (
              <div style={{ display: "flex", alignItems: "center", gap: `${tokens.spacing.sm}px`, flexWrap: "wrap" }}>
                {renderValue()}
                {deltasEl}
              </div>
            ) : (
              renderValue()
            )}
            {deltaPosition === "below-value" && deltasEl}
            {!isExpanded && renderChartSection()}
            {renderDetailSection()}
          </div>
        );
    }
  };

  // Wrap with mouse handlers for layouts that need it
  if (layout === "vertical") {
    return renderLayout();
  }

  return (
    <div
      onMouseEnter={() => setIsCardHovered(true)}
      onMouseLeave={() => setIsCardHovered(false)}
    >
      {renderLayout()}
    </div>
  );
};

export default KpiCard;
