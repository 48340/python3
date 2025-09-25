<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Noughts and Crosses</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .game-container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        h1 {
            margin-bottom: 1rem;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .game-info {
            margin-bottom: 2rem;
            font-size: 1.2em;
        }
        
        .board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-gap: 10px;
            max-width: 300px;
            margin: 0 auto 2rem;
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 15px;
        }
        
        .cell {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.9);
            border: none;
            border-radius: 10px;
            font-size: 2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .cell:hover:not(.taken) {
            background: rgba(255, 255, 255, 1);
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .cell.taken {
            cursor: not-allowed;
            background: rgba(255, 255, 255, 0.7);
        }
        
        .cell.x {
            color: #e74c3c;
        }
        
        .cell.o {
            color: #3498db;
        }
        
        .winning-cell {
            background: rgba(46, 204, 113, 0.8) !important;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .reset-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .reset-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        
        .score {
            display: flex;
            justify-content: space-around;
            margin: 1rem 0;
            font-size: 1.1em;
        }
        
        .score-item {
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 10px;
            min-width: 80px;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🎯 Noughts and Crosses</h1>
        
        <div class="game-info">
            <div id="status">Player X's Turn</div>
        </div>
        
        <div class="score">
            <div class="score-item">
                <div>Player X</div>
                <div id="scoreX">0</div>
            </div>
            <div class="score-item">
                <div>Draws</div>
                <div id="scoreDraw">0</div>
            </div>
            <div class="score-item">
                <div>Player O</div>
                <div id="scoreO">0</div>
            </div>
        </div>
        
        <div class="board" id="board">
            <button class="cell" data-index="0"></button>
            <button class="cell" data-index="1"></button>
            <button class="cell" data-index="2"></button>
            <button class="cell" data-index="3"></button>
            <button class="cell" data-index="4"></button>
            <button class="cell" data-index="5"></button>
            <button class="cell" data-index="6"></button>
            <button class="cell" data-index="7"></button>
            <button class="cell" data-index="8"></button>
        </div>
        
        <button class="reset-button" onclick="resetGame()">New Game</button>
    </div>

    <script>
        let currentPlayer = 'X';
        let gameBoard = ['', '', '', '', '', '', '', '', ''];
        let gameActive = true;
        let scores = { X: 0, O: 0, draw: 0 };
        
        const statusElement = document.getElementById('status');
        const cells = document.querySelectorAll('.cell');
        
        // Winning combinations
        const winningCombinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6] // Diagonals
        ];
        
        // Add click listeners to cells
        cells.forEach(cell => {
            cell.addEventListener('click', handleCellClick);
        });
        
        function handleCellClick(e) {
            const index = parseInt(e.target.dataset.index);
            
            if (gameBoard[index] !== '' || !gameActive) {
                return;
            }
            
            // Make move
            gameBoard[index] = currentPlayer;
            e.target.textContent = currentPlayer;
            e.target.classList.add('taken', currentPlayer.toLowerCase());
            
            // Check for win or draw
            if (checkWinner()) {
                gameActive = false;
                statusElement.textContent = `Player ${currentPlayer} Wins! 🎉`;
                scores[currentPlayer]++;
                updateScoreboard();
                highlightWinningCells();
            } else if (gameBoard.every(cell => cell !== '')) {
                gameActive = false;
                statusElement.textContent = "It's a Draw! 🤝";
                scores.draw++;
                updateScoreboard();
            } else {
                // Switch player
                currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
                statusElement.textContent = `Player ${currentPlayer}'s Turn`;
            }
        }
        
        function checkWinner() {
            return winningCombinations.some(combination => {
                const [a, b, c] = combination;
                return gameBoard[a] && 
                       gameBoard[a] === gameBoard[b] && 
                       gameBoard[a] === gameBoard[c];
            });
        }
        
        function highlightWinningCells() {
            const winningCombo = winningCombinations.find(combination => {
                const [a, b, c] = combination;
                return gameBoard[a] && 
                       gameBoard[a] === gameBoard[b] && 
                       gameBoard[a] === gameBoard[c];
            });
            
            if (winningCombo) {
                winningCombo.forEach(index => {
                    cells[index].classList.add('winning-cell');
                });
            }
        }
        
        function updateScoreboard() {
            document.getElementById('scoreX').textContent = scores.X;
            document.getElementById('scoreO').textContent = scores.O;
            document.getElementById('scoreDraw').textContent = scores.draw;
        }
        
        function resetGame() {
            gameBoard = ['', '', '', '', '', '', '', '', ''];
            gameActive = true;
            currentPlayer = 'X';
            statusElement.textContent = "Player X's Turn";
            
            cells.forEach(cell => {
                cell.textContent = '';
                cell.className = 'cell';
            });
        }
    </script>
</body>
</html>
