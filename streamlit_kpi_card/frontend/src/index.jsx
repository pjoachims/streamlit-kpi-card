import React from "react";
import { createRoot } from "react-dom/client";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import KpiCard from "./KpiCard";

class StreamlitKpiCard extends StreamlitComponentBase {
  constructor(props) {
    super(props);
    this.containerRef = React.createRef();
    this.state = { searchQuery: "", expandedRows: {} };
  }

  resolveTheme(themeProp) {
    if (themeProp === "auto") {
      return this.props.theme?.base === "dark" ? "dark" : "light";
    }
    return themeProp;
  }

  renderSingleCard() {
    const {
      name,
      value,
      valueBefore,
      delta,
      deltaPercent,
      relativeChange,
      isInverse,
      timeSeriesData,
      averageValue,
      format,
      extraDeltas,
      // Style dicts
      cardStyle,
      chartStyle,
      textStyle,
      deltaStyle,
      // Layout
      layout,
      size,
      theme,
    } = this.props.args;

    return (
      <KpiCard
        name={name}
        value={value}
        valueBefore={valueBefore}
        delta={delta}
        deltaPercent={deltaPercent}
        relativeChange={relativeChange}
        isInverse={isInverse}
        timeSeriesData={timeSeriesData}
        averageValue={averageValue}
        format={format}
        extraDeltas={extraDeltas}
        // Style dicts
        cardStyle={cardStyle || {}}
        chartStyle={chartStyle || {}}
        textStyle={textStyle || {}}
        deltaStyle={deltaStyle || {}}
        // Layout
        layout={layout}
        size={size}
        theme={this.resolveTheme(theme)}
      />
    );
  }

  renderCardComponent(card, idx, { selectable, selected, onSelect, miniColumns, isExpanded, onToggleExpand } = {}) {
    return (
      <KpiCard
        key={idx}
        name={card.name}
        value={card.value}
        valueBefore={card.valueBefore}
        delta={card.delta}
        deltaPercent={card.deltaPercent}
        relativeChange={card.relativeChange}
        isInverse={card.isInverse}
        timeSeriesData={card.timeSeriesData}
        averageValue={card.averageValue}
        format={card.format}
        extraDeltas={card.extraDeltas}
        // Style dicts
        cardStyle={card.cardStyle || {}}
        chartStyle={card.chartStyle || {}}
        textStyle={card.textStyle || {}}
        deltaStyle={card.deltaStyle || {}}
        // Layout
        layout={card.layout}
        size={card.size}
        theme={this.resolveTheme(card.theme)}
        // Multi-card props
        selectable={selectable}
        selected={selected}
        onSelect={onSelect}
        miniColumns={miniColumns}
        isExpanded={isExpanded}
        onToggleExpand={onToggleExpand}
      />
    );
  }

