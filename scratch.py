import numpy as np

info = np.array([0.5, 0.3, 0.2])
success = np.array([0.2, 0.3, 0.5])
power1 = info**1 * success**1
print('power 1')
print(power1/0.29)
print(sum(power1))
print(sum(power1/(info+success)))

power_5 = info**0.5 * success**0.5
print('power 0.5')
print(power_5/(sum(power_5)))
print(sum(power_5))

print('lookie here')
print(power_5/(info**0.5 + success**0.5))

power_43 = info**0.43 * success**0.43
print('power 0.43')
print(power_43)
print(sum(power_43))

power_47 = info**0.47 * success**0.47
print('power 0.47')
print(power_47)
print(sum(power_47))

print('---------------')

info = np.array([0.6, 0.3, 0.1])
success = np.array([0.1, 0.3, 0.6])
power1 = info**1 * success**1
print('power 1')
print(power1)
print(sum(power1))

power_5 = info**0.5 * success**0.5
print('power 0.5')
print(power_5)
print(sum(power_5))

print(info**0.5 + success**0.5)

power_43 = info**0.43 * success**0.43
print('power 0.43')
print(power_43)
print(sum(power_43))

power_47 = info**0.47 * success**0.47
print('power 0.47')
print(power_47)
print(sum(power_47))