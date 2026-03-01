# Hexagon 2048

Eso es el juego conocido 2048, pero con una cuadrícula hexagonal.

## Ejecutar el juego

Primero, necesitas instalar **pygame**. Puedes hacerlo con ```pip3 install pygame``` o ```pip3 install -r requirements.txt```.

A continuación, puedes ejecutar el juego: ```python3.12 main.py```.

## Controles del juego

Usa las siguientes teclas:

- U: Mover a la izquierda y arriba;
- J: Mover a la izquierda;
- N: Mover a la izquierda y abajo;
- B: Mover a la derecha y abajo;
- G: Mover a la derecha;
- Y: Mover a la derecha y arriba;
- Z: Deshacer el último movimiento (sólo 1);
- Q: Salir.

![Controles del juego](./screenshots/controls.png "Controles del juego")

## Puntuación

Obtienes 1 punto por cada movimiento y varios puntos por combinar celdas:

- 2 + 2 (4) - 2 puntos
- 4 + 4 (8) - 3 puntos
- 8 + 8 (16) - 4 puntos
- y así sucesivamente.

**¡Nota!** En cada movimiento, solo obtienes puntos por combinaciones únicas. Por ejemplo, si tienes 2 o 3 combinaciones de 2 + 2, solo obtienes 2 puntos. Sin embargo, si tienes varias combinaciones diferentes durante un movimiento, obtienes puntos por cada una. Por ejemplo, si combinas celdas de 2 + 2 y 4 + 4 durante un movimiento, obtienes 6 puntos: 1 por el movimiento y 2 y 3 por las combinaciones.

## Capturas de la pantalla

### Linux Mint 22.3

![Linux Mint 22.3](./screenshots/linux_mint_22_3.png "Linux Mint 22.3")

### Windows 11

![Windows 11](./screenshots/windows_11.png "Windows 11")
