:- use_module(library(http/http_server)).
:- use_module(library(http/http_json)).
:- use_module(library(http/json)).

:- http_handler(/, handler(M), [method(M), methods([get]), time_limit(10000)]).
:- [ind2].

server :- http_server(http_dispatch, [port(4040)]).

handler(get, Req) :-
    http_parameters(Req, [
        x(X, [integer]),
        y(Y, [integer]), 
        z(Z, [integer]),
        x1(X1, [integer]),
        y1(Y1, [integer]),
        mx(MX, [float]),
        my(MY, [float]),
        mz(MZ, [float]),
        tgx(TgX, [float]),
        tgy(TgY, [float]),
        tgz(TgZ, [float]), 
        ry(Ry, [float])
    ]),
    res(X, MX, TgX, Y, MY, TgY, Ry, Z, MZ, TgZ, X1, Y1, Res),
    reply_json_dict(res{type: Res}).
