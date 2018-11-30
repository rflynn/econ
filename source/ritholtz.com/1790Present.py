from PIL import Image
im = Image.open('1790-Present.gif')

imrgb = im.convert('RGB')
px = imrgb.load()

'''
im = Image.open('px.gif')
0 0 (255, 0, 0)
1 0 (0, 255, 0)
2 0 (0, 0, 255)
0 1 (0, 0, 0)
1 1 (136, 136, 136)
2 1 (255, 255, 255)
'''

# 1790,botton pixel
(29, 486)
# 1795, bottom
(52, 486)

# 2010, bottom pixel
(1067, 486)

# 2005, bottom pixel
(1046, 486)

def is_blackish(rgb):
    r, g, b = rgb
    return r == g and g == b and r < 50

def is_whitish(rgb):
    r, g, b = rgb
    return r > 200 and g > 200 and b > 200

height = []
for x in range(29, 1067+1):
    for y in range(486, 0, -1):
        p = px[x, y]
        # print(x, y, px[x,y])
        if is_whitish(p) or is_blackish(p):
            height.append(y)
            break
print(height)


# 1% - 486
# 2% - 455 - 31
# 3% - 424 - 31
# 4% - 393 - 31
# 5% - 362 - 31
# 6% - 331 - 31
# 7% - 300 - 31
# 8% - 269 - 31
pcts = [round(abs(486 - h) / 31. + 1., 2) for h in height]
print(pcts)


with open('1790Present.csv', 'w') as f:
    for n, year in enumerate(range(1790, 2010, 1)):
        #offset = 52 + (23.66 * n)
        offset = 28.8 + ((23.66 / 5) * n)
        o = round(offset)
        f.write('{},{}\n'.format(year, pcts[o - 29]))
