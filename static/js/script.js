// script.js

// Global game variables
let playerData = [];
let currentPlayers = { player1: null, player2: null };
let streak = 0;
let highestStreak = 0;

let gameContent; 
let streakValueElement;
let highestStreakValueElement;

// Initialize DOM references and load data when the page is ready
document.addEventListener('DOMContentLoaded', function() {
    gameContent = document.getElementById('game-content');
    streakValueElement = document.getElementById('streak-value');
    highestStreakValueElement = document.getElementById('highest-streak-value');
    
    // Load highest streak from localStorage if available
    const savedHighestStreak = localStorage.getItem('nba-salary-game-highest-streak');
    if (savedHighestStreak) {
        highestStreak = parseInt(savedHighestStreak);
        if (highestStreakValueElement) {
            highestStreakValueElement.textContent = highestStreak;
        }
    }

    // Begin fetching player data from the server
    fetchPlayerData();
});

// Format a salary number to currency string (e.g., $44,474,988)
function formatSalary(salary) {
    return '$' + Number(salary).toLocaleString();
}

// Display an error message within the game container
function showError(message) {
    if (!gameContent) return;
    gameContent.innerHTML = `
        <div class="game-container">
            <div class="question" style="color: #dc3545;">Error Loading Game</div>
            <p>There was a problem loading the player data. Please try refreshing the page.</p>
            <p>Error details: ${message}</p>
            <button class="button" id="retry-button">Retry</button>
        </div>
    `;
    const retryButton = document.getElementById('retry-button');
    if (retryButton) {
        retryButton.addEventListener('click', fetchPlayerData);
    }
}

