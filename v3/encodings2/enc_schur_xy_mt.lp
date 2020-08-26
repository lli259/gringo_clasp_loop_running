number(1..n).
part(1..8).
{partition(X,Y) : part(Y)}=1 :- number(X).
:- partition(X,P), partition(Z-X,P), partition(Z,P), 2*X<=Z,
   number(X),number(Z),Z-X<=n,part(P).
