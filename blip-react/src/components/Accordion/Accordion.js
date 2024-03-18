import React from 'react';
import Card from '../Card/Card';
import "./Accordion.css";

import CHI_LOGO from '../../assets/CHI.png';  
import FUTURISM_LOGO from '../../assets/Futurism.png';  
import MIT_TECH_REVIEW_LOGO from '../../assets/MIT Tech Review.png';
import TechCrunch from '../../assets/TechCrunch.png';
import The_Verge from '../../assets/The Verge.png';
import WIRED from '../../assets/Wired.png'; 

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

import {
    IconLink,
    IconBackspaceFilled,
} from '@tabler/icons-react';


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


function Bookmarks({ cardsInList, onRemove }) {

    const { classes, theme } = useStyles();

    const getCardHeaderColor = (aspectLabel) => {
        switch(aspectLabel) {
          case 'economy': 
            return "#cfd8dc";
          case 'equality & justice':
            return "#f8bbd0";
          case 'health & wellbeing':
            return "#b3e5fc";
          case 'access to information & discourse':
            return "#e6ee9c";  
          case 'politics':
            return "#ffcc80";
          case 'power dynamics':
            return "#ef9a9a";
          case 'security & privacy':
            return "#fff59d";
            // "";
          case 'social norms & relationship':
            return "#e1bee7";
          case 'user experience':
            return "#d1c4e9";
          case 'environment & sustainability':
            return "#aed581";
          default:
            return 'bg-secondary';  // Default color for unknown domains
        }
      };

    const condenseSector = (sector) => {
        switch(sector) {
            case 'Social Media':
                return 'Social';
            case 'Voice Assistant':
                return 'Voice';
            case 'Augmented/Virtual Reality':
                return 'AR/VR';
            case 'Computer Vision':
                return 'CV';
            case 'Robotics':
                return 'Robot';
            case 'Mobile Technology':
                return 'Mobile';
            case 'AI Decision-Making':
                return 'AI';
            case 'Neuroscience':
                return 'Neuro';
            case 'Computational Biology':
                return 'Comp Bio';
            case 'Ubiquitous Computing':
                return 'UbiComp';
        }
    };

    const getMagazineLogo = (magazine) => {
        switch(magazine) {
          case 'CHI':
            return CHI_LOGO;
          case 'Futurism':
            return FUTURISM_LOGO;
          case 'MIT Tech Review':
            return MIT_TECH_REVIEW_LOGO;
          case 'TechCrunch':
            return TechCrunch;
          case 'The Verge':
            return The_Verge;
          case 'Wired':
            return WIRED;
          default:
            return 'bg-secondary';  // Default color for unknown domains
        }
      };

    // const renderCardContent = (content) => {
    //   if (!content) return <p>Please select a card on the left</p>;
    //   if (typeof content === 'object') return <Card {...content} />;
    //   return content;
    // };

    const renderAccordian = (content) => {
      // if (!content) return <p>Please bookmark any cards of your interest!</p>;
      // if (content.length === 0) return <p>Please bookmark any cards of your interest!</p>;
      if (typeof content === 'object') {
        return (
                <Accordion
                  maw={420}
                  mx="auto"
                  mt="xl"
                  variant="filled"
                  defaultValue="customization"
                  classNames={classes}
                  className={classes.root}>
                {content.map((card, index) => (
                  <Accordion.Item value={`heading${index}`}>
                  <Accordion.Control>
                      <Text lineClamp={2}
                          className={classes.cardTitle}
                      >
                          {card.title}
                      </Text>
                      
                          <Badge
                              radius="sm"
                              color="dark"
                              variant="outline"
                              size="xs"
                              mr={3}
                          >
                              {condenseSector(card.sector)}
                          </Badge>
                          <Badge
                              radius="sm"
                              variant="filled"
                              size="xs"
                              style={{
                                  backgroundColor: getCardHeaderColor(card.label),
                                  color: theme.colors.dark[9],
                              }}
                          >
                              {card.label}
                          </Badge>
                  </Accordion.Control>
                  <Accordion.Panel style={{ textAlign: 'left' }}>
                      <Text 
                          className={classes.cardText}
                          lineClamp={6}
                      >
                          {card.text}
                          
                      </Text>
                      <Anchor href={card.url} target="_blank" mr={8} color="gray">
                          {/* <IconExternalLink size={15} /> */}
                          <Text 
                          size="xs"
                          style={{ display: 'inline-block' }}
                          color="#aaa"
                          mb={5}
                          
                          >
                          Read More
                          </Text>
                      </Anchor>
                  <div className="d-flex justify-content-between">
                  <div className="">
                      <ActionIcon color="yellow" variant="transparent" onClick={() => onRemove(card)} style={{ display: 'inline-block' }}>
                          <IconBackspaceFilled size={17} />
                      </ActionIcon>
                  </div>
                  <div className="">
                      <img src={getMagazineLogo(card.magazine)} alt={`${card.magazine} logo`} height="15" />
                  </div>
                  </div>
                  </Accordion.Panel>
                  </Accordion.Item>
                ))}
                </Accordion>
        );
      }
        return content;
    }

    return (
        <MantineCard withBorder radius="md" className={classes.bookmark} style={{ margin: 2}}>
        <Text className={classes.title}>Bookmarked Articles</Text>
        <p>Please bookmark any cards of your interest!</p>
        
        {renderAccordian(cardsInList)}
          
        
        </MantineCard>
    );
}

export default Bookmarks;
