from matplotlib import pyplot as plt

target = []
predicted = []
with open('testing', encoding='utf-8') as in_file:
    in_file.readline()
    for line in in_file:
        l =line.strip().split()
        target.append(float(l[3]))

with open('.\\result\\RBF_ALL_output', encoding='utf-8') as in_file:
    in_file.readline()
    in_file.readline()
    for line in in_file:
        predicted.append(float(line.strip()))

print(target)
print(len(target))
print(predicted)
print(len(predicted))
predict_to_mae = {}
keys = []
mae = [abs(target[i] - predicted[i]) for i in range(1000)]
for idx, item in enumerate(target):
    str_item = round(item, 1)
    if str_item not in predict_to_mae:
        predict_to_mae[str_item] = [mae[idx]]
        keys.append(str_item)
    else:
        predict_to_mae[str_item].append(mae[idx])

print(predict_to_mae)


print(sum(mae) / 1000)

plt.figure(1)
plt.scatter(target, mae, s=10)
plt.xlim(1.0, 5.0)
plt.show()

keys.sort()
average_mae = []
for key in keys:
    average_mae.append(sum(predict_to_mae[key])/len(predict_to_mae[key]))

print(keys)
plt.plot(keys, average_mae)
plt.show()