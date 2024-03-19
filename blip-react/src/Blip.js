import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import DATASET from './dataset/dataset.csv';
import CardList from './components/CardList/CardList';
import FilterDropdown from './components/FilterDropdown/FilterDropdown';
import LogoHeader from './components/LogoHeader/LogoHeader';
import Bookmarks from './components/Accordion/Accordion';
import SafetyModal from './components/SafetyModal/SafetyModal';  // Adjust the path if you place it in another directory
import SearchBar from './components/SearchBar/SearchBar';
import SideBar from './components/SideBar/SideBar';
import ArticleModal from './components/ArticleModal/ArticleModal';
import ContributeModal from './components/ContributeModal/ContributeModal';
import Toggle from './components/Toggle/Toggle';
import InfiniteScroll from 'react-infinite-scroll-component';
import Joyride from 'react-joyride';
import WebFont from 'webfontloader';

// import { useNavigate } from 'react-router-dom';


import  {
    Text,
    Button,
} from '@mantine/core';
import {
    IconMicroscope,
    IconHealthRecognition,
    IconArrowsShuffle,
} from '@tabler/icons-react';



function Blip() {

    const [cards, setCards] = useState([]); 
    const [filteredCards, setFilteredCards] = useState(cards);
    const [domainFilter, setDomainFilter] = useState("");
    const [aspectFilter, setAspectFilter] = useState("");
    const [cardsInList, setCardsInList] = useState([]);
    const [searchQuery, setSearchQuery] = useState(""); 
    const [showModal, setShowModal] = useState(false);
    const [isArticleModalOpen, setArticleModalOpen] = useState(false);
    const [isContributeModalOpen, setContributeModalOpen] = useState(false);

    // infinite scrolling; State to manage the "page" or "portion" of cards to display
    const [hasMore, setHasMore] = useState(true);
    const [currentCards, setCurrentCards] = useState([]);  
    const [next, setNext] = useState(100);  

    const [isJoyrideReady, setIsJoyrideReady] = useState(false);
    // joystick steps
    const [joyrideSteps, setJoyrideSteps] = useState([
        {
            target: '#filter-Domain',
            content: 'Here you can select the domain you are interested in.',
            title: 'Domain Selection'
        },
        {
            target: '#filter-Aspect',
            content: 'Choose the aspect you want to focus on.',
            title: 'Aspect Selection'
        },
        {
            target: '#search-bar',
            content: 'Use the search bar to find specific cards. We use LLM to find the most relevant cards for your search query within the domain and aspect you selected.',
            title: 'Search'
        },
        {
            target: '.shuffle-button',
            content: 'Click here to shuffle the cards for new inspiration.',
            title: 'Shuffle'
        },
        {
            target: ".bookmark-btn",
            content: "Click here to add a card to your list to review further.",
            title: "Bookmark"
        },
        {
            target: ".bookmark-cancel-btn",
            content: "Click here to remove a card from your list if you don't like it!",
            title: "Remove Bookmark"
        },
        {
            target: ".toggle-group .btn-success",
            content: "See your bookmarked cards in this section. The goal is that you can reference this in the future to help you make decisions about your own project.",
            title: "Click to see your bookmarked cards!"
        },
        {
            target: ".contribute-card-btn",
            content: "Click here to contribute to the card by adding your own thoughts, ideas, or experiences. Edit in the sidebar!",
            title: "Contribute"
        },
        {
            target: ".toggle-group .btn-secondary",
            content: "Share your story here. We want to hear about your experiences. Remember you need to select a card first!",
            title: "Click to Share Your Story!"
        }
    ]);

    useEffect(() => {
        const checkTargets = () => {
          const targets = ['#filter-Domain', '#filter-Aspect', '#search-bar'];
          return targets.every(selector => document.querySelector(selector));
        };
      
        const intervalId = setInterval(() => {
          if (checkTargets()) {
            setIsJoyrideReady(true);
            clearInterval(intervalId);
          }
        }, 1000); // Check every 1 second
      
        return () => clearInterval(intervalId);
      }, []);

      
    const [isOpen, setIsOpen] = useState(false);
    const [selectedCard, setSelectedCard] = useState(null);
    const [activeView, setActiveView] = useState('bookmarks'); 
    const openSidebar = () => setIsOpen(true);
    const closeSidebar = () => setIsOpen(false);
    
    const openSidebarWithContent = (card) => {
        setSelectedCard(card);
        setIsOpen(true);
        setActiveView('sidebar'); // Set active view to sidebar when opening it
      };
      

    const fetchMoreData = () => {
        console.log("fetchMoreData called");
        if (currentCards.length >= filteredCards.length) {
          setHasMore(false);
          return;
        }
        setTimeout(() => {
          setNext(prevNext => prevNext + 100);
          setCurrentCards(filteredCards.slice(0, next + 100));
        }, 1000);
      };

      useEffect(() => {
        const handleScroll = () => {
          // Your scroll event handling logic
          console.log("Scrolled");
        };
        
        window.addEventListener('scroll', handleScroll);
        
        return () => {
          window.removeEventListener('scroll', handleScroll);
        };
      }, []);
      

    useEffect(() => {
        WebFont.load({
            google: {
              families: ['DM Serif Display', 'DM Sans']
            }
          });
        if (!Cookies.get('shown')) {
        setShowModal(true);
        }
    }, []);

    useEffect(() => {
        setSearchQuery("");
    }, [domainFilter, aspectFilter]);

    
    useEffect(() => {
        const uniqueFilteredCards = cards.reduce((acc, card) => {
            if (!acc.some(accCard => accCard.title === card.title)) {
                acc.push(card);
            }
            return acc;
        }, []);
        
        const filtered = uniqueFilteredCards.filter(card =>
        (domainFilter ? card.sector === domainFilter : true) &&
        (aspectFilter ? card.label === aspectFilter : true)
        );
        setFilteredCards(filtered);
        // setCurrentCards(filtered.slice(0, next));
    }, [cards, domainFilter, aspectFilter]);

    useEffect(() => {
        setCurrentCards(filteredCards.slice(0, next));
    }, [filteredCards, next]);
    

    useEffect(() => {
        Papa.parse(DATASET, {
        header: true,
        download: true,
        skipEmptyLines: true,
        complete: (data) => {
            setCards(shuffleArray(data.data));
        }
        });
    }, []);

    /** Logic to add and remove cards */ 
    const handleCloseModal = () => {
            setShowModal(false);
        };

    const addToAccordionList = (card, targetElement) => {
        console.log('addToAccordionList called', card, targetElement);
        setActiveView('bookmarks');

        const cardElement = targetElement.closest('.card'); // Assuming each card has a class of 'card'
        cardElement.classList.add('moving-to-accordion');
        
        setTimeout(() => {
            cardElement.classList.remove("moving-to-accordion");
            setCardsInList([...cardsInList, card]);
            setFilteredCards(filteredCards.filter(c => c.title !== card.title));  // using title as a unique identifier
        }, 200);
    }

    const removeFromAccordionList = (card) => {
        setCardsInList(cardsInList.filter(c => c.title !== card.title));  // using title as a unique identifier
        // setFilteredCards([card, ...filteredCards]); // add back to main view
        // Check if the card matches the current domain and aspect filters before adding it back to the main view.
        if ((domainFilter ? card.sector === domainFilter : true) &&
            (aspectFilter ? card.label === aspectFilter : true)) {
            setFilteredCards([card, ...filteredCards]); // add back to main view
        }
    }

    const contribute = (card) => {
        setSelectedCard(card);
        setActiveView('sidebar');
        setIsOpen(true); 
    }

    const removeFromMainList = (card) => {
        setFilteredCards(filteredCards.filter(c => c.title !== card.title));  // using title as a unique identifier
    }

    /**
     * Shuffles array in place. ES6 version
     * @param {Array} a items An array containing the items.
     * https://stackoverflow.com/questions/6274339/how-can-i-shuffle-an-array
    **/
    const shuffleArray = (array)  => {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];  // Destructuring assignment to swap values
        }
        return array;
    }

    const handleShuffle = () => {
        const shuffledCards = shuffleArray([...filteredCards]);
        setFilteredCards(shuffledCards);
    }

    const handleSearch = async (e) => {
        e.preventDefault();

        console.log("About to fetch data from FastAPI...");
        try {
            const response = await fetch(
                'https://blip.labinthewild.org/api/search',
                {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    query: searchQuery,
                    domain: domainFilter,
                    aspect: aspectFilter
                })
            });

            if(response.ok) {
                console.log("Received successful response");
                const data = await response.json();
                // Check for the "error" keyword in the JSON data
                if (data.hasOwnProperty("error")) {
                    console.error("Received error in response data:", data.error);
                    return;
                }

                const { titles } = data;

                if (!Array.isArray(titles)) {
                    console.error("Received 'titles' is not an array:", titles);
                    return;
                }

                let matchedCards = titles.map(title => {
                    return cards.find(card => card.title === title);
                }).filter(card => card !== undefined);  // Remove undefined entries
    
                let unmatchedCards = cards.filter(card => !titles.includes(card.title));
                
                // Apply additional filtering based on domainFilter and aspectFilter
                const applyAdditionalFiltering = (cardList) => {
                    if (domainFilter) {
                        cardList = cardList.filter(card => card.sector === domainFilter);
                    }
                    if (aspectFilter) {
                        cardList = cardList.filter(card => card.label === aspectFilter);
                    }
                    return cardList;
                };
    
                matchedCards = applyAdditionalFiltering(matchedCards);
                unmatchedCards = applyAdditionalFiltering(unmatchedCards);
    
                const combinedCards = [...matchedCards, ...unmatchedCards];

                // Update the filteredCards state.
                setFilteredCards(combinedCards);
            } else {
                console.error(`Received unsuccessful response: ${response.status} ${response.statusText}`);
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }

        console.log("Exiting handleSearch.");
    };

    /** Logic to open and close modals */
    const openArticleModal = () => setArticleModalOpen(true);
    const closeArticleModal = () => setArticleModalOpen(false);
    const openContributeModal = () => setContributeModalOpen(true);
    const closeContributeModal = () => setContributeModalOpen(false);

    return (
        <div className="App">
            {showModal && <SafetyModal onClose={handleCloseModal} />}

            {!showModal && (
                <Joyride
                    steps={joyrideSteps}
                    continuous={true}
                    disableScrolling={true}
                    scrollToFirstStep={false}
                    showProgress={true}
                    showSkipButton={true}
                />
            )}

            <LogoHeader openArticleModal={openArticleModal} openContributeModal={openContributeModal}/>
            <ArticleModal isOpen={isArticleModalOpen} closeModal={closeArticleModal} />
            <ContributeModal isOpen={isContributeModalOpen} closeModal={closeContributeModal} />

            <div className='container-fluid'>
                <div className='row'>
                    <div className='col-12 col-md-9'>
                        {/* Search and Filters */}
                        <div className="row mt-4 mb-3 align-items-end">
                            <div className="col-md-3">
                                <FilterDropdown label={"Domain"} description="Which kind of technology?" options={
                                    ['Social Media', 'Voice Assistant', 'Augmented/Virtual Reality', "Computer Vision", "Robotics", "Mobile Technology", "AI Decision-Making", "Neuroscience", "Computational Biology", "Ubiquitous Computing"]
                                } onChange={setDomainFilter} />
                            </div>
                            <div className="col-md-3">
                                <FilterDropdown label={"Aspect"} description="Which aspect of life is affected?" options={
                                    ['user experience', 'health & wellbeing', 'security & privacy', 'access to information & discourse', 'social norms & relationship', 'equality & justice', 'economy', 'politics', 'power dynamics', 'environment & sustainability']
                                } onChange={setAspectFilter} />
                            </div>
                            <div className="col-md-4">
                                <SearchBar 
                                searchQuery={searchQuery} 
                                setSearchQuery={setSearchQuery} 
                                handleSearch={handleSearch} 
                                />
                            </div>
                            <div className="col-md-2">
                                <Button
                                    color="green"
                                    variant="light"
                                    leftIcon={<IconArrowsShuffle size={15}/>}
                                    onClick={handleShuffle}
                                    className='shuffle-button'
                                >
                                    Shuffle
                                </Button>
                            </div>
                        </div>

                        <InfiniteScroll
                            dataLength={currentCards.length}
                            next={fetchMoreData}
                            hasMore={hasMore}
                            scrollableTarget="scrollableDiv"
                        >
                        <CardList 
                            cards={currentCards} 
                            onAdd={addToAccordionList} 
                            onRemove={removeFromMainList} 
                            onContribute={contribute}
                            />
                
                        </InfiniteScroll>
                        {filteredCards.length === 0 && <p>No cards found.</p>}
                    </div>

                    <div className='col-12 col-md-3'>
                        {/* <div className="view-toggle">
                            <button onClick={() => setActiveView('bookmarks')} disabled={activeView === 'bookmarks'}>Bookmarks</button>
                            <button onClick={() => setActiveView('sidebar')} disabled={activeView === 'sidebar'}>Sidebar</button>
                        </div> */}
                        <Toggle activeView={activeView} setActiveView={setActiveView} />

                        {activeView === 'bookmarks' && <Bookmarks cardsInList={cardsInList} onRemove={removeFromAccordionList} />}
                        {activeView === 'sidebar' && <SideBar isOpen={isOpen} onClose={closeSidebar} content={selectedCard} />}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Blip;
