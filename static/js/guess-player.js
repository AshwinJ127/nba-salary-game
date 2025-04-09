// NBA Guess the Player - Game Logic

// Game state
let gameState = {
    allPlayers: [],        // All players from the API
    players: [],           // Filtered players based on year
    currentPlayer: null,   // The current player to guess
    streak: 0,             // Current streak
    highestStreak: 0,      // Highest streak achieved
    guessed: false,        // Whether the current player has been guessed
    searchResults: [],     // Search results
    yearFilter: 0,         // Year filter (0 means all years)
    availableYears: []     // Available years in the dataset
};

// DOM elements
const gameContent = document.getElementById('game-content');
const streakValue = document.getElementById('streak-value');
const highestStreakValue = document.getElementById('highest-streak-value');
const yearFilter = document.getElementById('year-filter');

// Initialize the game
async function initGame() {
    try {
        // Load player data from the API
        const response = await fetch('/player-stats');
        if (!response.ok) {
            throw new Error('Failed to fetch player data');
        }
        
        // Store all players and set initial filtered players
        gameState.allPlayers = await response.json();
        gameState.players = [...gameState.allPlayers];
        
        // Extract available years from the data
        extractAvailableYears();
        
        // Populate the year filter dropdown
        populateYearFilter();
        
        // Add event listener for year filter changes
        yearFilter.addEventListener('change', handleYearFilterChange);
        
        // Load saved streak from localStorage
        const savedStreak = localStorage.getItem('guessPlayerStreak');
        const savedHighestStreak = localStorage.getItem('guessPlayerHighestStreak');
        const savedYearFilter = localStorage.getItem('guessPlayerYearFilter');
        
        if (savedStreak) gameState.streak = parseInt(savedStreak);
        if (savedHighestStreak) gameState.highestStreak = parseInt(savedHighestStreak);
        if (savedYearFilter) {
            gameState.yearFilter = parseInt(savedYearFilter);
            yearFilter.value = savedYearFilter;
            filterPlayersByYear();
        }
        
        // Update streak display
        updateStreakDisplay();
        
        // Start the game
        startNewRound();
    } catch (error) {
        console.error('Error initializing game:', error);
        gameContent.innerHTML = `
            <div class="error-message">
                <p>Failed to load player data. Please try again later.</p>
                <button class="button" onclick="location.reload()">Retry</button>
            </div>
        `;
    }
}

// Extract available years from the player data
function extractAvailableYears() {
    // Get all unique years from the data
    const years = new Set();
    
    gameState.allPlayers.forEach(player => {
        // Use the year field directly from the data
        if (player.year) {
            years.add(player.year);
            console.log(`Player ${player.player} has year ${player.year}`);
        } else {
            console.log(`Player ${player.player} has NO year data`);
        }
    });
    
    // Convert to array and sort
    gameState.availableYears = Array.from(years).sort();
    console.log('Available years:', gameState.availableYears);
}

// Populate the year filter dropdown
function populateYearFilter() {
    // Add "All Years" option
    const allYearsOption = document.createElement('option');
    allYearsOption.value = 0;
    allYearsOption.textContent = 'All Years';
    yearFilter.appendChild(allYearsOption);
    
    // Add options for each available year
    gameState.availableYears.forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    });
}

// Handle year filter changes
function handleYearFilterChange() {
    const selectedYear = parseInt(yearFilter.value);
    gameState.yearFilter = selectedYear;
    
    // Save to localStorage
    localStorage.setItem('guessPlayerYearFilter', selectedYear);
    
    // Filter players based on the selected year
    filterPlayersByYear();
    
    // Start a new round with the filtered players
    startNewRound();
}

// Filter players based on the selected year
function filterPlayersByYear() {
    if (gameState.yearFilter === 0) {
        // If "All Years" is selected, use all players
        gameState.players = [...gameState.allPlayers];
    } else {
        // Filter players with years greater than or equal to the selected year
        gameState.players = gameState.allPlayers.filter(player => {
            return player.year && player.year >= gameState.yearFilter;
        });
    }
    
    console.log(`Filtered to ${gameState.players.length} players from ${gameState.yearFilter || 'all years'}`);
}

// Start a new round
function startNewRound() {
    // Reset game state for the new round
    gameState.guessed = false;
    
    // Select a random player
    const randomIndex = Math.floor(Math.random() * gameState.players.length);
    gameState.currentPlayer = gameState.players[randomIndex];
    
    // Render the game UI
    renderGameUI();
    
    // Focus on the search input after a short delay to ensure the UI is fully rendered
    setTimeout(() => {
        const searchInput = document.getElementById('player-search');
        if (searchInput) {
            searchInput.focus();
        }
    }, 100);
}

