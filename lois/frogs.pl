% Лабораторная работа №2 по дисциплине ЛОИС
% Выполнена студентом группы 121701 БГУИР Рыбакова Ирина Евгеньевна
% Файл содержит описание предикатов, позволяющих решить задачу с лягушками
% Расположение лягушек представлено в виде списка, где b - коричневая лягушка, g - зелёная лягушка, e - свободный камень

% Описание прыжка зеленой лягушки через занятый камень на свободный камень 
move([g,F,e|Tail],[e,F,g|Tail]).
% Описание прыжка коричневой лягушки через занятый камень на свободный камень
move([e,F,b|Tail],[b,F,e|Tail]).
% Описание прыжка зеленой лягушки на соседний свободный камень
move([g,e|Tail],[e,g|Tail]).
% Описание прыжка коричневой лягушки на соседний свободный камень
move([e,b|Tail],[b,e|Tail]).
% Лягушки могут прыгать не только в начале списка
move([H1|T1],[H1|T2]) :- move(T1,T2).

% Проверка существрвания решения от заданного начального расположения лягушек до заданного конечного
nextstep([b,b,b,e,g,g,g],[b,b,b,e,g,g,g], fact).
% Из расположения X можно перейти в расположение Y, если можно перейти из X в Y за один шаг (один прыжок одной лягушки)
nextstep(X,Y,fact):-move(X,Y).
% Из расположения X можно перейти в расположение Y, если найдется такое промежуточное расположение Z, являющееся следующим шагом от X,
% из которого можно перейти в Y
nextstep(X,Y,rule):-
    nextstep(X,Z,fact),
	nextstep(Z,Y,_).

% Решение всей задачи поменять лягушек местами
% Если текущее расположение является конечным, выводим его на экран, процесс поиска решения заканчивается
switch([b,b,b,e,g,g,g]):-write('[b,b,b,e,g,g,g]').
% Находим такой ход в расположение Y, что из Y можно перейти в нужное конечное состояние '[b,b,b,e,g,g,g]'
% Далее решаем задачу из расположения Y
switch(X) :- 
	write(X), nl,
	move(X,Y),
	nextstep(Y,[b,b,b,e,g,g,g],_),
	switch(Y).
% Решить задачу из начального положения '[g,g,g,e,b,b,b]'
switch :- switch([g,g,g,e,b,b,b]).