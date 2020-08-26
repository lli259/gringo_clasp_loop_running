number(1..n). 
part(1..8).
{partition(X,Y) : part(Y)}=1 :- number(X).
:- partition(X,P), partition(Y,P), partition(X+Y,P), X<=Y, number(X),number(Y),part(P),X+Y<=n.
