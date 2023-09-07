import React from 'react';

const SearchBar = ({ searchQuery, setSearchQuery, handleSearch }) => {
    return (
        <form onSubmit={handleSearch} className="d-flex">
            <input 
                type="text" 
                value={searchQuery} 
                onChange={(e) => setSearchQuery(e.target.value)} 
                placeholder="Search..."
                className="form-control"
                id="search-bar"
            />
        </form>
    );
};

export default SearchBar;
