from PIL import Image
im = Image.open('US_Total_Debt_as_a_%_of_GDP.png')

imrgb = im.convert('RGB')
px = imrgb.load()

#Topmost = 59
Leftmost = 139
# 1916,botton pixel
(140, 722)
# 1921,botton pixel
(228, '...')
# 1926,botton pixel
(318, '...')
# 1931,botton pixel
(403, '...')
# 2010,bottom pixel
(1808, 722)
Rightmost = 1808
Bottommost = 722
# (1808-139)/(2010-1916)
# 17.75531914893617021276

def is_red(rgb):
    r, g, b = rgb
    return r > 200 and g < 60 and b < 60

height = []
for x in range(Leftmost, Rightmost+1):
    for y in range(Bottommost, 0, -1):
        p = px[x, y]
        # print(x, y, p, is_red(p))
        if is_red(p):
            # calc mid -- interpolating a pixelated chart is imprecise, so inclue bounds
            low = y
            y2 = y
            while y2 > 0 and is_red(p):
                y2 -= 1
                p = px[x, y2]
            hi = y2
            mid = min(low, hi) + (abs(low - hi) // 2)
            height.append(mid)
            break
print(height)


# 400% - 160 (93)
# 350% - 253 (96)
# 300% - 349 (92)
# 250% - 441 (94)
# 200% - 534 (96)
# 150% - 630 (92)
# 100% - 722
# (722-160)/300.
# 1.87333333333333333333 
def h2pct(h):
    return round((float(Bottommost) - h) / 1.87333 + 100., 2)
pcts = [h2pct(h) for h in height]
print(pcts)


with open('US_Total_Debt_as_a_%_of_GDP.csv', 'w') as f:
    f.write('date,pct\n')
    for n, year in enumerate(range(1916, 2010+1)):
        pixelsperyear = 17.7553
        for month in range(1, 12 + 1):
            pctyear = float(month - 1.) / 12
            offset = Leftmost + (pixelsperyear * n) + (pixelsperyear * pctyear)
            o = round(offset)
            if o - Leftmost < len(pcts):
                p = pcts[o - Leftmost]
                f.write('{}-{:02d}-01,{}\n'.format(year, month, p))
