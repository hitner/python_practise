import poker

out1 = poker.min3_from_monocolor_visual('A234567890JQKVW')

print(out1)

out2 = poker.min3_from_color_visual('2A2223444546676889808J8Q2K0V0W')

print(out2)

out3 = poker.visual_from_monocolor_min3(out1)

print(out3)

out4 = poker.visual_from_color_min3(out2)

print(out4)

print(poker.visual_from_color_min3(poker.MIN3_ALL))
