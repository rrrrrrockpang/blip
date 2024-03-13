import React, { useState } from 'react';
import Card from '../Card/Card';
import './SideBar.css'; // Import the CSS file here

const Sidebar = ({ isOpen, onClose, content }) => {
  const [input, setInput] = useState('');
  const [cardComments, setCardComments] = useState({});

  const handleChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setCardComments(prevComments => ({
      ...prevComments,
      [content.title]: [...(prevComments[content.title] || []), input]
    }));
    setInput('');
  };

  if (!isOpen) return <p>Please select a card on the left</p>;

  const renderCardContent = (content) => {
    if (!content) return <p>Please select a card on the left</p>;
    if (typeof content === 'object') return <Card {...content} />;
    return content;
  };

  return (
    <div className="sidebar" style={{ margin: 2}}>
      {/* <button onClick={onClose} className="close-button">Close</button> */}
      <form onSubmit={handleSubmit}>
        {/* Welcome message and input field */}
        <label htmlFor="input" style={{ display: 'block', fontWeight: 'bold' }}>
          <h4><strong>Share Your Story</strong></h4>
        </label>

        <p>
          This story might resonate with your own experiences. If it does, we'd love to hear it!
        </p>
        
        {/* Render card content */}
        {renderCardContent(content)}

        <textarea
          value={input}
          onChange={handleChange}
          placeholder="Share your experience..."
          className="textarea"
        />

        <button type="submit" className="submit-button">Submit</button>

        {cardComments[content.title] && (
          <div className="comments-section">
            <p><strong>What other people have said?</strong></p>
            <ul>
              {cardComments[content.title].map((comment) => (
                <div className="comment-box">{comment}</div> /* Apply the new class here */
              ))}
            </ul>
          </div>
        )}

      </form>
    </div>
  );
};

export default Sidebar;