  renderMultiCards() {
    const { cards, columns = 4, gap = "12px", rowGap, columnGap, gridMode, gridRows, miniColumns, selectable, selected, searchable } = this.props.args;
    const { searchQuery } = this.state;

    // Resolve gaps: specific gaps override general gap
    const vGap = rowGap || gap;
    const hGap = columnGap || gap;

    const onSelect = selectable ? (cardName) => Streamlit.setComponentValue(cardName) : undefined;
    const selectProps = { selectable, selected, onSelect, miniColumns };

    // Client-side search filter
    const matchesSearch = (card) => {
      if (!searchable || !searchQuery) return true;
      return card.name.toLowerCase().includes(searchQuery.toLowerCase());
    };

    const resolvedTheme = this.resolveTheme(this.props.args.cards?.[0]?.theme || this.props.args.gridRows?.[0]?.[0]?.theme || "light");
    const isDark = resolvedTheme === "dark";

    const searchInput = searchable ? (
      <div style={{ marginBottom: gap, position: "relative" }}>
        <svg
          width="14" height="14" viewBox="0 0 24 24" fill="none"
          stroke={isDark ? "#a3a3a3" : "#737373"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
          style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", pointerEvents: "none" }}
        >
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => this.setState({ searchQuery: e.target.value })}
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "8px 10px 8px 32px",
            fontSize: "13px",
            border: `1px solid ${isDark ? "#262626" : "#e5e5e5"}`,
            borderRadius: "8px",
            background: isDark ? "#0a0a0a" : "#ffffff",
            color: isDark ? "#fafafa" : "#171717",
            outline: "none",
            fontFamily: "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
          }}
        />
      </div>
    ) : null;

    // Grid mode: render rows with flexible columns per row
    if (gridMode && gridRows) {
      const filteredRows = gridRows.map(row => row.filter(matchesSearch));
      return (
        <div>
          {searchInput}
          <div style={{ display: "flex", flexDirection: "column", gap: vGap }}>
            {filteredRows.map((row, rowIdx) => {
              if (row.length === 0) return null;
              const rowExpanded = !!this.state.expandedRows[`grid-${rowIdx}`];
              const toggleRow = () => this.setState(prev => ({
                expandedRows: { ...prev.expandedRows, [`grid-${rowIdx}`]: !prev.expandedRows[`grid-${rowIdx}`] }
              }));
              return (
                <div
                  key={rowIdx}
                  style={{
                    display: "grid",
                    gridTemplateColumns: `repeat(${row.length}, 1fr)`,
                    gap: hGap,
                  }}
                >
                  {row.map((card, cardIdx) => this.renderCardComponent(card, `${rowIdx}-${cardIdx}`, { ...selectProps, isExpanded: rowExpanded, onToggleExpand: toggleRow }))}
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    // Flat mode: single grid with fixed columns
    if (!cards || cards.length === 0) {
      return null;
    }

    const filteredCards = cards.filter(matchesSearch);

    // Mini layout: vertical stack (Apple Stocks style)
    const isMini = filteredCards.length > 0 && filteredCards[0].layout === "mini";
    if (isMini) {
      return (
        <div>
          {searchInput}
          <div style={{ display: "flex", flexDirection: "column" }}>
            {filteredCards.map((card, idx) => this.renderCardComponent(card, idx, selectProps))}
          </div>
        </div>
      );
    }

    return (
      <div>
        {searchInput}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: `repeat(${columns}, 1fr)`,
            rowGap: vGap,
            columnGap: hGap,
          }}
        >
          {filteredCards.map((card, idx) => {
            const rowIdx = Math.floor(idx / columns);
            const rowExpanded = !!this.state.expandedRows[`flat-${rowIdx}`];
            const toggleRow = () => this.setState(prev => ({
              expandedRows: { ...prev.expandedRows, [`flat-${rowIdx}`]: !prev.expandedRows[`flat-${rowIdx}`] }
            }));
            return this.renderCardComponent(card, idx, { ...selectProps, isExpanded: rowExpanded, onToggleExpand: toggleRow });
          })}
        </div>
      </div>
    );
  }

  render() {
    const { multiCardMode } = this.props.args;

    return (
      <div ref={this.containerRef} style={{ padding: "4px" }}>
        {multiCardMode ? this.renderMultiCards() : this.renderSingleCard()}
      </div>
    );
  }

  componentDidMount() {
    this.updateFrameHeight();
    // ResizeObserver for dynamic height changes (e.g. detail expand/collapse)
    if (this.containerRef.current && typeof ResizeObserver !== "undefined") {
      this._resizeObserver = new ResizeObserver(() => this.updateFrameHeight());
      this._resizeObserver.observe(this.containerRef.current);
    }
  }

  componentDidUpdate() {
    this.updateFrameHeight();
  }

  componentWillUnmount() {
    if (this._resizeObserver) {
      this._resizeObserver.disconnect();
    }
  }

  updateFrameHeight() {
    const height = this.containerRef.current?.offsetHeight || 100;
    Streamlit.setFrameHeight(height + 8);
  }
}

const StreamlitKpiCardWrapped = withStreamlitConnection(StreamlitKpiCard);

const container = document.getElementById("root");
if (container) {
  const root = createRoot(container);
  root.render(<StreamlitKpiCardWrapped />);
}