// Fetch the player data from the backend API (/data)
async function fetchPlayerData() {
    if (!gameContent) {
        console.error("Game content element not found");
        return;
    }
    
    // Show a loading spinner while data loads
    gameContent.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
        </div>
    `;
    
    try {
        const response = await fetch('/data');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        
        // Filter out any records that are missing required fields
        playerData = data.filter(player =>
            player && typeof player === 'object' && player.player && player.salary
        );
        
        console.log(`Loaded ${playerData.length} player records from API`);
        
        if (playerData.length < 2) {
            throw new Error("Not enough valid player data to start the game");
        }
        
        startGame();
    } catch (error) {
        console.error("Error fetching player data:", error);
        showError(error.message);
    }
}

// Start the game: select players and render the UI
function startGame() {
    selectPlayers();
    renderGame();
}

// Randomly select a player with a rank of 150 or less.
// If none are available, fallback to any random player.
function getRandomPlayerWithRankUnder150() {
    const eligiblePlayers = playerData.filter(player => player.rank <= 150);
    if (eligiblePlayers.length === 0) {
        return playerData[Math.floor(Math.random() * playerData.length)];
    }
    return eligiblePlayers[Math.floor(Math.random() * eligiblePlayers.length)];
}

// Select a second player with a salary within ±25% range of the first player.
// It excludes the first player from the selection.
function getPlayerWithSimilarSalary(player1) {
    const targetSalary = Number(player1.salary);
    const lowerBound = targetSalary * 0.75;
    const upperBound = targetSalary * 1.25;
    
    console.log("Finding player with similar salary:");
    console.log("Target salary:", targetSalary, "Range:", lowerBound, "to", upperBound);
    
    let eligiblePlayers = playerData.filter(player =>
        player.id !== player1.id &&
        player.rank <= 150 &&
        Number(player.salary) >= lowerBound &&
        Number(player.salary) <= upperBound
    );
    
    console.log(`Found ${eligiblePlayers.length} eligible players`);
    
    if (eligiblePlayers.length === 0) {
        // If none qualify with the rank constraint, try any players that fall in the salary range.
        eligiblePlayers = playerData.filter(player =>
            player.id !== player1.id &&
            Number(player.salary) >= lowerBound &&
            Number(player.salary) <= upperBound
        );
    }
    
    if (eligiblePlayers.length === 0) {
        // As a last resort, return a random player (other than player1).
        const anyPlayers = playerData.filter(player => player.id !== player1.id);
        return anyPlayers[Math.floor(Math.random() * anyPlayers.length)];
    }
    
    return eligiblePlayers[Math.floor(Math.random() * eligiblePlayers.length)];
}

// Select two players for the current game round
function selectPlayers() {
    const player1 = getRandomPlayerWithRankUnder150();
    const player2 = getPlayerWithSimilarSalary(player1);
    
    console.log("Selected players:");
    console.log("Player 1:", player1.player, "Season:", player1.season, "Salary:", formatSalary(player1.salary));
    console.log("Player 2:", player2.player, "Season:", player2.season, "Salary:", formatSalary(player2.salary));
    
    currentPlayers = { player1, player2 };
}

// Render the game interface where players are displayed for selection
function renderGame() {
    if (!gameContent) {
        console.error("Game content element not found");
        return;
    }
    
    gameContent.innerHTML = `
        <div class="game-container">
            <div class="question">Who has the higher salary?</div>
            <div class="player-cards">
                <div class="player-card" id="player1-card">
                    <div class="player-name">${currentPlayers.player1.player}</div>
                    <div class="player-season">${currentPlayers.player1.season || 'Unknown Season'}</div>
                    <div class="player-salary" id="player1-salary">${formatSalary(currentPlayers.player1.salary)}</div>
                </div>
                <div class="player-card" id="player2-card">
                    <div class="player-name">${currentPlayers.player2.player}</div>
                    <div class="player-season">${currentPlayers.player2.season || 'Unknown Season'}</div>
                    <div class="player-salary" id="player2-salary">${formatSalary(currentPlayers.player2.salary)}</div>
                </div>
            </div>
        </div>
    `;
    
    // Attach event listeners to the player cards
    document.getElementById('player1-card').addEventListener('click', () => makeGuess(1));
    document.getElementById('player2-card').addEventListener('click', () => makeGuess(2));
}

// When a player is clicked, evaluate if the guess is correct
function makeGuess(playerNumber) {
    const player1Salary = Number(currentPlayers.player1.salary);
    const player2Salary = Number(currentPlayers.player2.salary);
    
    console.log("Comparing salaries: Player 1:", player1Salary, "Player 2:", player2Salary);
    
    const correctAnswer = player1Salary > player2Salary ? 1 : 2;
    const isCorrect = playerNumber === correctAnswer;
    
    if (isCorrect) {
        streak++;
        console.log("Correct! New streak:", streak);
        
        // Update highest streak if current streak is higher
        if (streak > highestStreak) {
            highestStreak = streak;
            console.log("New highest streak:", highestStreak);
            
            // Save to localStorage
            localStorage.setItem('nba-salary-game-highest-streak', highestStreak);
            
            // Update the highest streak display
            if (highestStreakValueElement) {
                highestStreakValueElement.textContent = highestStreak;
            }
        }
    } else {
        streak = 0;
        console.log("Wrong! Streak reset to 0");
    }
    
    // Update the current streak display with animation
    if (streakValueElement) {
        streakValueElement.textContent = streak;
        
        // Add animation class
        streakValueElement.classList.add('updated');
        
        // Remove the class after animation completes
        setTimeout(() => {
            streakValueElement.classList.remove('updated');
        }, 500);
    }
    
    // Update highest streak with animation if needed
    if (highestStreakValueElement && streak > highestStreak) {
        highestStreakValueElement.classList.add('updated');
        
        setTimeout(() => {
            highestStreakValueElement.classList.remove('updated');
        }, 500);
    }
    
    renderResult(isCorrect);
}

// Render the result view after a guess with an option to play again
function renderResult(isCorrect) {
    if (!gameContent) {
        console.error("Game content element not found");
        return;
    }
    
    gameContent.innerHTML = `
        <div class="game-container">
            <div class="result ${isCorrect ? 'correct' : 'incorrect'}">
                ${isCorrect ? 'Correct!' : 'Wrong!'}
            </div>
            <div class="player-cards">
                <div class="player-card">
                    <div class="player-name">${currentPlayers.player1.player}</div>
                    <div class="player-season">${currentPlayers.player1.season || 'Unknown Season'}</div>
                    <div class="player-salary" style="visibility: visible">${formatSalary(currentPlayers.player1.salary)}</div>
                </div>
                <div class="player-card">
                    <div class="player-name">${currentPlayers.player2.player}</div>
                    <div class="player-season">${currentPlayers.player2.season || 'Unknown Season'}</div>
                    <div class="player-salary" style="visibility: visible">${formatSalary(currentPlayers.player2.salary)}</div>
                </div>
            </div>
            <button class="button" id="next-button">
                ${isCorrect ? 'Next Players' : 'Play Again'}
            </button>
        </div>
    `;
    
    const nextButton = document.getElementById('next-button');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            selectPlayers();
            renderGame();
        });
    }
}
