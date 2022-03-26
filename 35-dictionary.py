d = {}
# d={"George":24,"Tom":32}
d["George"] = 24
d["Tom"] = 32
d["Jenny"] = 16

print(d["George"])
print(d["Tom"])

# keys are commonly string or number
d[10] = 100
print(d[10])

# how to iterate over key-value paris?
for key, value in d.items():
    print("key:")
    print(key)
    print("value:")
    print(value)
    print("")

