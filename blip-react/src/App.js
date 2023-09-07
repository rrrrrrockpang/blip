import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import Cookies from 'js-cookie';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import DATASET from './dataset/dataset.csv';
import CardList from './components/CardList/CardList';
import FilterDropdown from './components/FilterDropdown/FilterDropdown';
import LogoHeader from './components/LogoHeader/LogoHeader';
import Accordion from './components/Accordion/Accordion';
import SafetyModal from './components/SafetyModal/SafetyModal';  // Adjust the path if you place it in another directory
import SearchBar from './components/SearchBar/SearchBar';
import ArticleModal from './components/ArticleModal/ArticleModal';
import ContributeModal from './components/ContributeModal/ContributeModal';
import InfiniteScroll from 'react-infinite-scroll-component';
import Joyride from 'react-joyride';



function App() {
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
            target: ".accordion-section",
            content: "See your bookmarked cards in this section. The goal is that you can reference this in the future to help you make decisions about your own project.",
            title: "Bookmarked Cards"
        }
    ]);

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
        if (!Cookies.get('shown')) {
        setShowModal(true);
        }
    }, []);

    useEffect(() => {
        setSearchQuery("");
    }, [domainFilter, aspectFilter]);

    // Filter and Initialize Cards
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
            // Cookies.set('shown', 'yes', { expires: 1 }); // 1 day
        };

    const addToAccordionList = (card, targetElement) => {
        console.log('addToAccordionList called', card, targetElement);

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
                // 'http://localhost:8000/search', 
                "http://104.197.248.47:80/search",
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
                    <div className='col-9'>
                        {/* Search and Filters */}
                        <div className="row mb-3 align-items-center">
                            <div className="col-md-3">
                                <FilterDropdown label="Domain" options={
                                    ['Social Media', 'Voice Assistant', 'Augmented/Virtual Reality', "Computer Vision", "Robotics", "Mobile Technology", "AI Decision-Making", "Neuroscience", "Computational Biology", "Ubiquitous Computing"]
                                } onChange={setDomainFilter} />
                            </div>
                            <div className="col-md-3">
                                <FilterDropdown label="Aspect" options={
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
                            <div className="col-md-2 text-center shuffle-button">
                                <button className="btn btn-outline-secondary" onClick={handleShuffle}>
                                    <i className="fas fa-random"></i> Shuffle
                                </button>
                            </div>
                        </div>

                        {/* Cards */}
                        {/* <CardList cards={filteredCards} onAdd={addToAccordionList} onRemove={removeFromMainList} /> */}
                        <InfiniteScroll
                            dataLength={currentCards.length}
                            next={fetchMoreData}
                            hasMore={hasMore}
                            // loader={<h4>Loading...</h4>}
                            scrollableTarget="scrollableDiv"
                            // endMessage={
                            //     <p style={{ textAlign: 'center' }}>
                            //         <b>Yay! You have seen it all</b>
                            //     </p>
                            // }
                        >
                        <CardList cards={currentCards} onAdd={addToAccordionList} onRemove={removeFromMainList} />
                
                        </InfiniteScroll>
                        {filteredCards.length === 0 && <p>No cards found.</p>}
                    </div>

                    <div className='col-3'>
                        <Accordion cardsInList={cardsInList} onRemove={removeFromAccordionList} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
