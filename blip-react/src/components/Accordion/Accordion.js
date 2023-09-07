import React from 'react';
import Card from '../Card/Card';
import "./Accordion.css"

function Accordion({ cardsInList, onRemove }) {
    return (
        <div className="accordion-section">
            <h3 className="accordion-title">Bookmarked Articles</h3>
            <div className="accordion" id="cardsAccordion">
                {cardsInList.map((card, index) => (
                    <div className="card" key={index}>
                        <div className="card-header" id={`heading${index}`}>
                            <h5 className="mb-0">
                                <button 
                                    className="btn btn-link" 
                                    type="button" 
                                    data-toggle="collapse" 
                                    data-target={`#collapse${index}`} 
                                    aria-expanded="true" 
                                    aria-controls={`collapse${index}`}
                                    style={{textDecoration: 'none', textAlign: 'left'}}
                                >
                                        {card.title}
                                </button>
                            </h5>
                        </div>
                        <div id={`collapse${index}`} className="collapse" aria-labelledby={`heading${index}`} data-parent="#cardsAccordion">
                            <div className="card-body">
                                <Card {...card}  mode="accordion" onRemove={() => onRemove(card)} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Accordion;
