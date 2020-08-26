number(1..n). 
part(1..8).
{partition(X,Y) : part(Y)}=1 :- number(X).
:- partition(X,P), partition(Y,P), partition(Z,P), trisum(X,Y,Z), X<=Y, Y<Z, part(P).
