chess_board = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat and Chess</title>
    <link rel="stylesheet"
      href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css"
      integrity="sha384-q94+BZtLrkL1/ohfjR8c6L+A6qzNH9R2hBLwyoAfu3i/WCvQjzL2RQJ3uNHDISdU"
      crossorigin="anonymous">
      
</head>
<body>
    <div id="board"></div>

    <input type="text" id="customPosition" placeholder="Enter chess position">
    <button id="customB">Set position</button>

    <!--<button id="clearBoardBtn">Clear Board</button>-->
    <button id="startPositionBtn">Start Position</button>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"
    integrity="sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2"
    crossorigin="anonymous"></script>

    <!--<script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.js"></script> -->
    <script src="./static/js/chessboard-1.0.0.js"></script> 
    <!--<script src="static/chessboard.js"></script> -->

    <script>

        var board = Chessboard('board', {
            draggable: true,
            position: 'start',
            onSnapEnd: onSnapEnd,
            dropOffBoard: 'trash',  // Option to allow dropping pieces off the board
            sparePieces: true       // Option to enable spare pieces
        })

        $('#clearBoardBtn').on('click', board.clear)
        $('#startPositionBtn').on('click', setstartPosition)
        $('#customB').on('click', setCustomPosition)

        function setCustomPosition(){
            const customPosition = document.getElementById('customPosition').value;

            console.log(customPosition)
           board = Chessboard('board', {
                draggable: true,
                position: customPosition,
                onSnapEnd: onSnapEnd,
                dropOffBoard: 'trash',  // Option to allow dropping pieces off the board
                sparePieces: true       // Option to enable spare pieces
            })
        }

        function setstartPosition(){
            const customPosition = document.getElementById('customPosition').value;

            console.log(customPosition)
           board = Chessboard('board', {
                draggable: true,
                position: 'start',
                onSnapEnd: onSnapEnd,
                dropOffBoard: 'trash',  // Option to allow dropping pieces off the board
                sparePieces: true       // Option to enable spare pieces
            })
        }

        function onSnapEnd () {
           board.position(board.fen());
        }

    </script>
</body>
</html>
"""