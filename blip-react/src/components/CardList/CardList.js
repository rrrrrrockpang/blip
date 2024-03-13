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

  return (
    <div id="scrollableDiv" style={{ width: '100%', height: '80vh', overflowY: 'auto', padding: '20px'}}>
        <Masonry
        breakpointCols={breakpointColumnsObj}
        className="my-masonry-grid"
        columnClassName="my-masonry-grid_column"
        >
        {cards.map((card, index) => (
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
