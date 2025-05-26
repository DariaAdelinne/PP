% Extended family relations model

% Facts
% tatal( Father, Child ).
tatal(ilie, vasale).
tatal(popa, vasale).
tatal(george, ilie).
tatal(maria, ilie).
tatal(petru, popa).
tatal(vasilica, cobelea).
tatal(dana, pavel).

% mama( Mother, Child ).
mama(george, vasilica).
mama(maria, vasilica).
mama(vasilica, diana).
mama(petru, dana).
mama(matcu, dana).
mama(dana, elena).
mama(ilie, elena).
mama(popa, elena).

% Gender
barbat(george).
barbat(petru).
barbat(ilie).
barbat(popa).
barbat(vasale).
barbat(cobelea).
barbat(pavel).

femeie(maria).
femeie(matcu).
femeie(vasilica).
femeie(ileana).
femeie(dana).
femeie(diana).
femeie(elena).

% Marriages
sot(vasilica, ilie).
sot(dana, popa).
sot(ileana, petru).

% Uncles and aunts (derived)
% unchi( Uncle, NieceOrNephew ).
unchi(X, Y) :- tatal(X, A), tatal(Y, A), barbat(X), X \= Y.
unchi(X, Y) :- sot(X, W), unchi(W, Y).

% frate( Brother, Sibling ).
frate(X, Y) :- tatal(Z, X), tatal(Z, Y), barbat(X), X \= Y.

sora(X, Y) :- tatal(Z, X), tatal(Z, Y), femeie(X), X \= Y.

% matusa( Aunt, NieceOrNephew ).
matusa(X, Y) :- sot(X, W), sora(W, Y).
matusa(X, Y) :- tatal(P, K), sora(X, P), (tatal(K, Y); mama(K, Y)).

% Grandparents
bunicul(X, Y) :- barbat(X), (tatal(X, W); mama(X, W)), (tatal(W, Y); mama(W, Y)).
bunica(X, Y)   :- femeie(X), (tatal(X, W); mama(X, W)), (tatal(W, Y); mama(W, Y)).

% Grandchild
nepot(X, Y)   :- bunicul(Y, X).
nepoata(X, Y) :- bunica(Y, X).

% Cousins
verisor(X, Y) :- (tatal(P, X); mama(P, X)), (frate(P, S); sora(P, S)), (tatal(S, Y); mama(S, Y)).

% General kinship rule
ruda(X, Y) :- frate(X, Y); sora(X, Y);
              unchi(X, Y); matusa(X, Y);
              bunicul(X, Y); bunica(X, Y);
              nepot(X, Y); nepoata(X, Y);
              verisor(X, Y).

% Sample queries:
% ?- matusa(Aunt, vasale).
% ?- bunicul(Grandfather, dana).
% ?- sora(Sister, george).
% ?- nepot(Nephew, popa).
% ?- nepoata(Niece, ilie).
% ?- verisor(Cousin, cobelea).
% ?- ruda(Relation, elena).
