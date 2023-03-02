
# あらかじめ作っておいたfood_list.txtを呼び出す。
f = open('food_list.txt')
data1 = f.read()
f.close()
lines = data1.split('\n')

f = open('receipt.txt')
data2 = f.read()
f.close()
receipt_data = data2.split('\n')

# 食材リストとレシートのデータを照らし合わせて照合するものが存在すればsearch_wordsに加える
search_words = []
for word in lines:
    for receipt in receipt_data:
        if word in receipt:
            search_words.append(word)

print(search_words)
search_words.sort(key=len, reverse=True)
search_words = search_words[:2]
print("search_words is ....", search_words, "\n")