# Dan Castro - Easter Egg
# Juego de la serpiente.
import sys
import random
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20

# Colores
COLOR_BACKGROUND = QColor(0, 0, 0)
COLOR_SNAKE = QColor(0, 255, 0)
COLOR_FOOD = QColor(255, 0, 0)

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Snake Game")
        self.setGeometry(100, 100, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.start_game()
        self.show()
    
    def start_game(self):
        self.snake = [(5, 5)]
        self.direction = Qt.Key.Key_Right
        self.food = self.generate_food()
        self.timer.start(100)
        self.update()
    
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def keyPressEvent(self, event):
        # Evitar que la serpiente se mueva en dirección opuesta
        if event.key() == Qt.Key.Key_Up and self.direction != Qt.Key.Key_Down:
            self.direction = Qt.Key.Key_Up
        elif event.key() == Qt.Key.Key_Down and self.direction != Qt.Key.Key_Up:
            self.direction = Qt.Key.Key_Down
        elif event.key() == Qt.Key.Key_Left and self.direction != Qt.Key.Key_Right:
            self.direction = Qt.Key.Key_Left
        elif event.key() == Qt.Key.Key_Right and self.direction != Qt.Key.Key_Left:
            self.direction = Qt.Key.Key_Right
    
    def game_loop(self):
        head_x, head_y = self.snake[0]
        
        if self.direction == Qt.Key.Key_Up:
            head_y -= 1
        elif self.direction == Qt.Key.Key_Down:
            head_y += 1
        elif self.direction == Qt.Key.Key_Left:
            head_x -= 1
        elif self.direction == Qt.Key.Key_Right:
            head_x += 1
        
        new_head = (head_x, head_y)
        
        # Verificar colisiones
        if (new_head in self.snake or
            head_x < 0 or head_x >= GRID_WIDTH or
            head_y < 0 or head_y >= GRID_HEIGHT):
            self.timer.stop()
            self.show_game_over()
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()
        
        self.update()
    
    def show_game_over(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText("¡Has perdido! ¿Quieres jugar de nuevo?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg_box.exec()
        
        if result == QMessageBox.StandardButton.Yes:
            self.start_game()
        else:
            self.close()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), COLOR_BACKGROUND)
        
        painter.setBrush(COLOR_SNAKE)
        for x, y in self.snake:
            painter.drawRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        painter.setBrush(COLOR_FOOD)
        painter.drawRect(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SnakeGame()
    sys.exit(app.exec())
