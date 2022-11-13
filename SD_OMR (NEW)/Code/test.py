import numpy as np

arr = np.array([41, 54, 43, 44, 52])

# Create an empty list
filter_arr  = []
counter_arr = []
counter=0
# go through each element in arr
for element in arr:
  # if the element is higher than 42, set the value to True, otherwise False:
  if element > 50:
    filter_arr.append(True)
  else:
    filter_arr.append(False)

for element in arr:
    print(element)

newarr = arr[filter_arr]
print(filter_arr)               #View values
print(counter_arr)

print(newarr)                   #View values
if(len(newarr)>1):
    print("Pass")
else:
    print("Failed")
