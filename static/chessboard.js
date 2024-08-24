$(document).ready(function() {

var board = Chessboard('board', {
    draggable: true,
    position: 'start',  // Sets the starting position with all pieces
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    dropOffBoard: 'trash',  // Option to allow dropping pieces off the board
    sparePieces: true       // Option to enable spare pieces
});

function onDragStart (source, piece, position, orientation) {
    // Do not allow the piece to be dragged if the game is over
    // or if it's not the player's turn, etc.
}

function onDrop (source, target) {
    // Handle the piece drop logic here
}

function onSnapEnd () {
    // Handle logic after a piece is placed on the board
    board.position(board.fen());  // Update the board with the new position
}

function onMouseoutSquare(square, piece) {
    // Handle mouse out events
}

function onMouseoverSquare(square, piece) {
    // Handle mouse over events
}

// Optionally, you can set the board to the starting position when the page loads
//board.position('start');
var customPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

// Initialize chessboard with custom position
board.position(customPosition);

});