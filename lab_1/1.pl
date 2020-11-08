
%countofwins
badX(X, 0):-X>=5,!.
badX(X,Mu):-X<5, Mu is -0.2 * X + 1,!.
badXbool(X):-badX(X,Mu), Mu >= 0.5.

normalX(X,Mu):- X < 5, Mu is 0.2 * X,!.
normalX(X,Mu):- Mu is -0.2 * X + 2, !.
normalXbool(X):-normalX(X, Mu), Mu > 0.5.

goodX(X, 0):- X =< 5, !.
goodX(X, Mu):- Mu is 0.2 * X - 1, !.
goodXbool(X):-goodX(X, Mu), Mu >= 0.5.
 
%countofpatiens
badY(Y,1):-Y =< 2, !.
badY(Y,0):-Y >=4, !.
badY(Y, Mu):- Mu is -Y/2 + 2, !.
badYbool(Y):-badY(Y, Mu), Mu >= 0.5.

normalY(Y,1):-Y>=4, Y=<6,!.
normalY(Y,Mu):-Y<4,Y>2,Mu is 1/2 * Y - 1, !.
normalY(Y, Mu):- Y > 8, Y < 6, Mu is -1/2*Y + 4, !.
normalY(Y,0).
normalYbool(Y):-normalY(Y, Mu), Mu > 0.5.

goodY(Y, 0):-Y=<6,!.
goodY(Y,1):-Y>=8,!.
goodY(Y, Mu):- Mu is 1/2 * Y - 3, !.
goodYbool(Y):-goodY(Y, Mu), Mu >= 0.5.


%countwin1win2

badZ(Z, 0):-Z>=5,!.
badZ(Z, Mu):-Mu is -0.2 * Z + 1, !.
badZbool(Z):-badZ(Z, Mu), Mu >= 0.5.

normalZ(Z,Mu):-Z=<5, Mu is 0.2 *Z, !.
normalZ(Z, Mu):- Mu is -0.2 * Z + 1, !.
normalZbool(Z):- normalZ(Z, Mu), Mu > 0.5.

goodZ(Z, 0):-Z=< 5, !.
goodZ(Z, Mu):- Mu is 0.2 * Z - 1.
goodZbool(Z):- goodZ(Z, Mu), Mu >= 0.5.

%result

badR(X,0):- X>=5,!.
badR(X,1):- X=<3,!.
badR(X, Mu):- Mu is -0.5 * X + 2.5.
badRbool(X):-badR(X, Mu), Mu >= 0.5.

normalR(X, 0):- (X =<3; X>=7), !.
normalR(X, Mu):- X<5, X>3, Mu is 0.5 * X - 1.5, !.
normalR(X, Mu):- Mu is -0.5 * X + 3.5.
normalRbool(X):- normalR(X, Mu), Mu > 0.5.

goodR(X,0):- X =< 5, !.
goodR(X,1):- X >= 7, !.
goodR(X, Mu):- Mu is 0.5 * X -2.5.
goodRbool(X):- goodR(X, Mu), Mu >= 0.5.

%programm

programm(X1,X2,Y1,Y2,Z, Res):- agregation(X1,X2,Y1,Y2,Z, Num1,Num2,Num3), getRes(Res, 0, 0, 0, Num1, Num2, Num3), write_res(Res).

implication(X,Y,Z, R, Res):- badR(R, MuR1), normalR(R, MuR2), goodR(R, MuR3), min(X, MuR1, SubRes1), min(Y, MuR2, SubRes2), min(Z, MuR3, SubRes3), max(SubRes1, SubRes2, SubRes), 
                             max(SubRes3, SubRes, Res).


getRes(R, Ch, Zn, 10, _, _, _):- R is Ch / Zn, !.
getRes(R,Ch,Zn,I, X, Y, Z):-implication(X, Y, Z, I, Res), Ch1 is Ch + Res * I, Zn1 is Zn + Res, I1 is I + 1, getRes(R, Ch1, Zn1, I1, X, Y, Z).


agregation(X1,X2,Y1,Y2,Z,MinNum1, MinNum2, MinNum3):-agregationBad(X1,X2,Y1,Y2,Z,MinNum1),agregationNormal(X1,X2,Y1,Y2,Z,MinNum2),agregationGood(X1,X2,Y1,Y2,Z,MinNum3).

agregationBad(X1,X2,Y1,Y2,Z,MinNum):- goodY(Y1,MuY11), normalY(Y1,MuY12), max(MuY11, MuY12, ResY1), goodY(Y2, MuY21), normalY(Y2, MuY22),max(MuY21, MuY22, SubResY2), 
                                      badY(Y2, MuY23), max(MuY23, SubResY2, ResY2), goodX(X1, MuX11), normalX(X1, MuX12),
                                      max(MuX11, MuX12, ResX1),normalX(X2, MuX21),badX(X2, MuX22),max(MuX21, MuX22, ResX2), min(ResY1, ResY2, ResY), badZ(Z, MuZ), min(ResY, MuZ, SubRes), 
                                      min(ResX2,ResX1,ResX), min(ResX, SubRes, MinNum).

agregationNormal(X1,X2,Y1,Y2,Z,MinNum):- normalZ(Z, Mu), max(Mu, 0.5, Res), MinNum is Res .

agregationGood(X1,X2,Y1,Y2,Z,MinNum):-goodY(Y2,MuY21), normalY(Y2,MuY22), max(MuY21, MuY22, ResY2), goodY(Y1, MuY11), normalY(Y1, MuY12),max(MuY11, MuY12, SubResY1), 
                                      badY(Y1, MuY13), max(MuY13, SubResY1, ResY1), goodX(X2, MuX21), normalX(X2, MuX22),
                                      max(MuX21, MuX22, ResX2),normalX(X1, MuX11),badX(X1, MuX12),max(MuX11, MuX12, ResX1), min(ResY2, ResY1, ResY), goodZ(Z, MuZ), min(ResY, MuZ, SubRes), 
                                      min(ResX1,ResX2,ResX), min(ResX, SubRes, MinNum).

write_res(Res):-badRbool(Res), write("Team 1 Win"), !.
write_res(Res):-normalRbool(Res), write("Draw"), !.
write_res(Res):-goodRbool(Res), write("Team 2 WIn"), !.


%helpers

max(X,Y,X):-X>=Y,!.
max(X,Y,Y):-X<Y,!.
min(X,Y,X):-X<Y,!.
min(X,Y,Y):-X>=Y.