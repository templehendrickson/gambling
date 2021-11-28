from deucesLib import Deck,Card,Evaluator

def deucesFormatConvert(s):
    # input standard string format, output deuces card format
    # H14 -> Ah

    convDict = {
        '11':'J',
        '12':'Q',
        '13':'K',
        '14':'A'
    }

    suit = s[0]
    val = s[1:]

    if val in list(convDict.keys()):
        val = convDict[val]

    newS = val + suit.lower()

    print(newS)

    cardObj = Card.new(newS)

    return cardObj

## testing the converter
# test = deucesFormatConvert('H13')
# Card.printCards([test])

## testing drawing from the package
# deck = Deck()
# hand1 = deck.draw(2)
# hand2 = deck.draw(2)

# Card.printCards(hand1)
# Card.printCards(hand2)

# def printEvalWrapper(evaluator,score):
#     t = evaluator.class_to_string(evaluator.get_rank_class(score))
#     print(t)

## testing evaluator
# deck = Deck()
# board = deck.draw(5)
# hand1 = deck.draw(2)
# hand2 = deck.draw(2)

# eval = Evaluator()

# hand1_score = eval.evaluate(hand1,board)
# hand2_score = eval.evaluate(cards=hand2,board=board)

# print('board dealt: {}'.format(board))
# print('hand1 dealt: {}'.format(hand1))
# print('hand2 dealt: {}'.format(hand2))

# print('board')
# Card.printCards(board)

# print('hand 1')
# Card.printCards(hand1)

# print('hand 2')
# Card.printCards(hand2)

# print('hand1_score: {}'.format(hand1_score))
# print('hand2_score: {}'.format(hand2_score))

# ## in deuces, lower score is better

# if hand1_score < hand2_score:
#     print('hand 1 won')

# else:
#     print('hand 2 won')

# print('hand 1 type')
# printEvalWrapper(eval,hand1_score)

# print('hand 2 type')
# printEvalWrapper(eval,hand2_score)

# print('complete')