// Render the game UI
function renderGameUI() {
    const player = gameState.currentPlayer;
    
    // Create the game container
    const gameContainer = document.createElement('div');
    gameContainer.className = 'game-container';
    
    // Add the player info section (Team, Position, Age, Season)
    const playerInfoSection = document.createElement('div');
    playerInfoSection.className = 'player-info-section';
    
    // Create player info display
    const playerInfoDisplay = document.createElement('div');
    playerInfoDisplay.className = 'player-info-display';
    
    // Add basic info stats
    const basicInfoStats = [
        { label: 'Team', value: player.team },
        { label: 'Position', value: player.position },
        { label: 'Age', value: player.age },
        { label: 'Season', value: player.season }
    ];
    
    basicInfoStats.forEach(stat => {
        const statItem = document.createElement('div');
        statItem.className = 'info-stat-item';
        
        const statLabel = document.createElement('div');
        statLabel.className = 'stat-label';
        statLabel.textContent = stat.label;
        
        const statValue = document.createElement('div');
        statValue.className = 'stat-value';
        statValue.textContent = stat.value;
        
        statItem.appendChild(statLabel);
        statItem.appendChild(statValue);
        playerInfoDisplay.appendChild(statItem);
    });
    
    playerInfoSection.appendChild(playerInfoDisplay);
    gameContainer.appendChild(playerInfoSection);
    
    // Add the games and minutes section
    const gamesMinutesSection = document.createElement('div');
    gamesMinutesSection.className = 'games-minutes-section';
    
    // Create games and minutes display
    const gamesMinutesDisplay = document.createElement('div');
    gamesMinutesDisplay.className = 'games-minutes-display';
    
    // Add games and minutes stats
    const gamesMinutesStats = [
        { label: 'Games', value: player.games },
        { label: 'MPG', value: player.mpg }
    ];
    
    gamesMinutesStats.forEach(stat => {
        const statItem = document.createElement('div');
        statItem.className = 'games-minutes-stat-item';
        
        const statLabel = document.createElement('div');
        statLabel.className = 'stat-label';
        statLabel.textContent = stat.label;
        
        const statValue = document.createElement('div');
        statValue.className = 'stat-value';
        statValue.textContent = stat.value;
        
        statItem.appendChild(statLabel);
        statItem.appendChild(statValue);
        gamesMinutesDisplay.appendChild(statItem);
    });
    
    gamesMinutesSection.appendChild(gamesMinutesDisplay);
    gameContainer.appendChild(gamesMinutesSection);
    
    // Add the main stats section
    const mainStatsSection = document.createElement('div');
    mainStatsSection.className = 'main-stats-section';
    
    // Create main stats display
    const mainStatsDisplay = document.createElement('div');
    mainStatsDisplay.className = 'main-stats-display';
    
    // Add main performance stats
    const mainStats = [
        { label: 'PPG', value: player.ppg },
        { label: 'RPG', value: player.rpg },
        { label: 'APG', value: player.apg },
        { label: 'SPG', value: player.spg },
        { label: 'BPG', value: player.bpg }
    ];
    
    mainStats.forEach(stat => {
        const statItem = document.createElement('div');
        statItem.className = 'main-stat-item';
        
        const statLabel = document.createElement('div');
        statLabel.className = 'stat-label';
        statLabel.textContent = stat.label;
        
        const statValue = document.createElement('div');
        statValue.className = 'stat-value main-stat-value';
        statValue.textContent = stat.value;
        
        statItem.appendChild(statLabel);
        statItem.appendChild(statValue);
        mainStatsDisplay.appendChild(statItem);
    });
    
    mainStatsSection.appendChild(mainStatsDisplay);
    gameContainer.appendChild(mainStatsSection);
    
    // Add the search container
    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-container';
    
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'search-input';
    searchInput.placeholder = 'Search for a player...';
    searchInput.id = 'player-search';
    searchInput.autocomplete = 'off';
    
    searchContainer.appendChild(searchInput);
    
    // Add search results container
    const searchResults = document.createElement('div');
    searchResults.className = 'search-results';
    searchResults.id = 'search-results';
    searchResults.style.display = 'none';
    searchContainer.appendChild(searchResults);
    
    gameContainer.appendChild(searchContainer);
    
    // Add the result container (initially hidden)
    const resultContainer = document.createElement('div');
    resultContainer.className = 'result';
    resultContainer.id = 'result';
    resultContainer.style.display = 'none';
    gameContainer.appendChild(resultContainer);
    
    // Add a container for the next button to center it
    const nextButtonContainer = document.createElement('div');
    nextButtonContainer.style.textAlign = 'center';
    nextButtonContainer.style.margin = '5px 0 10px';
    
    // Add the next button (initially hidden)
    const nextButton = document.createElement('button');
    nextButton.className = 'button';
    nextButton.textContent = 'Next Player';
    nextButton.id = 'next-button';
    nextButton.style.display = 'none';
    nextButton.addEventListener('click', startNewRound);
    
    nextButtonContainer.appendChild(nextButton);
    gameContainer.appendChild(nextButtonContainer);
    
    // Clear the game content and add the new game container
    gameContent.innerHTML = '';
    gameContent.appendChild(gameContainer);
    
    // Add event listeners
    document.getElementById('player-search').addEventListener('input', handleSearch);
    document.getElementById('player-search').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            // If there are search results and player hasn't guessed yet, select the first result
            if (gameState.searchResults.length > 0 && !gameState.guessed) {
                handleGuess(gameState.searchResults[0].player);
            } 
            // If player has already guessed and next button is visible, click it
            else if (gameState.guessed) {
                const nextButton = document.getElementById('next-button');
                if (nextButton && nextButton.style.display !== 'none') {
                    nextButton.click();
                }
            }
        }
    });
}

