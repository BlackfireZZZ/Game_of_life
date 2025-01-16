# Игра в жизнь

## Техническое задание
Разработать приложение, реализующее "Игру в жизнь", которое будет показывать исходное состояние поля и его эволюцию.
В приложении должны присутствовать различные варианты задания стартового поля, а также другие фичи, улучшающие пользовательский опыт.
## Правила игры
- Место действия - ограниченная клетчатая плоскость, заданных пользователем размеров
- Каждая клетка на этой поверхности имеет восемь соседей, окружающих её, и может находиться в двух состояниях: быть «живой» (заполненной) или «мёртвой» (пустой).
- Распределение клеток в начале пользователь может импортировать из JSON файла, задать (нарисовать) вручную или сгенерировать случайно.
- Если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; в противном случае (если живых соседей меньше двух или больше трёх) клетка умирает.
![Пользовательские сценарии](Scheme.jpg)
## Технические основы
- Программа написана на Python tkinter.
- Для хранения игрового поля используется двумерный массив. Для сохранения игры используется формат JSON.
## Как запустить
1. ```bash
   https://github.com/BlackfireZZZ/Game_of_life
2. ```bash
   cd Game_of_life
   ```
3. Запустите скрипт:  
   ```bash
   python main.py
   ```
4. Задайте начальное поле и наслаждайтесь!


