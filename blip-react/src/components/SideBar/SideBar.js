import React, { useState } from 'react';
import Card from '../Card/Card';
import './SideBar.css'; 
import {
  createStyles,
  Accordion,
  Card as MantineCard,
  rem,
  Text,
  Badge,
  Group,
  Anchor,
  ActionIcon,
} from '@mantine/core';

const useStyles = createStyles((theme) => ({
  root: {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
      // borderRadius: theme.radius.sm,
      borderTopColor: theme.colors.gray[3],
      borderTopWidth: rem(1),
      borderTopStyle: 'solid',
    },
  
  item: {
  backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
  border: `${rem(1)} solid transparent`,
  borderRadius: '0px',
  borderBottomColor: theme.colors.gray[3],
  position: 'relative',
  zIndex: 0,
  transition: 'transform 150ms ease',

      '&[data-active]': {
          transform: 'scale(1.03)',
          backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.white,
          boxShadow: theme.shadows.md,
          borderColor: theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[2],
          borderRadius: theme.radius.md,
          zIndex: 1,      
      },
  },
  
  chevron: {
      '&[data-rotate]': {
          transform: 'rotate(-90deg)',
      },
  },
  bookmark: {
    background: theme.colors.gray[0],
    marginTop: rem(50),
    position: '-webkit-sticky', /* For Safari */
    position: 'sticky',
    top: 0,
    // width: '24vw',
    // height: '90vh',
    width: 'auto',
    height: 'auto',
    maxHeight: '100vh',
    overflowY: 'auto',
  },

  title: {
    fontFamily: 'DM Sans',
    fontWeight: 600,
    fontSize: '18px',
    marginTop: '10px',
  },

  cardTitle: {
      fontFamily: 'DM Sans',
      fontSize: '0.85rem',
      fontWeight: 600,
  },

  cardText: {
      fontFamily: 'DM Sans',
      fontSize: '0.8rem',
      color: '#777',
      textAlign: 'left',
  }
}));

const Sidebar = ({ isOpen, onClose, content }) => {
  const { classes, theme } = useStyles();

  const [input, setInput] = useState('');
  const [cardComments, setCardComments] = useState({});

  const handleChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    

    // call /create and submit the comment to the backend
    console.log("submitting comments");
    try {
      fetch(
        "https://blip.labinthewild.org/api/create",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          name: content.title,
          title: content.title,
          message: input,
          timestamp: new Date().toISOString()
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          setCardComments(prevComments => ({
            ...prevComments,
            [content.title]: [...(prevComments[content.title] || []), input]
          }));
          setInput('');
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!isOpen) return <p>Please select a card on the left</p>;

  const renderCardContent = (content) => {
    if (!content) return <p>Please select a card on the left</p>;
    if (typeof content === 'object') return <Card {...content} />;
    return content;
  };

  return (
    // <div className="sidebar" style={{ margin: 2}}>
    <MantineCard withBorder radius="md" className={classes.bookmark} style={{ margin: 2}}>
      {/* <button onClick={onClose} className="close-button">Close</button> */}
      <form onSubmit={handleSubmit}>
        {/* Welcome message and input field */}
        <Text className={classes.title}>Share Your Story</Text>

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
    {/* </div> */}
    </MantineCard>
  );
};

export default Sidebar;
