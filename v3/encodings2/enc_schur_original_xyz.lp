number(1..n). 
part(1..8).
{partition(X,Y) : part(Y)}=1 :- number(X).
:- partition(X,P), partition(Y,P), partition(Z,P), X<=Y,Y<Z, Z=X+Y, number(X),number(Y),number(Z),part(P).
