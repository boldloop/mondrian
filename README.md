# Mondrian machine

This project grew from a desire to 1) learn a little more about the python graphics package DrawBot and 2) investigate *what* makes Mondrian paintings special. To that end, I wrote a program that generates paintings in the style of Mondrian. Looking at the paintings it makes, some are simply laughable, some are ugly, some are more Rothko than Mondrian, and some are surprisingly balanced and beautiful. It's helped me think about proportion and balance in composition, and hopefully it helps you too—you can see 100 sample paintings in the `gallery/` directory.

Oh, a word on how it works: the dimensions of the painting are chosen, and then a short line segment is placed somewhere on the canvas. Then, the segment grows a random amount, possibly sprouting one or two branches. The process repeats until either there are no more open termini, so every line terminates on the canvas's border or on another line.
