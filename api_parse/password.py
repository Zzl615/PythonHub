import bcrypt

# 假设我们有一个明文密码
password = b"qwer1234"

# 使用bcrypt散列密码
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)