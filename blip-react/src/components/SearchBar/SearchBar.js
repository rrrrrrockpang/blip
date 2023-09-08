import React from 'react';

import { IconSearch } from '@tabler/icons-react';
import { Input } from '@mantine/core';

const SearchBar = ({ searchQuery, setSearchQuery, handleSearch }) => {
    return (
        <form onSubmit={handleSearch} className="d-flex">
            {/* <input 
                type="text" 
                value={searchQuery} 
                onChange={(e) => setSearchQuery(e.target.value)} 
                placeholder="Search..."
                className="form-control"
                id="search-bar"
            /> */}
            <div style={{ textAlign: 'left' }}>
             <Input.Wrapper
                id="input-demo"
                label="&nbsp;"
                px={10}
                description="Search for anything else"
                >
                <Input
                    value={searchQuery}
                    icon={<IconSearch size={15} />}
                    onChange={(e) => setSearchQuery(e.target.value)} 
                    placeholder="Search"
                    id="search-bar"
                />
            </Input.Wrapper>
            </div>
        </form>
    );
};

export default SearchBar;
