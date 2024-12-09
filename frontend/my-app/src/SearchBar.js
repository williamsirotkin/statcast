import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';

function SearchBar({setPlayer}) {
  const [searchText, setSearchText] = useState('');

  const handleSearch = () => {
    console.log(setPlayer)
    setPlayer(searchText);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <Box className="p-6">
      <Box className="flex justify-center">
        <Box className="flex gap-4 w-full max-w-lg">
          <TextField
            variant="outlined"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search player"
            size="medium"
            className="w-[32rem]"
            InputProps={{
              className: "h-14"
            }}
          />
          <br></br>
          <br></br>
          <Button 
            variant="contained"
            onClick={handleSearch}
            className="px-8 h-14"
          >
            Search
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default SearchBar;