// Handle search input
function handleSearch(event) {
    const searchTerm = event.target.value.trim().toLowerCase();
    const searchResults = document.getElementById('search-results');
    
    if (searchTerm.length < 2) {
        searchResults.style.display = 'none';
        gameState.searchResults = [];
        return;
    }
    
    // Filter players based on search term
    const filteredPlayers = gameState.players.filter(player => 
        player.player.toLowerCase().includes(searchTerm)
    );
    
    // Group players by name (combine seasons)
    const playerMap = new Map();
    filteredPlayers.forEach(player => {
        if (!playerMap.has(player.player)) {
            playerMap.set(player.player, player);
        }
    });
    
    // Convert map back to array
    gameState.searchResults = Array.from(playerMap.values()).slice(0, 10); // Limit to 10 results
    
    // Display search results
    if (gameState.searchResults.length > 0) {
        searchResults.innerHTML = '';
        
        gameState.searchResults.forEach(player => {
            const resultItem = document.createElement('div');
            resultItem.className = 'search-result-item';
            resultItem.innerHTML = `
                <span class="search-result-name">${player.player}</span>
            `;
            resultItem.addEventListener('click', () => handleGuess(player.player));
            searchResults.appendChild(resultItem);
        });
        
        searchResults.style.display = 'block';
    } else {
        searchResults.style.display = 'none';
    }
}

// Handle player guess
function handleGuess(guessedPlayerName) {
    // If already guessed, ignore
    if (gameState.guessed) return;
    
    const searchInput = document.getElementById('player-search');
    const searchResults = document.getElementById('search-results');
    const resultContainer = document.getElementById('result');
    const nextButton = document.getElementById('next-button');
    const nextButtonContainer = nextButton.parentElement;
    
    // Hide search results
    searchResults.style.display = 'none';
    
    // Check if the guess is correct (compare player names)
    const isCorrect = guessedPlayerName === gameState.currentPlayer.player;
    
    // Update game state
    gameState.guessed = true;
    
    if (isCorrect) {
        // Correct guess
        gameState.streak++;
        if (gameState.streak > gameState.highestStreak) {
            gameState.highestStreak = gameState.streak;
        }
        
        resultContainer.textContent = `Correct! It's ${gameState.currentPlayer.player}.`;
        resultContainer.className = 'result correct';
    } else {
        // Incorrect guess
        gameState.streak = 0;
        
        resultContainer.textContent = `Incorrect! It's ${gameState.currentPlayer.player}.`;
        resultContainer.className = 'result incorrect';
    }
    
    // Update localStorage
    localStorage.setItem('guessPlayerStreak', gameState.streak);
    localStorage.setItem('guessPlayerHighestStreak', gameState.highestStreak);
    
    // Update streak display
    updateStreakDisplay();
    
    // Show result and next button
    resultContainer.style.display = 'block';
    nextButton.style.display = 'inline-block';
    nextButtonContainer.style.display = 'block';
    
    // Clear search input
    searchInput.value = '';
}

// Update streak display
function updateStreakDisplay() {
    streakValue.textContent = gameState.streak;
    highestStreakValue.textContent = gameState.highestStreak;
}

// Handle Enter key press globally
function handleGlobalKeyPress(e) {
    // Skip if the event target is the search input (it has its own handler)
    if (e.target.id === 'player-search') {
        return;
    }
    
    if (e.key === 'Enter' && gameState.guessed) {
        const nextButton = document.getElementById('next-button');
        if (nextButton && nextButton.style.display !== 'none') {
            nextButton.click();
        }
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initGame();
    // Add global key press event listener
    document.addEventListener('keydown', handleGlobalKeyPress);
});