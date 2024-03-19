import React from "react";
import Card from "../Card/Card"; // Import your Card component
import Masonry from "react-masonry-css";
import "./CardList.css";

export default function CardList({ cards, onAdd, onRemove, onContribute }) {
  const breakpointColumnsObj = {
    default: 4,  // 4 columns by default
    1100: 3,
    700: 2,
    500: 1
  };

  // Filter cards that meet the criteria: non-empty and non-'none' aspect, and summary with 5 or more words
  const filteredCards = cards.filter(card => {
    const isAspectValid = card.label || card.label.toLowerCase() !== 'none' || card.label.length > 0;
    const isSummaryValid = card.gpt_summary && card.gpt_summary.split(' ').length >= 5;
    return isAspectValid && isSummaryValid;
  });

  return (
    <div id="scrollableDiv" style={{ width: '100%', height: '80vh', overflowY: 'auto', padding: '20px'}}>
        <Masonry
        breakpointCols={breakpointColumnsObj}
        className="my-masonry-grid"
        columnClassName="my-masonry-grid_column"
        >
        {filteredCards.map((card, index) => (
            <div key={index}>
            <Card 
                {...card} 
                onAdd={(e) => onAdd(card, e.target)}
                onRemove={() => onRemove(card)}
                onContribute={() => onContribute(card)}
            />
            </div>
        ))}
        </Masonry>
    </div>
  );
}
