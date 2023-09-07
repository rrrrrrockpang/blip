// import Card from '../Card/Card';
// import Masonry from 'masonry-layout';
// import React, { useEffect } from 'react';   
// import "./CardList.css"

// function CardList({ cards, onAdd, onRemove }) {
//     useEffect(() => {
//         var msnry = new Masonry('#allcards');
//         msnry.layout();
//     }, [cards]);


//     return (
//         <div id="allcards" className="card-list row">
//         {cards.map((card, index) => (
//             <div key={index} className="col-md-3 mb-3">
//             <Card 
//                 {...card} 
//                 onAdd={(e) => {
//                     onAdd(card, e.target)}} 
//                 onRemove={() => onRemove(card)}
//             />
//             </div>
//         ))}
//         </div>
//     );
// }
import React from "react";
import Card from "../Card/Card"; // Import your Card component
import Masonry from "react-masonry-css";
import "./CardList.css";

export default function CardList({ cards, onAdd, onRemove }) {
  const breakpointColumnsObj = {
    default: 4,  // 4 columns by default
    1100: 3,
    700: 2,
    500: 1
  };

  return (
    <div id="scrollableDiv" style={{ width: '100%', height: '80vh', overflowY: 'auto' }}>
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
            />
            </div>
        ))}
        </Masonry>
    </div>
  );
}
