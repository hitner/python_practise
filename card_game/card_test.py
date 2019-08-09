import card


bin_cards = card.bin_card_from_terminal_string('!Wd2c3h0bK')

print(bin_cards)

again = card.bin_card_to_terminal_output(bin_cards)

print(again)

assert '!W♦2♣3♥0♠K' == again

nocolors = card.bin_card_remove_color(bin_cards)
nocolor_str = card.bin_card_to_terminal_output(nocolors)
print(nocolor_str)

base64_show = card.bin_cards_to_base64(bin_cards)
print(f'base64 {base64_show}')
back_from_64 = card.bin_cards_from_base64(base64_show)
print(f'back from base64 {card.bin_card_to_terminal_output(back_from_64)}')


print(card.bin_card_to_terminal_output(card.one_deck))

orgin_cards = list(card.one_deck)
card.fisher_yates_shuffle(orgin_cards)
print(card.bin_card_to_terminal_output(orgin_cards))


## some
before_remove = list(card.one_deck)
is_remove = card.bin_cards_remove_some(before_remove, bin_cards)
print(card.bin_card_to_terminal_output(before_remove))


after_sorted = card.sort_by_doudizhu_rule(before_remove)
print(card.bin_card_to_terminal_output(after_sorted))
print (type(after_sorted))