winLow(X, M, _, 0) :- 
  X >= M, 
  !.

winLow(X, M, Tg, 1) :- 
  M1 is M - Tg, 
  X =< M1, 
  !.

winLow(X, M, Tg, Mu) :- 
  T1 is -1 * Tg, 
  X1 is M + X, 
  Mu is T1 * X1 + 1, 
  !.

winLowbool(X, M, Tg) :- 
  winLow(X, M, Tg, Mu), 
  Mu >= 0.5.

winMed(X, M, Tg, 0) :- 
  M1 is M - Tg, 
  X =< M1, 
  !.

winMed(X, M, Tg, 0) :- 
  M1 is M + Tg, 
  X >= M1, 
  !.

winMed(X, M, Tg, Mu) :- 
  M1 is M - Tg, 
  X >= M1, 
  X =< M, 
  X1 is X - M, 
  Mu is Tg * X1 - 1, 
  !.

winMed(X, M, Tg, Mu) :- 
  M1 is M + Tg,  
  X >= M, 
  X =< M1, 
  X1 is X - M, 
  Mu is -1 * Tg * X1 + 1, 
  !.

winMedbool(X, M, Tg) :- 
  winMed(X, M, Tg, Mu), 
  Mu > 0.5.

winHigh(X, M, _, 0) :- 
  X =< M, 
  !.

winHigh(X, M, Tg, 1) :- 
  M1 is M + Tg, 
  X >= M1, 
  !.

winHigh(X, M, Tg, Mu) :- 
  X1 is X + M, 
  Mu is Tg * X1 - 1, 
  !.

winHighbool(X, M, Tg) :- 
  winHigh(X, M, Tg, Mu), 
  Mu >= 0.5.

weekLow(X, M, _, R, 0) :- 
  M1 is M - R, 
  X >= M1, 
  !.

weekLow(X, M, Tg, R, 1) :- 
  M1 is M - R - Tg, 
  X =< M1, 
  !.

weekLow(X, M, Tg, R, Mu) :- 
  T1 is -1 * Tg, 
  X1 is M - R + X, 
  Mu is T1 * X1 + 1, 
  !.

weekLowbool(X, M, Tg, R) :- 
  weekLow(X, M, Tg, R, Mu), 
  Mu >= 0.5.

weekMed(X, M, Tg, R, 0) :- 
  M1 is M - R - Tg, 
  X =< M1, 
  !.

weekMed(X, M, Tg, R, 0) :- 
  M1 is M + R + Tg, 
  X >= M1, 
  !.

weekMed(X, M, Tg, R, 1) :- 
  M1 is M - R, 
  M2 is M + R, 
  X >= M1, 
  X =< M2, 
  Tg = Tg, 
  !.

weekMed(X, M, Tg, R, Mu) :- 
  M1 is M - R - Tg, 
  X >= M1, 
  X =< M, 
  X1 is X - M + R, 
  Mu is Tg * X1 - 1, 
  !.

weekMed(X, M, Tg, R, Mu) :- 
  M1 is M + R + Tg, 
  X >= M, 
  X =< M1, 
  X1 is X - M - R, 
  Mu is -1 * Tg * X1 + 1, 
  !.

weekMedbool(X, M, Tg, R) :- 
  weekMed(X, M, Tg, R, Mu), 
  Mu > 0.5.

weekHigh(X, M, _, R, 0) :- 
  M1 is M + R, 
  X =< M1, 
  !.

weekHigh(X, M, Tg, R, 1) :- 
  M1 is M + R + Tg, 
  X >= M1, 
  !.

weekHigh(X, M, Tg, R, Mu) :- 
  X1 is X + M + R, 
  Mu is Tg * X1 - 1, 
  !.

weekHighbool(X, M, Tg, R) :- 
  weekHigh(X, M, Tg, R, Mu),
  Mu >= 0.5.

togetherLow(X, M, _, 0) :- 
  X >= M, 
  !.
togetherLow(X, M, Tg, 1) :- 
  M1 is M - Tg, 
  X =< M1, 
  !.
togetherLow(X, M, Tg, Mu) :- 
  T1 is -1 * Tg,  
  X1 is M + X, 
  Mu is T1 * X1 + 1, 
  !.
togetherLowbool(X, M, Tg) :- 
  togetherLow(X, M, Tg, Mu), 
  Mu >= 0.5.

togetherMed(X, M, Tg, 0) :- 
  M1 is M - Tg, 
  X =< M1, 
  !.
togetherMed(X, M, Tg, 0) :- 
  M1 is M + Tg, 
  X >= M1, 
  !.
togetherMed(X, M, Tg, Mu) :- 
  M1 is M - Tg, 
  X >= M1, 
  X =< M, 
  X1 is X - M, 
  Mu is Tg * X1 - 1, 
  !.
togetherMed(X, M, Tg, Mu) :- 
  M1 is M + Tg, 
  X >= M, 
  X =< M1, 
  X1 is X - M, 
  Mu is -1 * Tg * X1 + 1, 
  !.
togetherMedbool(X, M, Tg) :- 
  togetherMed(X, M, Tg, Mu), 
  Mu > 0.5.

togetherHigh(X, M, _, 0) :- 
  X =< M, 
  !.
togetherHigh(X, M, Tg, 1) :- 
  M1 is M + Tg, 
  X >= M1, 
  !.
togetherHigh(X, M, Tg, Mu) :- 
  X1 is X + M, 
  Mu is Tg * X1 - 1, 
  !.
togetherHighbool(X, M, Tg) :- 
  togetherHigh(X, M, Tg, Mu), 
  Mu >= 0.5.

res(X, Mx, Tgx, Y, My, Tgy, Ry, Z, Mz, Tgz, _, _, Res) :- 
  (winHighbool(X, Mx, Tgx);
  winMedbool(X, Mx, Tgx)), 
  (weekLowbool(Y, My, Tgy, Ry);
  weekMedbool(Y, My, Tgy, Ry)), 
  togetherLowbool(Z, Mz, Tgz), 
  Res is 0,
  !.

res(_, Mx, Tgx, _, My, Tgy, Ry, Z, Mz, Tgz, X1, Y1, Res) :- 
  (winHighbool(X1, Mx, Tgx);
  winMedbool(X1, Mx, Tgx)), 
  (weekLowbool(Y1, My, Tgy, Ry);
  weekMedbool(Y1, My, Tgy, Ry)), 
  togetherHighbool(Z, Mz, Tgz), 
  Res is 2,
  !.

res(_,_,_,_,_,_,_,_,_,_,_,_, Res):- Res is 1, !.
